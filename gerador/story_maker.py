import os
import re
import unicodedata
from pathlib import Path
from datetime import datetime

PASTA = Path(__file__).resolve().parent / "historias"
PASTA.mkdir(exist_ok=True)


def limpar_tela():
    os.system("clear")


def titulo():
    print("=" * 42)
    print("             STORY MAKER")
    print("          SEU ESTUDIO DE HISTORIAS")
    print("=" * 42)


def pausar():
    input("\nPressione ENTER para continuar...")


def criar_nome(texto):
    texto = unicodedata.normalize("NFD", texto.lower())
    texto = "".join(
        c for c in texto
        if unicodedata.category(c) != "Mn"
    )
    texto = re.sub(r"[^a-z0-9]+", "_", texto)
    return texto.strip("_") or "historia"


def arquivos():
    return sorted(PASTA.glob("*.txt"))


def carregar(caminho):
    texto = caminho.read_text(encoding="utf-8")
    linhas = texto.split("\n", 1)

    if linhas[0].startswith("# "):
        nome = linhas[0][2:]
        conteudo = linhas[1] if len(linhas) > 1 else ""
    else:
        nome = caminho.stem
        conteudo = texto

    return nome, conteudo


def salvar(nome, conteudo, caminho=None):
    if caminho is None:
        base = criar_nome(nome)
        caminho = PASTA / f"{base}.txt"
        numero = 2

        while caminho.exists():
            caminho = PASTA / f"{base}_{numero}.txt"
            numero += 1

    texto = f"# {nome}\n\n{conteudo.rstrip()}\n"
    caminho.write_text(texto, encoding="utf-8")
    return caminho


def escrever(conteudo_anterior=""):
    print("\n" + "-" * 42)
    print("ESCREVA SUA HISTORIA")
    print("-" * 42)
    print("Escreva livremente, usando varias linhas.")
    print("Digite salvar ou :salvar para terminar.")
    print("Digite cancelar ou :cancelar para desistir.\n")

    if conteudo_anterior:
        print("Conteudo anterior:")
        print(conteudo_anterior)
        print("\nReescreva a historia inteira abaixo.\n")

    linhas = []

    while True:
        try:
            linha = input()
        except (EOFError, KeyboardInterrupt):
            print("\nEscrita interrompida.")
            return None

        comando = linha.strip().casefold()

        if comando in {"salvar", ":salvar"}:
            return "\n".join(linhas).strip()

        if comando in {"cancelar", ":cancelar"}:
            return None

        linhas.append(linha)


def criar_historia():
    limpar_tela()
    titulo()
    print("\nNOVA HISTORIA\n")

    nome = input("Titulo: ").strip()

    if not nome:
        print("Voce precisa escolher um titulo.")
        pausar()
        return

    conteudo = escrever()

    if conteudo is None:
        print("Historia cancelada.")
        pausar()
        return

    if not conteudo:
        print("A historia esta vazia. Nada foi salvo.")
        pausar()
        return

    caminho = salvar(nome, conteudo)

    print(f"\nHistoria salva em: {caminho.name}")
    pausar()


def escolher_historia():
    lista = arquivos()

    if not lista:
        print("\nVoce ainda nao escreveu historias.")
        return None

    print("\nSUAS HISTORIAS\n")

    for i, caminho in enumerate(lista, 1):
        nome, conteudo = carregar(caminho)
        print(f"{i}. {nome}")

    try:
        escolha = int(input("\nNumero da historia (0 para voltar): "))

        if escolha == 0:
            return None

        if 1 <= escolha <= len(lista):
            return lista[escolha - 1]

    except ValueError:
        pass

    print("Escolha invalida.")
    return None


def listar_historias():
    limpar_tela()
    titulo()
    escolher_historia()
    pausar()


def abrir_historia():
    limpar_tela()
    titulo()
    caminho = escolher_historia()

    if caminho:
        nome, conteudo = carregar(caminho)
        print("\n" + "=" * 42)
        print(nome.upper())
        print("=" * 42)
        print(conteudo or "(Historia sem texto)")
    pausar()


def editar_historia():
    limpar_tela()
    titulo()
    caminho = escolher_historia()

    if not caminho:
        pausar()
        return

    nome, conteudo = carregar(caminho)

    print(f"\nEDITANDO: {nome}")
    novo_conteudo = escrever(conteudo)

    if novo_conteudo is None:
        print("Edicao cancelada.")
    elif not novo_conteudo:
        print("O texto esta vazio. A historia original foi preservada.")
    else:
        salvar(nome, novo_conteudo, caminho)
        print("Historia atualizada!")

    pausar()


def menu():
    while True:
        limpar_tela()
        titulo()

        print("\nMENU PRINCIPAL\n")
        print("1. Criar nova historia")
        print("2. Minhas historias")
        print("3. Ler uma historia")
        print("4. Editar uma historia")
        print("5. Sair")

        escolha = input("\nO que deseja fazer? ")

        if escolha == "1":
            criar_historia()
        elif escolha == "2":
            listar_historias()
        elif escolha == "3":
            abrir_historia()
        elif escolha == "4":
            editar_historia()
        elif escolha == "5":
            print("\nAte a proxima historia!")
            break
        else:
            print("\nOpcao invalida.")
            pausar()


if __name__ == "__main__":
    try:
        menu()
    except KeyboardInterrupt:
        print("\nPrograma encerrado.")
