# Citizen Assist AI — Assistente Digital de Orientação ao Cidadão

**Global Solution 2026.2 · FIAP · Pensamento Computacional e Automação com Python**  
Desafio **CitizenTech**

O Citizen Assist AI é um assistente de terminal desenvolvido em Python puro, sem bibliotecas externas, que ajuda cidadãos a encontrar orientações sobre saúde, trabalho, documentos, assistência social e direitos do consumidor.

As respostas utilizam informações de fontes oficiais, apresentam a data de verificação e incluem avisos sobre as limitações do sistema. O programa também protege dados pessoais, evitando registrar perguntas que contenham possíveis informações sensíveis.

## 1. Integrante

| Nome | RM |
|---|---|
| Kayo Henderson | 570706 |

Projeto desenvolvido individualmente.

## 2. Público e problema

O projeto atende jovens e cidadãos que encontram dificuldades para localizar informações sobre serviços públicos, documentos e direitos.

A proposta é centralizar orientações em linguagem simples, permitindo buscas por texto livre ou navegação por categorias.

## 3. ODS relacionados

- **ODS 3:** Saúde e Bem-Estar.
- **ODS 8:** Trabalho Decente e Crescimento Econômico.
- **ODS 10:** Redução das Desigualdades.
- **ODS 16:** Paz, Justiça e Instituições Eficazes.

## 4. Funcionalidades

- Base de conhecimento armazenada em JSON.
- 12 orientações distribuídas em 4 categorias.
- Busca por texto livre com normalização de palavras.
- Sistema de pontuação e níveis de confiança: ALTA e MÉDIA.
- Sugestão de orientações alternativas.
- Navegação por categorias.
- Proteção contra entradas inválidas e dados pessoais.
- Histórico de atendimentos em JSON.
- Indicadores de desempenho e facilidade de uso.
- Exportação de atendimentos para CSV.
- Tratamento de arquivos ausentes ou corrompidos.
- Exibição de fontes oficiais e datas de verificação.

## 5. Como executar

**Requisito:** Python 3.10 ou superior.

Na pasta principal do projeto, execute:

```bash
python main.py
```

No Windows, também é possível utilizar:

```powershell
py main.py
```

### Menu principal

1. Fazer uma pergunta.
2. Navegar por categorias.
3. Ver indicadores.
4. Exportar atendimentos para CSV.
0. Sair.

## 6. Estrutura do projeto

```text
citizen-assist-ai/
├── main.py
├── orientacao.py
├── base_conhecimento.py
├── assistente.py
├── README.md
├── tests/
│   └── teste_basico.py
└── data/
    ├── base_conhecimento.json
    ├── historico.json
    └── atendimentos.csv
```

## 7. Arquitetura

O sistema utiliza três classes principais:

- **Orientacao:** armazena e apresenta as informações.
- **BaseConhecimento:** carrega o JSON, organiza categorias e realiza as buscas.
- **Assistente:** controla a interação com o cidadão, registra atendimentos e calcula indicadores.

A arquitetura utiliza composição entre as classes.

## 8. Sistema de busca

A busca funciona por regras e pontuação, sem utilizar inteligência artificial generativa.

O sistema normaliza os textos, removendo acentos, pontuação e diferenças entre letras maiúsculas e minúsculas.

| Critério | Pontuação |
|---|---:|
| Palavra-chave encontrada | +3 |
| Palavra do título encontrada | +1 |

**Níveis de confiança:**
- 6 pontos ou mais: ALTA.
- 3 a 5 pontos: MÉDIA.
- Menos de 3 pontos: orientação não encontrada.

## 9. Privacidade e transparência

O sistema não solicita nome, CPF, telefone ou e-mail.

Perguntas contendo 8 ou mais dígitos ou o caractere `@` são bloqueadas e não registradas.

Todas as orientações apresentam fonte oficial, data de verificação e o aviso de que o assistente não representa nenhum órgão público.

## 10. Histórico e indicadores

Os atendimentos são armazenados em JSON e podem ser exportados para CSV.

O sistema calcula:
- Percentual de respostas encontradas.
- Taxa de acerto.
- Tempo médio de atendimento.
- Média de tentativas.
- Facilidade de uso.
- Dúvidas não solucionadas.

## 11. Testes automatizados

Os testes utilizam a biblioteca `unittest` do Python.

Para executar:

```bash
python -m unittest discover -s tests -v
```

São verificados a normalização, a pontuação, as categorias, a proteção de dados pessoais e a exportação CSV.

## 12. Teste com usuários

O projeto prevê testes com pelo menos 3 pessoas externas, totalizando 10 atendimentos ou mais.

Os resultados devem ser preenchidos com dados reais, incluindo taxa de acerto, tempo médio, facilidade de uso e melhorias realizadas.

## 13. Decisões técnicas e limitações

A escolha por busca baseada em regras permite resultados previsíveis e explicáveis, utilizando apenas Python e suas bibliotecas padrão.

Entre as limitações estão:
- Dependência de palavras-chave cadastradas.
- Dificuldade para interpretar sinônimos e erros de digitação.
- Base limitada a 12 orientações.
- Necessidade de atualização periódica das informações.
- Proteção de dados pessoais baseada em regras simples.

## 14. Fontes oficiais

As informações foram consultadas em portais oficiais em **12/11/2026**, incluindo:

- Ministério da Saúde.
- Gov.br.
- Ministério da Justiça e Segurança Pública.
- Consumidor.gov.br.

## 15. Vídeo técnico e repositório

**Vídeo no YouTube:** _PREENCHER_  
**Repositório GitHub:** _PREENCHER_

O vídeo deve apresentar a proposta, a base JSON, as classes, o sistema de busca, a execução, os testes, o histórico e uma demonstração de melhoria na base de conhecimento.

---

*Projeto acadêmico da FIAP — Global Solution 2026.2. Protótipo educacional que não substitui os canais oficiais de atendimento público.*
