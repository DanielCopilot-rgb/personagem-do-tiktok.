import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from gerador.gemini import obter_chave_api


class TestChaveGemini(unittest.TestCase):

    def test_variavel_de_ambiente_tem_prioridade(self):
        with tempfile.TemporaryDirectory() as pasta:
            arquivo = Path(pasta) / '.gemini_env'
            arquivo.write_text('GEMINI_API_KEY=chave-arquivo\n', encoding='utf-8')
            with patch.dict(os.environ, {'GEMINI_API_KEY': 'chave-ambiente'}):
                self.assertEqual(obter_chave_api(arquivo), 'chave-ambiente')

    def test_carrega_formato_export_com_aspas(self):
        with tempfile.TemporaryDirectory() as pasta:
            arquivo = Path(pasta) / '.gemini_env'
            arquivo.write_text(
                '# comentário\nexport GEMINI_API_KEY="chave-teste"\n',
                encoding='utf-8'
            )
            with patch.dict(os.environ, {}, clear=True):
                self.assertEqual(obter_chave_api(arquivo), 'chave-teste')

    def test_arquivo_sem_chave_retorna_none(self):
        with tempfile.TemporaryDirectory() as pasta:
            arquivo = Path(pasta) / '.gemini_env'
            arquivo.write_text('OUTRA_VARIAVEL=valor\n', encoding='utf-8')
            with patch.dict(os.environ, {}, clear=True):
                self.assertIsNone(obter_chave_api(arquivo))

    def test_arquivo_inexistente_retorna_none(self):
        with tempfile.TemporaryDirectory() as pasta:
            arquivo = Path(pasta) / 'inexistente.env'
            with patch.dict(os.environ, {}, clear=True):
                self.assertIsNone(obter_chave_api(arquivo))


if __name__ == '__main__':
    unittest.main()
