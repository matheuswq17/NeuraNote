from faster_whisper import WhisperModel

def transcribe(audio_path: str, model_size: str = "small") -> str:
    """
    Transcreve um arquivo de áudio local usando faster-whisper.
    Requer ffmpeg instalado no sistema.
    """
    # Escolha do compute_type: int8 ou float16 (GPU). int8 é leve e roda em CPU.
    model = WhisperModel(model_size, device="cpu", compute_type="int8")
    segments, info = model.transcribe(
        audio_path,
        vad_filter=True,
        vad_parameters=dict(min_silence_duration_ms=500),
        beam_size=5
    )
    text_parts = [seg.text for seg in segments]
    text = "".join(text_parts).strip()
    return text
