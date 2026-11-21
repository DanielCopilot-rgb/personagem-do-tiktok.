import unittest
from unittest.mock import patch

from gerador.story_maker import escrever


class TestStoryMaker(unittest.TestCase):

    def test_escrever_aceita_salvar_sem_dois_pontos(self):
        with patch("builtins.input", side_effect=["Minha primeira frase.", "salvar"]):
            resultado = escrever()

        self.assertEqual(resultado, "Minha primeira frase.")

    def test_escrever_aceita_cancelar_sem_dois_pontos(self):
        with patch("builtins.input", side_effect=["Texto que nao deve ser salvo.", "cancelar"]):
            resultado = escrever()

        self.assertIsNone(resultado)

    def test_escrever_mantem_comando_salvar_antigo(self):
        with patch("builtins.input", side_effect=["Texto valido.", ":salvar"]):
            resultado = escrever()

        self.assertEqual(resultado, "Texto valido.")


if __name__ == "__main__":
    unittest.main()
