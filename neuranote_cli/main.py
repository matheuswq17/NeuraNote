import argparse
import pathlib
import json
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
    transcript = transcribe(str(audio_path), model_size=args.whisper_model)
    transcript_file = outdir / (audio_path.stem + "_transcript.txt")
    transcript_file.write_text(transcript, encoding="utf-8")
    print(f"✅ Transcrição salva em {transcript_file}")

    # 2) Resumo
    print(f"✍️ Resumindo em {args.format} com {args.engine}...")
    summary = summarize(transcript, fmt=args.format, engine=args.engine)

    summary_file = outdir / (audio_path.stem + "_summary.json")
    summary_file.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"✅ Resumo salvo em {summary_file}\n")

    print("📤 Saída:")
    print(json.dumps(summary, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
