# NeuraNote CLI (transcrever + resumir)

CLI simples: você fornece um arquivo de áudio gravado (wav/mp3/m4a...), ele transcreve com `faster-whisper` e resume em SOAP ou PHEE usando **Ollama** (local) ou **OpenAI**.

## Pré-requisitos
- Python 3.10+
- FFmpeg instalado no sistema (obrigatório para Whisper)
- (Opcional) **Ollama** se quiser rodar o LLM local: https://ollama.com
- (Opcional) **OpenAI**: exporte `OPENAI_API_KEY`

## Instalação
```bash
pip install -r requirements.txt