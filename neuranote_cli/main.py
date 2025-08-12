import argparse
import pathlib
import json
import time
import datetime
import textwrap
from transcribe import transcribe
from summarize import summarize
from utils import ensure_dir

LINE = "─" * 72

def bullets(items):
    items = items or []
    if not items:
        return "- (vazio)"
    return "\n".join(f"- {it}" for it in items)

def wrap(text, width=100, indent=0):
    if not text:
        return ""
    ind = " " * indent
    return "\n".join(textwrap.fill(line, width=width, subsequent_indent=ind, drop_whitespace=False)
                     for line in text.splitlines())

def write_pretty_soap(final, meta, outpath: pathlib.Path):
    S = final.get("S", "")
    O = final.get("O", "")
    A = final.get("A", {}) or {}
    P = final.get("P", {}) or {}

    content = [
        f"NeuraNote — Resumo da Sessão (SOAP)",
        LINE,
        f"Arquivo: {meta['file_name']}",
        f"Gerado em: {meta['generated_at']}",
        f"Transcrição: Whisper {meta['whisper_model']}  |  Engine: {meta['engine']}  |  Chunks: {meta['chunks']}",
        LINE,
        "S — Subjetivo (conciso)",
        wrap(S, width=100),
        "",
        "O — Objetivo",
        wrap(O, width=100),
        "",
        "A — Avaliação",
        "• Hipóteses:",
        bullets(A.get("hipoteses", [])),
        "",
        "• Incertezas:",
        bullets(A.get("incertezas", [])),
        "",
        "• Evidências (trechos literais):",
        bullets(A.get("evidencias", [])),
        "",
        "P — Plano",
        "• Próximos passos:",
        bullets(P.get("proximos_passos", [])),
        "",
        "• Tarefas:",
        bullets(P.get("tarefas", [])),
        "",
        "• Alertas:",
        bullets(P.get("alertas", [])),
        "",
        LINE
    ]
    outpath.write_text("\n".join(content), encoding="utf-8")
    return outpath

def write_pretty_phee(final, meta, outpath: pathlib.Path):
    content = [
        f"NeuraNote — Resumo da Sessão (PHEE)",
        LINE,
        f"Arquivo: {meta['file_name']}",
        f"Gerado em: {meta['generated_at']}",
        f"Transcrição: Whisper {meta['whisper_model']}  |  Engine: {meta['engine']}  |  Chunks: {meta['chunks']}",
        LINE,
        "Problema",
        wrap(final.get("Problema",""), width=100),
        "",
        "Hipóteses",
        bullets(final.get("Hipoteses", [])),
        "",
        "Evidências (trechos literais)",
        bullets(final.get("Evidencias", [])),
        "",
        "Encaminhamentos",
        bullets(final.get("Encaminhamentos", [])),
        "",
        LINE
    ]
    outpath.write_text("\n".join(content), encoding="utf-8")
    return outpath

def main():
    parser = argparse.ArgumentParser(description="NeuraNote CLI - transcreve e resume um áudio clínico.")
    parser.add_argument("--audio", required=True, help="Caminho para o arquivo de áudio (wav/mp3/m4a...).")
    parser.add_argument("--format", choices=["SOAP", "PHEE"], default="SOAP", help="Formato do resumo.")
    parser.add_argument("--engine", choices=["ollama", "openai"], default="ollama", help="Motor de resumo.")
    parser.add_argument("--whisper_model", default="small", help="Modelo do faster-whisper (tiny/base/small/medium/large).")
    parser.add_argument("--outdir", default="out", help="Pasta de saída.")
    args = parser.parse_args()

    t0 = time.perf_counter()

    audio_path = pathlib.Path(args.audio)
    if not audio_path.exists():
        raise FileNotFoundError(f"Áudio não encontrado: {audio_path}")

    outdir = pathlib.Path(args.outdir)
    ensure_dir(outdir)

    # 1) Transcrição
    print("🧾 Transcrevendo com faster-whisper...")
    start_trans = time.perf_counter()
    transcript = transcribe(str(audio_path), model_size=args.whisper_model)
    end_trans = time.perf_counter()
    transcript_file = outdir / (audio_path.stem + "_transcript.txt")
    transcript_file.write_text(transcript, encoding="utf-8")
    print(f"✅ Transcrição salva em {transcript_file}")
    print(f"⏱️ Tempo de transcrição: {end_trans - start_trans:.2f} segundos")

    # 2) Resumo
    print(f"✍️ Resumindo em {args.format} com {args.engine}...")
    start_sum = time.perf_counter()
    result = summarize(transcript, fmt=args.format, engine=args.engine)
    end_sum = time.perf_counter()

    partials_file = outdir / (audio_path.stem + "_partials.json")
    summary_json_file = outdir / (audio_path.stem + "_summary.json")
    partials_file.write_text(json.dumps(result.get("partials", []), ensure_ascii=False, indent=2), encoding="utf-8")
    summary_json_file.write_text(json.dumps(result.get("final", {}), ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"✅ Parciais: {partials_file}")
    print(f"✅ Resumo final (JSON): {summary_json_file}\n")
    print(json.dumps(result.get("final", {}), ensure_ascii=False, indent=2))
    print(f"⏱️ Tempo de resumo: {end_sum - start_sum:.2f} segundos")

    # 3) TXT legível com títulos e listas
    final = result.get("final", {}) or {}
    meta = {
        "file_name": audio_path.name,
        "generated_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "whisper_model": args.whisper_model,
        "engine": args.engine,
        "chunks": result.get("chunks", 1),
    }
    summary_txt_file = outdir / (audio_path.stem + "_summary.txt")
    if args.format.upper() == "SOAP":
        write_pretty_soap(final, meta, summary_txt_file)
    else:
        write_pretty_phee(final, meta, summary_txt_file)
    print(f"📝 Resumo legível (TXT): {summary_txt_file}")

    # 4) Tempo total
    t1 = time.perf_counter()
    print(f"⏲️ Tempo total: {t1 - t0:.2f} segundos")

if __name__ == "__main__":
    main()
