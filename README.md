# Citizen Assist AI — Assistente Digital de Orientação ao Cidadão

**Global Solution 2026.2 | FIAP — Pensamento Computacional e Automação com Python**

## 1. Problema e proposta

Informações sobre serviços públicos estão distribuídas em diferentes portais e podem ser difíceis de entender. O Citizen Assist AI é um protótipo executado no terminal que organiza orientações em linguagem simples, pesquisa dúvidas por regras de pontuação e apresenta a fonte e a data de verificação.

**Público escolhido:** jovens e cidadãos que precisam localizar orientações básicas sobre saúde, trabalho, documentos, assistência social e direitos do consumidor.

**Problema:** dificuldade para encontrar rapidamente orientações confiáveis, entender documentos iniciais e identificar o canal público correto.

**ODS relacionados (alinhamento proposto):**
- ODS 3 — Saúde e Bem-Estar: acesso a informações sobre vacinação e serviços do SUS.
- ODS 8 — Trabalho Decente e Crescimento Econômico: acesso a informações trabalhistas.
- ODS 10 — Redução das Desigualdades: simplificação do acesso a informações e serviços.
- ODS 16 — Paz, Justiça e Instituições Eficazes: orientação sobre direitos e canais públicos.

## 2. Funcionalidades implementadas

- Leitura da base `data/base_conhecimento.json`.
- 12 orientações, distribuídas em 4 categorias.
- Três classes obrigatórias: `Orientacao`, `BaseConhecimento` e `Assistente`.
- Busca por texto livre com normalização de acentos, pontuação e caixa.
- Pontuação conforme o briefing: +3 por palavra-chave encontrada e +1 por palavra de 4 ou mais letras presente no título.
- Confiança ALTA (6 ou mais), MÉDIA (3 a 5) e sem resultado (menos de 3).
- Exibição de até duas alternativas com pontuação mínima 3.
- Navegação por categoria e opção 0 para voltar em todas as telas.
- Tratamento de entradas inválidas.
- Bloqueio de pergunta com 8 ou mais dígitos ou com `@`; a entrada bloqueada não é registrada.
- Histórico em JSON, indicadores e exportação CSV.
- Avaliação opcional de facilidade de uso de 1 a 5 ao sair.
- Tratamento de arquivo JSON ausente ou corrompido sem encerrar abruptamente.

## 3. Estrutura do projeto

```text
citizen-assist-ai/
├── README.md
├── main.py
├── orientacao.py
├── base_conhecimento.py
├── assistente.py
├── tests/
│   └── teste_basico.py
└── data/
    ├── base_conhecimento.json
    ├── historico.json
    └── atendimentos.csv
```

## 4. Como executar

Requisito: Python 3.10 ou superior. Não há bibliotecas externas obrigatórias.

No terminal, dentro da pasta do projeto:

```bash
python main.py
```

No Windows, se `python` não funcionar:

```powershell
py main.py
```

## 5. Como funciona a busca

1. `normalizar()` converte o texto para minúsculas, remove acentos e substitui pontuação por espaços.
2. `pontuar()` percorre as palavras-chave da orientação. Cada palavra-chave que aparece na pergunta soma 3 pontos.
3. Cada palavra da pergunta com 4 ou mais letras que aparece no título soma 1 ponto.
4. `buscar()` devolve uma lista de tuplas `(pontos, orientacao)`, ordenada da maior para a menor pontuação.
5. A maior pontuação define a confiança: ALTA ≥ 6; MÉDIA entre 3 e 5; abaixo de 3, o sistema informa que não encontrou.

**Exemplo didático:** a pergunta “Como faço o cartão do SUS?” pode pontuar pela expressão “cartao sus”, por “sus” e por palavras do título. O resultado exato é calculado pelo código, não fixado manualmente.

## 6. Orientação a Objetos e composição

- `Orientacao`: guarda os atributos de um registro e apresenta `exibir()`.
- `BaseConhecimento`: carrega o JSON, mantém uma lista de objetos `Orientacao`, lista categorias, filtra por categoria e executa a busca.
- `Assistente`: possui uma instância de `BaseConhecimento` no atributo `base`; conduz o atendimento, registra o histórico, calcula indicadores e exporta CSV.

A composição é: `Assistente → BaseConhecimento → lista de Orientacao`.

## 7. Privacidade, transparência e limitações

- O sistema não solicita nome, CPF, telefone ou e-mail.
- Entradas com 8 ou mais dígitos ou com `@` são recusadas e não são registradas.
- Não digite dados pessoais durante a demonstração.
- Cada orientação mostra fonte, data de verificação e o aviso “este assistente não é canal oficial”.
- A busca é baseada em regras, não é uma IA generativa e pode não entender sinônimos não cadastrados.
- O conteúdo não substitui atendimento, avaliação ou decisão do órgão público.
- Requisitos, documentos, endereços, horários e regras podem mudar. A equipe deve revisar as fontes antes da apresentação.
- O bloqueio é uma proteção básica para o escopo acadêmico, não um mecanismo completo de prevenção contra todos os dados pessoais.
- O histórico local armazena a pergunta digitada quando ela não é bloqueada. Não inclua informações pessoais nas perguntas.

## 8. Fontes oficiais consultadas

As páginas abaixo foram consultadas em **12/11/2026** para compor a base. A data no JSON indica a conferência realizada para este protótipo; a equipe deve revalidar antes da entrega final.

