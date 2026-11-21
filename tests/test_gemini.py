import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from gerador.gemini import obter_chave_api, validar_analise


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


class TestValidacaoGemini(unittest.TestCase):

    def test_aceita_cena_valida(self):
        analise = {
            'cenas': [{'texto': 'Olá!', 'expressao': 'sorriso_fechado'}]
        }
        self.assertEqual(validar_analise(analise), analise)

    def test_substitui_expressao_desconhecida(self):
        analise = {'cenas': [{'texto': 'Olá!', 'expressao': 'expressao_inexistente'}]}
        resultado = validar_analise(analise)
        self.assertEqual(resultado['cenas'][0]['expressao'], 'sorriso_fechado')

    def test_rejeita_resposta_que_nao_e_objeto(self):
        with self.assertRaisesRegex(RuntimeError, 'objeto JSON'):
            validar_analise([])

    def test_rejeita_cena_sem_texto(self):
        with self.assertRaisesRegex(RuntimeError, 'texto válido'):
            validar_analise({'cenas': [{'expressao': 'sorriso_fechado'}]})


if __name__ == '__main__':
    unittest.main()
