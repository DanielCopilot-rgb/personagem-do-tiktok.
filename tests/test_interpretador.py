import unittest
import tempfile
from pathlib import Path

from gerador.interpretador import (
    normalizar,
    dividir_texto,
    escolher_expressao,
    interpretar_roteiro,
)


class TestInterpretador(unittest.TestCase):

    def test_normalizar_remove_acentos_e_maiusculas(self):
        self.assertEqual(normalizar("INCRÍVEL"), "incrivel")

    def test_dividir_texto_separa_frases(self):
        resultado = dividir_texto("Olá! Tudo bem? Vamos começar.")
        self.assertEqual(
            resultado,
            ["Olá!", "Tudo bem?", "Vamos começar."]
        )

    def test_escolher_expressao_detecta_cansaco(self):
        resultado = escolher_expressao("Estou cansado hoje.", [])
        self.assertEqual(resultado, "cansado_olhos_fechados")

    def test_escolher_expressao_detecta_alegria(self):
        resultado = escolher_expressao("Estou feliz!", [])
        self.assertEqual(resultado, "feliz_olhos_fechados")

    def test_escolher_expressao_detecta_humor(self):
        resultado = escolher_expressao("Hahaha, que engraçado!", [])
        self.assertEqual(resultado, "riso_boca_aberta")

    def test_escolher_expressao_usa_contexto(self):
        resultado = escolher_expressao(
            "O que será que aconteceu?",
            ["Havia um mistério no corredor."]
        )
        self.assertEqual(resultado, "serio_boca_reta")

    def test_roteiro_antigo(self):
        conteudo = (
            "sorriso_fechado | Olá!\n"
            "serio_boca_reta | Precisamos conversar."
        )

        with tempfile.TemporaryDirectory() as pasta:
            arquivo = Path(pasta) / "roteiro.txt"
            arquivo.write_text(conteudo, encoding="utf-8")

            resultado = interpretar_roteiro(arquivo)

        self.assertEqual(
            resultado,
            [
                ("sorriso_fechado", "Olá!"),
                ("serio_boca_reta", "Precisamos conversar."),
            ]
        )

    def test_texto_livre(self):
        conteudo = "Estou feliz! Hoje consegui terminar o trabalho."

        with tempfile.TemporaryDirectory() as pasta:
            arquivo = Path(pasta) / "historia.txt"
            arquivo.write_text(conteudo, encoding="utf-8")

            resultado = interpretar_roteiro(arquivo)

        self.assertEqual(len(resultado), 2)
        self.assertEqual(resultado[0][0], "feliz_olhos_fechados")
        self.assertEqual(resultado[0][1], "Estou feliz!")


if __name__ == "__main__":
    unittest.main()