- [Ministério da Saúde — Calendário Nacional de Vacinação](https://www.gov.br/saude/pt-br/vacinacao/calendario)
- [Ministério da Saúde — Vacina na APS](https://www.gov.br/saude/pt-br/composicao/saps/vacina-na-aps)
- [Gov.br — Obter a Carteira de Trabalho](https://www.gov.br/pt-br/servicos/obter-a-carteira-de-trabalho)
- [Gov.br — Solicitar Seguro-Desemprego](https://www.gov.br/pt-br/servicos/solicitar-o-seguro-desemprego)
- [Gov.br — Criar conta gov.br](https://www.gov.br/pt-br/servicos/criar-sua-conta-gov.br)
- [Gov.br — Inscrever no CPF](https://www.gov.br/pt-br/servicos/inscrever-no-cpf)
- [Gov.br — Inscrever-se no Cadastro Único](https://www.gov.br/pt-br/servicos/inscrever-se-no-cadastro-unico-para-programas-sociais-do-governo-federal)
- [MJSP — Como registrar reclamação no Consumidor.gov.br](https://www.gov.br/mj/pt-br/assuntos/noticias/consumidor-gov-br-saiba-como-registrar-uma-reclamacao-pela-plataforma)
- [Gov.br — Obter passaporte comum](https://www.gov.br/pt-br/servicos/obter-passaporte-comum-para-brasileiro)

## 9. Testes técnicos

Execute os testes automatizados:

```bash
python -m unittest discover -s tests -v
```

Os testes verificam normalização, pontuação, categorias, bloqueio de dados pessoais, persistência do histórico e exportação CSV.

**Teste obrigatório com pessoas reais (a equipe precisa executar):**
- [ ] Testar com pelo menos 3 pessoas de fora da equipe.
- [ ] Somar pelo menos 10 atendimentos.
- [ ] Não registrar nomes, CPFs, telefones, e-mails ou outros dados das pessoas.
- [ ] Anotar os indicadores reais exibidos pelo programa.
- [ ] Registrar dúvidas sem solução.
- [ ] Fazer pelo menos uma melhoria baseada no teste (por exemplo, adicionar palavra-chave) e repetir a pergunta.

**Tabela para preencher com dados reais:**

| Indicador | Resultado do teste |
|---|---|
| Pessoas participantes | Preencher (mínimo 3) |
| Atendimentos | Preencher (mínimo 10) |
| Resposta encontrada (%) | Preencher após teste |
| Taxa de acerto (ajudou %) | Preencher após teste |
| Tempo médio | Preencher após teste |
| Tentativas por atendimento | Preencher após teste |
| Facilidade média (1 a 5) | Preencher após teste |
| Melhoria feita após feedback | Descrever |

Não invente resultados: os campos acima devem ser preenchidos somente depois do teste real.

## 10. Roteiro do vídeo técnico (5 a 8 minutos)

**A gravação deve ser feita pela equipe, com voz humana.** Todos os integrantes precisam falar. Não use narração de IA ou voz sintética.

1. **Equipe, público e problema (até 30 s):** apresentar o nome Citizen Assist AI, público escolhido e problema.
2. **JSON (45–60 s):** abrir `base_conhecimento.json`, explicar um dicionário, os campos obrigatórios, a lista e as palavras-chave.
3. **Classes (60–75 s):** mostrar as três classes, atributos, métodos, `self` e a composição.
4. **Busca (60–75 s):** explicar `normalizar()`, `pontuar()` e `buscar()`. Digitar uma pergunta real e demonstrar a soma dos pontos.
5. **Execução (60–75 s):** demonstrar uma resposta encontrada, uma não encontrada, entrada inválida, dado pessoal bloqueado (use apenas exemplo fictício e não registre) e navegação por categoria.
6. **Alteração ao vivo (30–45 s):** escolher uma orientação, adicionar uma palavra-chave no JSON, reiniciar o programa e mostrar uma pergunta que antes não era encontrada e agora é encontrada.
7. **Histórico, CSV e indicadores (45–60 s):** mostrar `historico.json`, exportar e abrir `atendimentos.csv`; apresentar os indicadores reais do teste.
8. **Decisão técnica e limitação (30–45 s):** explicar uma decisão (por exemplo, pontuação por regras) e uma limitação (sinônimos não cadastrados).

**Distribuição sugerida em trio:** integrante 1 — contexto, JSON e fontes; integrante 2 — classes e busca; integrante 3 — execução, histórico, indicadores e limitações. Em dupla ou individual, dividir os blocos igualmente.

## 11. Checklist final de entrega

- [ ] Revisar as 12 orientações e abrir cada link oficial.
- [ ] Rodar `python main.py` sem erros.
- [ ] Rodar os testes automatizados.
- [ ] Fazer o teste real com 3 pessoas e 10 atendimentos.
- [ ] Atualizar este README com os resultados reais e a melhoria implementada.
- [ ] Publicar o repositório público no GitHub.
- [ ] Gravar vídeo técnico de 5 a 8 minutos, não listado, com participação de todos.
- [ ] Inserir o link do vídeo neste README ou na entrega.
- [ ] Enviar no portal FIAP o `.txt` com nome do assistente, público, integrantes/RM, link do GitHub e link do vídeo.

## 12. Dados da equipe — preencher antes da entrega

- Integrantes e RM: **PREENCHER**
- Link do repositório: **PREENCHER**
- Link do vídeo: **PREENCHER**
