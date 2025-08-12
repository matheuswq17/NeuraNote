CHUNK_SOAP_PROMPT = """Você é um assistente clínico ético. Resuma APENAS este trecho no formato SOAP.

REGRAS:
- NÃO faça diagnóstico; use hipóteses/observações.
- S (Subjetivo) deve ser CONCISO: 1 a 3 linhas, apenas queixas e mudanças relevantes.
- Cite evidências LITERAIS entre aspas quando possível (em A).
- Se faltar base, escreva "informação insuficiente".
- Tom clínico, claro e objetivo.
- Retorne **JSON válido**.

TRECHO:
{chunk}

SAÍDA (JSON):
{{
  "S": "1 a 3 linhas, conciso",
  "O": "observações verificáveis",
  "A": {{
    "hipoteses": ["..."],
    "incertezas": ["..."],
    "evidencias": ["trecho 1", "trecho 2"]
  }},
  "P": {{
    "proximos_passos": ["..."],   // manter essa seção
    "tarefas": ["..."],           // manter essa seção
    "alertas": ["..."]
  }}
}}
"""

CHUNK_PHEE_PROMPT = """Você é um assistente clínico ético. Resuma APENAS este trecho no formato PHEE.

REGRAS:
- Sem diagnóstico; use hipóteses/observações.
- Inclua evidências LITERAIS quando possível.
- Se faltar base, escreva "informação insuficiente".
- Tom clínico, claro e objetivo.
- Retorne **JSON válido**.

TRECHO:
{chunk}

SAÍDA (JSON):
{{
  "Problema": "conciso",
  "Hipoteses": ["..."],
  "Evidencias": ["trecho 1", "trecho 2"],
  "Encaminhamentos": ["..."]  // pode incluir próximos passos/tarefas quando fizer sentido
}}
"""

AGG_SOAP_PROMPT = """Você agregará vários resumos parciais (JSON) de uma sessão.

REGRAS DE AGREGAÇÃO:
- Produza um **único** SOAP consistente.
- **S conciso (1–3 linhas)**: apenas queixas e mudanças relevantes.
- Não repita conteúdo; una as evidências representativas em A.
- Sem diagnóstico fechado; apenas hipóteses/observações.
- Mantenha **Próximos passos** e **Tarefas** em P como listas separadas.

RESUMOS PARCIAIS (um JSON por linha):
{partials}

SAÍDA (JSON FINAL):
{{
  "S": "1 a 3 linhas, conciso",
  "O": "observações verificáveis",
  "A": {{
    "hipoteses": ["..."],
    "incertezas": ["..."],
    "evidencias": ["trecho 1", "trecho 2"]
  }},
  "P": {{
    "proximos_passos": ["..."],
    "tarefas": ["..."],
    "alertas": ["..."]
  }}
}}
"""

AGG_PHEE_PROMPT = """Você agregará vários resumos parciais (JSON) de uma sessão.

REGRAS DE AGREGAÇÃO:
- Produza um PHEE único, sem repetições.
- Sem diagnóstico; hipóteses/observações.
- Evidências literais representativas.
- Encaminhamentos podem incluir próximos passos e tarefas quando fizer sentido.

RESUMOS PARCIAIS (um JSON por linha):
{partials}

SAÍDA (JSON FINAL):
{{
  "Problema": "conciso",
  "Hipoteses": ["..."],
  "Evidencias": ["trecho 1", "trecho 2"],
  "Encaminhamentos": ["..."]
}}
"""
