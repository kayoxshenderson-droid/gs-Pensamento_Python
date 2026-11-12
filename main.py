from pathlib import Path

from base_conhecimento import BaseConhecimento
from assistente import Assistente


def main():
    # Usa a pasta do próprio projeto, sem exigir que o usuário crie uma pasta data.
    pasta_projeto = Path(__file__).resolve().parent
    caminho_base = pasta_projeto / "base_conhecimento.json"

    base = BaseConhecimento(caminho_base)
    if not base.carregar():
        raise SystemExit("Não foi possível iniciar: confira o arquivo base_conhecimento.json.")

    assistente = Assistente("Citizen Assist AI", base, pasta_projeto / "data")
    assistente.executar()


if __name__ == "__main__":
    main()
