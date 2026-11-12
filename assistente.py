import csv
import json
import re
import time
from datetime import datetime
from pathlib import Path


class Assistente:
    """Controla a conversa, histórico, indicadores e exportação."""

    AVISO = "este assistente não é canal oficial"

    def __init__(self, nome, base, pasta_dados="data"):
        self.nome = nome
        self.base = base
        self.pasta_dados = Path(pasta_dados)
        self.pasta_dados.mkdir(parents=True, exist_ok=True)
        self.arquivo_historico = self.pasta_dados / "historico.json"
        self.arquivo_csv = self.pasta_dados / "atendimentos.csv"
        self.historico = self._carregar_historico()
        self.facilidade = []

    def _carregar_historico(self):
        try:
            with self.arquivo_historico.open("r", encoding="utf-8") as arquivo:
                dados = json.load(arquivo)
            return dados if isinstance(dados, list) else []
        except (OSError, json.JSONDecodeError):
            return []

    @staticmethod
    def contem_dado_pessoal(texto):
        """Bloqueia entradas com 8+ dígitos ou caractere @, conforme briefing."""
        digitos = re.sub(r"\D", "", texto)
        return len(digitos) >= 8 or "@" in texto

    @staticmethod
    def _entrada_sim_nao(mensagem):
        while True:
            resposta = input(mensagem).strip().lower()
            if resposta in ("s", "sim"):
                return True
            if resposta in ("n", "nao", "não"):
                return False
            print("Entrada inválida. Digite apenas s ou n.")

    def _salvar_historico(self):
        with self.arquivo_historico.open("w", encoding="utf-8") as arquivo:
            json.dump(self.historico, arquivo, ensure_ascii=False, indent=4)

    def registrar(self, origem, pergunta, orientacao_id, encontrou,
                  ajudou, tentativas, tempo):
        registro = {
            "data": datetime.now().isoformat(timespec="seconds"),
            "origem": origem,
            "pergunta": pergunta,
            "id_orientacao": orientacao_id,
            "encontrou": bool(encontrou),
            "ajudou": ajudou,
            "tentativas": int(tentativas),
            "tempo_segundos": round(float(tempo), 1)
        }
        self.historico.append(registro)
        self._salvar_historico()

    def perguntar(self):
        """Atende uma pergunta livre e registra somente entradas não sensíveis."""
        inicio = time.time()
        tentativas = 1
        while True:
            pergunta = input("\nDigite sua dúvida (0 para voltar): ").strip()
            if pergunta == "0":
                return
            if not pergunta:
                print("A pergunta não pode ficar vazia. Tente novamente.")
                tentativas += 1
                continue
            if self.contem_dado_pessoal(pergunta):
                print("Atenção: não digite CPF, telefone, e-mail ou outros dados pessoais.")
                print("Reescreva sua dúvida sem informações pessoais. Nada foi registrado.")
                tentativas += 1
                continue
            break

        resultados = self.base.buscar(pergunta)
        melhor_pontuacao, melhor = resultados[0] if resultados else (0, None)
        tempo = round(time.time() - inicio, 1)

        if melhor is None or melhor_pontuacao < 3:
            print("\nNão encontrei uma orientação com confiança suficiente.")
            print("Tente usar outras palavras ou navegar pelas categorias.")
            if resultados:
                sugestoes = [o.titulo for pontos, o in resultados[:2] if pontos > 0]
                if sugestoes:
                    print("Talvez você queira dizer: " + " | ".join(sugestoes))
            self.registrar("pergunta", pergunta, None, False, False,
                           tentativas, tempo)
            return

        confianca = "ALTA" if melhor_pontuacao >= 6 else "MÉDIA"
        print(f"\nConfiança da resposta: {confianca} ({melhor_pontuacao} pontos)")
        melhor.exibir()
        alternativas = [(p, o) for p, o in resultados[1:3] if p >= 3]
        if alternativas:
            print("\nOutras orientações que podem ajudar:")
            for pontos, orientacao in alternativas:
                print(f"  - {orientacao.titulo} ({pontos} pontos)")
        ajudou = self._entrada_sim_nao("\nEssa orientação respondeu sua dúvida? (s/n): ")
        self.registrar("pergunta", pergunta, melhor.id, True, ajudou,
                       tentativas, tempo)

    def navegar(self):
        """Navegação por categorias, com opção 0 em todas as telas."""
        categorias = self.base.categorias()
        if not categorias:
            print("Não há categorias disponíveis.")
            return
        while True:
            print("\n--- CATEGORIAS ---")
            for indice, categoria in enumerate(categorias, start=1):
                print(f"{indice}. {categoria}")
            print("0. Voltar")
            escolha = input("Escolha uma categoria: ").strip()
            if escolha == "0":
                return
            if not escolha.isdigit() or not (1 <= int(escolha) <= len(categorias)):
                print("Opção inválida. Tente novamente.")
                continue
            categoria = categorias[int(escolha) - 1]
            orientacoes = self.base.por_categoria(categoria)
            while True:
                print(f"\n--- {categoria.upper()} ---")
                for indice, orientacao in enumerate(orientacoes, start=1):
                    print(f"{indice}. {orientacao.titulo}")
                print("0. Voltar")
                opcao = input("Escolha uma orientação: ").strip()
                if opcao == "0":
                    break
                if not opcao.isdigit() or not (1 <= int(opcao) <= len(orientacoes)):
                    print("Opção inválida. Tente novamente.")
                    continue
                inicio = time.time()
                orientacao = orientacoes[int(opcao) - 1]
                orientacao.exibir()
                ajudou = self._entrada_sim_nao("Essa orientação respondeu sua dúvida? (s/n): ")
                self.registrar("categoria", f"Consulta por categoria: {categoria}",
                               orientacao.id, True, ajudou, 1,
                               round(time.time() - inicio, 1))

    def indicadores(self):
        total = len(self.historico)
        if total == 0:
            print("\nAinda não há atendimentos registrados.")
            return
        encontrados = sum(1 for r in self.historico if r["encontrou"])
        avaliados = [r for r in self.historico if r["ajudou"] is not None]
        ajudaram = sum(1 for r in avaliados if r["ajudou"])
        tempo_medio = sum(r["tempo_segundos"] for r in self.historico) / total
        tentativas_media = sum(r["tentativas"] for r in self.historico) / total
        print("\n========== INDICADORES ==========")
        print(f"Atendimentos registrados: {total}")
        print(f"Resposta encontrada: {encontrados / total * 100:.1f}%")
        if avaliados:
            print(f"Taxa de acerto (ajudou): {ajudaram / len(avaliados) * 100:.1f}%")
        else:
            print("Taxa de acerto: sem avaliações")
        print(f"Tempo médio para encontrar: {tempo_medio:.1f} s")
        print(f"Tentativas por atendimento: {tentativas_media:.2f}")
        if self.facilidade:
            print(f"Facilidade de uso (1 a 5): {sum(self.facilidade)/len(self.facilidade):.2f}")
        else:
            print("Facilidade de uso: ainda sem avaliações de saída")
        sem_solucao = [r for r in self.historico if not r["encontrou"]]
        print("Dúvidas sem solução:")
        if sem_solucao:
            for registro in sem_solucao:
                print(f"  - {registro['pergunta']}")
        else:
            print("  Nenhuma registrada.")

    def exportar_csv(self):
        campos = ["data", "origem", "pergunta", "id_orientacao", "encontrou",
                  "ajudou", "tentativas", "tempo_segundos"]
        with self.arquivo_csv.open("w", newline="", encoding="utf-8-sig") as arquivo:
            escritor = csv.DictWriter(arquivo, fieldnames=campos)
            escritor.writeheader()
            escritor.writerows(self.historico)
        print(f"CSV exportado em: {self.arquivo_csv}")

    def executar(self):
        print(f"\n{'=' * 58}\nBem-vindo ao {self.nome}!\nOrientação cidadã com fontes verificadas.\n{'=' * 58}")
        while True:
            print("\n1. Fazer uma pergunta")
            print("2. Navegar por categorias")
            print("3. Ver indicadores")
            print("4. Exportar atendimentos para CSV")
            print("0. Sair")
            opcao = input("Escolha: ").strip()
            if opcao == "1":
                self.perguntar()
            elif opcao == "2":
                self.navegar()
            elif opcao == "3":
                self.indicadores()
            elif opcao == "4":
                self.exportar_csv()
            elif opcao == "0":
                self._avaliar_facilidade()
                self.indicadores()
                self.exportar_csv()
                print("\nObrigado por utilizar. Consulte sempre os canais oficiais.")
                break
            else:
                print("Opção inválida. Digite uma opção do menu.")

    def _avaliar_facilidade(self):
        while True:
            nota = input("\nDe 1 a 5, qual foi a facilidade de uso? (0 para pular): ").strip()
            if nota == "0":
                return
            if nota in {"1", "2", "3", "4", "5"}:
                self.facilidade.append(int(nota))
                return
            print("Nota inválida. Digite um número de 1 a 5 ou 0 para pular.")
