import argparse
import pathlib
import json
import time
from transcribe import transcribe
from summarize import summarize
from utils import ensure_dir

def main():
    parser = argparse.ArgumentParser(description="NeuraNote CLI - transcreve e resume um áudio clínico.")
    parser.add_argument("--audio", required=True, help="Caminho para o arquivo de áudio (wav/mp3/m4a...).")
    parser.add_argument("--format", choices=["SOAP", "PHEE"], default="SOAP", help="Formato do resumo.")
    parser.add_argument("--engine", choices=["ollama", "openai"], default="ollama", help="Motor de resumo.")
    parser.add_argument("--whisper_model", default="small", help="Modelo do faster-whisper (tiny/base/small/medium/large).")
    parser.add_argument("--outdir", default="out", help="Pasta de saída.")
    args = parser.parse_args()

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

    # 3) TXT legível
    final = result.get("final", {}) or {}
    pretty_txt = []

    if args.format.upper() == "SOAP":
        pretty_txt.append("=== SOAP ===")
        pretty_txt.append(f"S: {final.get('S','')}")
        pretty_txt.append(f"O: {final.get('O','')}")
        A = final.get('A', {}) or {}
        pretty_txt.append("A:")
        pretty_txt.append(f"  - Hipóteses: {', '.join(A.get('hipoteses', []) or [])}")
        pretty_txt.append(f"  - Incertezas: {', '.join(A.get('incertezas', []) or [])}")
        pretty_txt.append(f"  - Evidências: {', '.join(A.get('evidencias', []) or [])}")
        P = final.get('P', {}) or {}
        pretty_txt.append("P:")
        pretty_txt.append(f"  - Próximos passos: {', '.join(P.get('proximos_passos', []) or [])}")
        pretty_txt.append(f"  - Tarefas: {', '.join(P.get('tarefas', []) or [])}")
        pretty_txt.append(f"  - Alertas: {', '.join(P.get('alertas', []) or [])}")
    else:
        pretty_txt.append("=== PHEE ===")
        pretty_txt.append(f"Problema: {final.get('Problema','')}")
        pretty_txt.append(f"Hipóteses: {', '.join(final.get('Hipoteses', []) or [])}")
        pretty_txt.append(f"Evidências: {', '.join(final.get('Evidencias', []) or [])}")
        pretty_txt.append(f"Encaminhamentos: {', '.join(final.get('Encaminhamentos', []) or [])}")

    summary_txt_file = outdir / (audio_path.stem + "_summary.txt")
    summary_txt_file.write_text("\n".join(pretty_txt), encoding="utf-8")
    print(f"📝 Resumo legível (TXT): {summary_txt_file}")

if __name__ == "__main__":
    main()
