import json
import tempfile
import unittest
from pathlib import Path

from base_conhecimento import BaseConhecimento
from assistente import Assistente


class TesteCitizenAssist(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.pasta = Path(self.temp.name)
        self.arquivo = self.pasta / "base.json"
        self.arquivo.write_text(json.dumps([
            {
                "id": 1, "categoria": "Saúde", "titulo": "Consultar Cartão SUS",
                "palavras_chave": ["cartao do sus", "cartao sus", "sus", "cns"],
                "resposta": "Procure a UBS.", "documentos": ["Documento"],
                "onde": "UBS", "fonte": "https://www.gov.br/saude",
                "verificado_em": "2026-11-12"
            }
        ], ensure_ascii=False), encoding="utf-8")
        self.base = BaseConhecimento(self.arquivo)
        self.base.carregar()

    def tearDown(self):
        self.temp.cleanup()

    def test_normalizacao(self):
        self.assertEqual(self.base.normalizar("CARTÃO, SUS!"), " cartao sus ")

    def test_busca_e_pontuacao(self):
        resultados = self.base.buscar("Como faço o cartão do SUS?")
        self.assertGreaterEqual(resultados[0][0], 6)
        self.assertEqual(resultados[0][1].id, 1)

    def test_categorias(self):
        self.assertEqual(self.base.categorias(), ["Saúde"])

    def test_bloqueio_dados_pessoais(self):
        self.assertTrue(Assistente.contem_dado_pessoal("meu contato 12345678"))
        self.assertTrue(Assistente.contem_dado_pessoal("meu email teste@exemplo.com"))
        self.assertFalse(Assistente.contem_dado_pessoal("onde fica a UBS?"))

    def test_registro_e_csv(self):
        app = Assistente("Teste", self.base, self.pasta / "data")
        app.registrar("pergunta", "onde fica a UBS?", 1, True, True, 1, 1.2)
        app.exportar_csv()
        self.assertTrue((self.pasta / "data" / "historico.json").exists())
        self.assertTrue((self.pasta / "data" / "atendimentos.csv").exists())


if __name__ == "__main__":
    unittest.main()
