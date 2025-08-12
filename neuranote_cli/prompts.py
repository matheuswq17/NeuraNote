CHUNK_SOAP_PROMPT = """Você é um assistente clínico ético. Resuma APENAS este trecho da transcrição no formato SOAP.
REGRAS: sem diagnóstico; cite evidências literais (entre aspas) quando possível; marque "informação insuficiente" se faltar base.
Retorne JSON válido.

TRECHO:
{chunk}

SAÍDA (JSON):
{{
  "S": "...",
  "O": "...",
  "A": {{"hipoteses": ["..."], "incertezas": ["..."], "evidencias": ["trecho 1", "trecho 2"]}},
  "P": {{"proximos_passos": ["..."], "tarefas": ["..."], "alertas": ["..."]}}
}}
"""

CHUNK_PHEE_PROMPT = """Você é um assistente clínico ético. Resuma APENAS este trecho no formato PHEE.
REGRAS: sem diagnóstico; inclua evidências literais quando possível; marque "informação insuficiente" se faltar base.
Retorne JSON válido.

TRECHO:
{chunk}

SAÍDA (JSON):
{{
  "Problema": "...",
  "Hipoteses": ["..."],
  "Evidencias": ["trecho 1", "trecho 2"],
  "Encaminhamentos": ["..."]
}}
"""

AGG_SOAP_PROMPT = """Você irá AGREGAR vários resumos parciais (em JSON) de uma mesma sessão (vários trechos).
Produza um único resumo final SOAP consistente, sem repetir informações, preservando a ética:
- Sem diagnóstico fechado; apenas hipóteses/observações.
- Inclua evidências literais representativas (sem excesso).
- Mantenha tom clínico, claro e objetivo.

RESUMOS PARCIAIS (JSON por linha):
{partials}

SAÍDA (JSON FINAL):
{{
  "S": "...",
  "O": "...",
  "A": {{"hipoteses": ["..."], "incertezas": ["..."], "evidencias": ["trecho 1", "trecho 2"]}},
  "P": {{"proximos_passos": ["..."], "tarefas": ["..."], "alertas": ["..."]}}
}}
"""

AGG_PHEE_PROMPT = """Você irá AGREGAR vários resumos parciais (em JSON) de uma mesma sessão (vários trechos).
Produza um único resumo final PHEE consistente, sem repetir informações, preservando a ética:
- Sem diagnóstico fechado; apenas hipóteses/observações.
- Inclua evidências literais representativas (sem excesso).
- Tom clínico, claro e objetivo.

RESUMOS PARCIAIS (JSON por linha):
{partials}

SAÍDA (JSON FINAL):
{{
  "Problema": "...",
  "Hipoteses": ["..."],
  "Evidencias": ["trecho 1", "trecho 2"],
  "Encaminhamentos": ["..."]
}}
"""
