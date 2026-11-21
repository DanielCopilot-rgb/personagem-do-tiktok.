import re
import unicodedata


def normalizar(texto):
    texto = texto.lower()
    texto = unicodedata.normalize("NFD", texto)
    return "".join(c for c in texto if unicodedata.category(c) != "Mn")


def dividir_texto(texto):
    paragrafos = [p.strip() for p in texto.splitlines() if p.strip()]
    trechos = []

    for paragrafo in paragrafos:
        frases = re.split(r'(?<=[.!?])\s+', paragrafo)
        trechos.extend(f.strip() for f in frases if f.strip())

    return trechos


def contem(texto, palavras):
    """Procura palavras/frases completas e evita falsos positivos por substring."""
    negacoes = {"nao", "nunca", "jamais"}

    for palavra in palavras:
        padrao = r"(?<!\w)" + re.escape(palavra) + r"(?!\w)"
        for correspondencia in re.finditer(padrao, texto):
            # Expressões que já incluem "não" são intenções afirmativas,
            # como "não aguento mais", e não devem ser descartadas.
            if palavra.startswith("nao "):
                return True

            anterior = texto[:correspondencia.start()].split()[-3:]
            if not negacoes.intersection(anterior):
                return True

    return False


def escolher_expressao(frase, historico):
    texto = normalizar(frase)
    contexto = normalizar(" ".join(historico[-2:]))

    cansaco = [
        "estou cansado", "estou exausto", "que sono",
        "nao aguento mais", "estou com sono"
    ]

    alegria = [
        "estou feliz", "que alegria", "maravilhoso",
        "incrivel", "adorei", "consegui", "deu certo",
        "que bom", "estou animado"
    ]

    humor = [
        "haha", "hahaha", "kkkk", "engracado",
        "que piada", "muito divertido", "hilario"
    ]

    seriedade = [
        "cuidado", "perigo", "importante", "atencao",
        "precisamos conversar", "problema", "risco",
        "infelizmente", "perdemos"
    ]

    satisfacao = [
        "finalmente", "conseguimos", "missao cumprida",
        "estou satisfeito", "valeu a pena", "terminamos"
    ]

    suspense = [
        "misterio", "estranho", "barulho", "escuro",
        "nao acredito", "o que foi isso", "de repente",
        "algo estava", "criatura", "surpresa"
    ]

    # Prioridade para emoções mais específicas.
    if contem(texto, cansaco):
        return "cansado_olhos_fechados"

    if contem(texto, humor):
        return "riso_boca_aberta"

    if contem(texto, satisfacao):
        return "satisfeito_olhos_fechados"

    if contem(texto, alegria):
        return "feliz_olhos_fechados"

    if contem(texto, seriedade):
        return "serio_boca_reta"

    if contem(texto, suspense):
        return "serio_boca_reta"

    # O contexto anterior ajuda a manter a expressão coerente.
    if contem(contexto, ["misterio", "perigo", "ameaca", "estranho"]):
        return "serio_boca_reta"

    if "?" in frase and contem(contexto, ["problema", "perigo", "misterio"]):
        return "serio_boca_reta"

    return "sorriso_fechado"


def interpretar_roteiro(caminho):
    with open(caminho, encoding="utf-8") as arquivo:
        texto = arquivo.read()

    # Compatibilidade: roteiros antigos com expressão | fala.
    linhas = [l.strip() for l in texto.splitlines()
              if l.strip() and not l.strip().startswith("#")]

    if linhas and all("|" in l for l in linhas):
        resultado = []
        for linha in linhas:
            expressao, fala = linha.split("|", 1)
            resultado.append((expressao.strip(), fala.strip()))
        return resultado

    trechos = dividir_texto(texto)
    resultado = []
    historico = []

    for trecho in trechos:
        expressao = escolher_expressao(trecho, historico)
        resultado.append((expressao, trecho))
        historico.append(trecho)

    return resultado
