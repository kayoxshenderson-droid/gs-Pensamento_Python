import json
import re
import unicodedata
from pathlib import Path

from orientacao import Orientacao


class BaseConhecimento:
    """Carrega, organiza e pesquisa as orientações do arquivo JSON."""

    def __init__(self, caminho):
        self.caminho = Path(caminho)
        self.orientacoes = []

    @staticmethod
    def normalizar(texto):
        texto = str(texto).lower().strip()
        texto = unicodedata.normalize("NFD", texto)
        texto = "".join(c for c in texto if unicodedata.category(c) != "Mn")
        texto = re.sub(r"[^a-z0-9]+", " ", texto)
        return " " + " ".join(texto.split()) + " "

    def carregar(self):
        """Lê o JSON e converte cada dicionário em um objeto Orientacao."""
        try:
            with self.caminho.open("r", encoding="utf-8") as arquivo:
                dados = json.load(arquivo)
            if not isinstance(dados, list):
                raise ValueError("A raiz do JSON precisa ser uma lista.")
            obrigatorios = {
                "id", "categoria", "titulo", "palavras_chave", "resposta",
                "documentos", "onde", "fonte", "verificado_em"
            }
            carregadas = []
            for indice, item in enumerate(dados, start=1):
                if not isinstance(item, dict):
                    raise ValueError(f"Registro {indice} não é um objeto.")
                faltantes = obrigatorios - item.keys()
                if faltantes:
                    raise ValueError(
                        f"Registro {indice} sem campos: {', '.join(sorted(faltantes))}"
                    )
                if not isinstance(item["palavras_chave"], list) or len(item["palavras_chave"]) < 3:
                    raise ValueError(f"Registro {indice} precisa de 3 palavras-chave.")
                if not isinstance(item["documentos"], list):
                    raise ValueError(f"Campo documentos inválido no registro {indice}.")
                carregadas.append(Orientacao(**item))
            self.orientacoes = carregadas
            return True
        except (OSError, json.JSONDecodeError, TypeError, ValueError) as erro:
            self.orientacoes = []
            print(f"\n[AVISO] Não foi possível carregar a base: {erro}")
            print("O programa continuará funcionando, mas sem orientações disponíveis.")
            return False

    def categorias(self):
        return sorted({o.categoria for o in self.orientacoes})

    def por_categoria(self, categoria):
        return [o for o in self.orientacoes if o.categoria == categoria]

    def pontuar(self, pergunta, orientacao):
        """
        Regra do briefing:
        +3 por palavra-chave encontrada na pergunta;
        +1 por palavra da pergunta (4+ letras) encontrada no título.
        """
        pergunta_norm = self.normalizar(pergunta)
        titulo_norm = self.normalizar(orientacao.titulo)
        pontos = 0
        for chave in orientacao.palavras_chave:
            chave_norm = self.normalizar(chave).strip()
            if chave_norm and f" {chave_norm} " in pergunta_norm:
                pontos += 3
        palavras = set(pergunta_norm.split())
        palavras.discard("")
        titulo_palavras = set(titulo_norm.split())
        pontos += sum(1 for palavra in palavras
                      if len(palavra) >= 4 and palavra in titulo_palavras)
        return pontos

    def buscar(self, pergunta):
        resultados = [
            (self.pontuar(pergunta, orientacao), orientacao)
            for orientacao in self.orientacoes
        ]
        return sorted(resultados, key=lambda item: item[0], reverse=True)
