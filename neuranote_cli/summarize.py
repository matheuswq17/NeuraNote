import json
import os
import subprocess
from dotenv import load_dotenv
load_dotenv()
from typing import Dict, Any, List
from prompts import (
    CHUNK_SOAP_PROMPT, CHUNK_PHEE_PROMPT,
    AGG_SOAP_PROMPT, AGG_PHEE_PROMPT
)
from utils import getenv_required, chunk_text

def _extract_json(text: str) -> Dict[str, Any]:
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1 or end <= start:
        return {"raw": text.strip()}
    try:
        return json.loads(text[start:end+1])
    except Exception:
        return {"raw": text.strip()}

# ====== OLLAMA LOCAL ======
def call_ollama(prompt: str, model: str = None) -> str:
    model = model or os.getenv("OLLAMA_MODEL", "llama3.1:8b")
    proc = subprocess.run(["ollama", "run", model, prompt], capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError(f"Ollama erro: {proc.stderr}")
    return proc.stdout

# ====== OPENAI API ======
def call_openai(prompt: str, model: str = None) -> str:
    from openai import OpenAI
    api_key = getenv_required("OPENAI_API_KEY")
    client = OpenAI(api_key=api_key)
    model = model or os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    resp = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "Você é um assistente clínico ético que segue regras estritas."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )
    return resp.choices[0].message.content

def _llm(prompt: str, engine: str) -> str:
    if engine == "ollama":
        return call_ollama(prompt)
    elif engine == "openai":
        return call_openai(prompt)
    else:
        raise ValueError("engine deve ser 'ollama' ou 'openai'.")

def _summarize_chunk(chunk: str, fmt: str, engine: str) -> Dict[str, Any]:
    tmpl = CHUNK_SOAP_PROMPT if fmt.upper() == "SOAP" else CHUNK_PHEE_PROMPT
    out = _llm(tmpl.format(chunk=chunk), engine)
    return _extract_json(out)

def _aggregate(partials: List[Dict[str, Any]], fmt: str, engine: str) -> Dict[str, Any]:
    # serializa parciais em JSON-lines
    lines = "\n".join(json.dumps(p, ensure_ascii=False) for p in partials)
    tmpl = AGG_SOAP_PROMPT if fmt.upper() == "SOAP" else AGG_PHEE_PROMPT
    out = _llm(tmpl.format(partials=lines), engine)
    return _extract_json(out)

def summarize(transcript: str, fmt: str = "SOAP", engine: str = "ollama") -> Dict[str, Any]:
    # 1) dividir em pedaços
    chunks = chunk_text(transcript, max_chars=int(os.getenv("CHUNK_MAX_CHARS", "6000")))
    # 2) mapear cada pedaço -> resumo parcial
    partials = [_summarize_chunk(c, fmt, engine) for c in chunks]
    # 3) reduzir/agregar em um resumo final consistente
    final = _aggregate(partials, fmt, engine)
    # anexa metadados úteis
    return {"format": fmt, "engine": engine, "chunks": len(chunks), "partials": partials, "final": final}
