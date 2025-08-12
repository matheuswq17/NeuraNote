import os
import pathlib
from typing import List

def ensure_dir(p: pathlib.Path):
    p.mkdir(parents=True, exist_ok=True)

def getenv_required(name: str) -> str:
    val = os.getenv(name)
    if not val:
        raise EnvironmentError(f"Variável de ambiente obrigatória ausente: {name}")
    return val

def chunk_text(text: str, max_chars: int = 6000, overlap: int = 400) -> List[str]:
    """
    Divide o texto em blocos ~6000 caracteres com sobreposição para contexto.
    Evita quebrar no meio de frases quando possível.
    """
    text = text.strip()
    if len(text) <= max_chars:
        return [text]

    chunks = []
    start = 0
    while start < len(text):
        end = min(start + max_chars, len(text))
        # tenta recuar até o último ponto final ou quebra de linha para fechar o chunk
        cut = max(text.rfind(". ", start, end), text.rfind("\n", start, end))
        if cut == -1 or cut <= start + 1000:  # não encontrou um bom corte
            cut = end
        chunk = text[start:cut].strip()
        if chunk:
            chunks.append(chunk)
        start = max(cut - overlap, cut)  # sobreposição leve
    return chunks
