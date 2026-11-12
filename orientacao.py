class Orientacao:
    """Representa uma orientação verificada da base de conhecimento."""

    def __init__(self, id, categoria, titulo, palavras_chave, resposta,
                 documentos, onde, fonte, verificado_em):
        self.id = id
        self.categoria = categoria
        self.titulo = titulo
        self.palavras_chave = palavras_chave
        self.resposta = resposta
        self.documentos = documentos
        self.onde = onde
        self.fonte = fonte
        self.verificado_em = verificado_em

    def exibir(self):
        """Exibe a orientação com transparência sobre fonte e limitações."""
        print("\n" + "=" * 68)
        print(f">> {self.titulo} [{self.categoria}]")
        print("-" * 68)
        print(self.resposta)
        print("\nDocumentos / informações que podem ser necessários:")
        for documento in self.documentos:
            print(f"  - {documento}")
        print(f"\nOnde: {self.onde}")
        print(f"Fonte oficial: {self.fonte}")
        print(f"Verificado em: {self.verificado_em}")
        print("Aviso: este assistente NÃO é um canal oficial.")
        print("Confirme requisitos, horários e disponibilidade no órgão responsável.")
        print("=" * 68)
