from base_conhecimento import BaseConhecimento
from assistente import Assistente


def main():
    base = BaseConhecimento("data/base_conhecimento.json")
    base.carregar()
    assistente = Assistente("Citizen Assist AI", base)
    assistente.executar()


if __name__ == "__main__":
    main()
