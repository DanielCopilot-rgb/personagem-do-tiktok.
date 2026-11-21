import os
import json
import urllib.request
import urllib.error
from pathlib import Path

MODELO = "gemini-3.8-flash"

EXPRESSOES = [
    "sorriso_fechado",
    "serio_boca_reta",
    "fala_boca_aberta",
    "fala_olhos_fechados",
    "feliz_olhos_fechados",
    "riso_boca_aberta",
    "satisfeito_olhos_fechados",
    "cansado_olhos_fechados"
]


def obter_chave_api(caminho=None):
    """Obtém a chave do ambiente ou, como fallback, de ~/.gemini_env."""
    chave = os.getenv("GEMINI_API_KEY")
    if chave and chave.strip():
        return chave.strip()

    arquivo = Path(caminho) if caminho else Path.home() / ".gemini_env"
    try:
        linhas = arquivo.read_text(encoding="utf-8").splitlines()
    except OSError:
        return None

    for linha in linhas:
        linha = linha.strip()
        if not linha or linha.startswith("#"):
            continue
        if linha.startswith("export "):
            linha = linha[len("export "):].strip()

        nome, separador, valor = linha.partition("=")
        if separador and nome.strip() == "GEMINI_API_KEY":
            valor = valor.strip()
            if len(valor) >= 2 and valor[0] == valor[-1] and valor[0] in "\"'":
                valor = valor[1:-1]
            return valor or None

    return None


def analisar_historia(caminho):
    chave = obter_chave_api()

    if not chave:
        raise RuntimeError("GEMINI_API_KEY não configurada no ambiente nem em ~/.gemini_env.")

    with open(caminho, encoding="utf-8") as arquivo:
        historia = arquivo.read().strip()

    if not historia:
        raise ValueError("O arquivo da história está vazio.")

    prompt = f"""
Você é um analista de narrativas para um personagem animado.

Sua tarefa é interpretar a história escrita pelo autor.
NÃO reescreva a história.
NÃO invente acontecimentos.
Considere o contexto das frases anteriores e a evolução da narrativa.

Divida a história em trechos naturais.
Para cada trecho, identifique:
- texto: trecho original, sem reescrever;
- emocao: emoção predominante;
- contexto: o que está acontecendo naquele momento;
- expressao: uma das expressões permitidas.

Expressões disponíveis:
{EXPRESSOES}

Escolha somente expressões dessa lista.
Não invente expressões que não existem.
Se houver dúvida, escolha sorriso_fechado.

Responda exclusivamente em JSON neste formato:
{{
  "cenas": [
    {{
      "texto": "trecho original",
      "emocao": "emoção identificada",
      "contexto": "descrição breve",
      "expressao": "nome_da_expressao"
    }}
  ]
}}

HISTÓRIA:
{historia}
"""

    dados = {
        "contents": [{
            "parts": [{"text": prompt}]
        }],
        "generationConfig": {
            "responseMimeType": "application/json",
            "temperature": 0.2
        }
    }

    url = (
        "https://generativelanguage.googleapis.com/v1beta/"
        f"models/{MODELO}:generateContent"
    )

    requisicao = urllib.request.Request(
        url,
        data=json.dumps(dados).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "x-goog-api-key": chave
        },
        method="POST"
    )

    try:
        with urllib.request.urlopen(requisicao, timeout=120) as resposta:
            resultado = json.loads(resposta.read().decode("utf-8"))

        texto = resultado["candidates"][0]["content"]["parts"][0]["text"]
        analise = json.loads(texto)

    except urllib.error.HTTPError as erro:
        detalhe = erro.read().decode("utf-8", errors="replace")
        raise RuntimeError(
            f"Erro da API ({erro.code}): {detalhe}"
        ) from erro

    except (KeyError, IndexError, json.JSONDecodeError) as erro:
        raise RuntimeError(
            f"Resposta inesperada do Gemini: {erro}"
        ) from erro

    if not isinstance(analise.get("cenas"), list):
        raise RuntimeError("A resposta não contém uma lista de cenas válida.")

    for cena in analise["cenas"]:
        if cena.get("expressao") not in EXPRESSOES:
            cena["expressao"] = "sorriso_fechado"

    return analise


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Uso: python gemini.py arquivo_da_historia.txt")
        sys.exit(1)

    try:
        resultado = analisar_historia(sys.argv[1])
        print(json.dumps(resultado, ensure_ascii=False, indent=2))
    except Exception as erro:
        print(f"ERRO: {erro}")
        sys.exit(1)
