# Guia Completo dos Scripts Python - Análise de Spreads

Este documento explica de forma detalhada e em linguagem simples o que cada arquivo Python deste projeto faz. É voltado para pessoas que não têm conhecimento técnico avançado em programação.

---

## Índice

1. [Visão Geral do Projeto](#visão-geral-do-projeto)
2. [carregar_dados_formato_planilha_spread.py](#carregar_dados_formato_planilha_spreadpy)
3. [calcular_spreads.py](#calcular_spreadspy)
4. [Ordem de Execução](#ordem-de-execução)
5. [Arquivos Gerados](#arquivos-gerados)
6. [Dicas e Observações](#dicas-e-observações)
7. [Perguntas Frequentes](#perguntas-frequentes)
8. [Recursos e Links Úteis](#recursos-e-links-úteis)
9. [Suporte](#suporte)

---

## Visão Geral do Projeto

Este projeto analisa **spreads** entre diferentes tipos de ações de empresas brasileiras. 

**O que é um spread?** 
Imagine que uma empresa tem dois tipos de ações: Ação Tipo 3 e Ação Tipo 4. O spread é a diferença de preço entre essas duas ações no mesmo dia. Se a Ação 3 custa R$ 10,00 e a Ação 4 custa R$ 9,50, o spread é de R$ 0,50.

**Por que isso é importante?**
Investidores podem aproveitar essas diferenças de preço para fazer operações de arbitragem (comprar a mais barata e vender a mais cara, lucrando com a diferença).

**Empresas analisadas:**
- **Itausa** (ITSA3 vs ITSA4)
- **Bradesco** (BBDC3 vs BBDC4)
- **Petrobras** (PETR3 vs PETR4)
- **Santander** (SANB3 + SANB4 vs SANB11)

---

## carregar_dados_formato_planilha_spread.py

### O que este script faz?

Este script é como um **"coletor de dados"**. Ele pega informações brutas da Bolsa de Valores (B3) e organiza tudo em um arquivo único e limpo para análise.

### Passo a Passo Detalhado:

#### **ETAPA 1: Identificar quais ações buscar**
- O script sabe quais ações precisa buscar baseado na planilha de referência
- Ele procura por:
  - **ITSA3** e **ITSA4** (Itausa)
  - **BBDC3** e **BBDC4** (Bradesco)
  - **SANB3**, **SANB4** e **SANB11** (Santander)

#### **ETAPA 2: Carregar arquivo da B3**
- A B3 disponibiliza um arquivo gigante (COTAHIST_A2025.TXT) com dados de TODAS as ações negociadas
- Este arquivo pode ter milhões de linhas e vários megabytes
- O script lê esse arquivo usando uma ferramenta especial chamada `b3fileparser`
- **Atenção:** Se você não tiver essa ferramenta instalada, o script vai avisar e pedir para instalar com: `pip install b3fileparser`

#### **ETAPA 3: Filtrar apenas as ações que precisamos**
- O arquivo da B3 tem dados de TODAS as empresas
- O script filtra e pega APENAS os dados das ações que nos interessam (Itausa, Bradesco, Santander)
- É como pegar uma lista telefônica gigante e copiar apenas os números que você precisa

#### **ETAPA 4: Organizar os dados**
- Os dados da B3 vêm com nomes de colunas complicados como "CODIGO_DE_NEGOCIACAO" e "PRECO_MAXIMO"
- O script renomeia tudo para nomes mais simples como "Ticker" e "Maxima"
- Também organiza as informações importantes:
  - Código da ação (Ticker)
  - Data da negociação
  - Preço de abertura
  - Preço máximo do dia
  - Preço mínimo do dia
  - Preço de fechamento
  - Volume negociado (quantidade e valor em reais)
  - Número de negociações

#### **ETAPA 5: Criar um arquivo unificado**
- O script junta todos os dados filtrados em um único arquivo chamado "dataset_unificado"
- É como juntar várias planilhas em uma só

#### **ETAPA 6: Salvar o resultado**
- O script salva tudo em um arquivo CSV (formato de planilha) chamado `dataset_unificado.csv`
- Também tenta salvar em formato Parquet (mais eficiente, mas opcional)
- O arquivo fica salvo em: `data_b3/dataset_unificado.csv`

### Resumo Simples:
**Este script transforma um arquivo gigante e confuso da B3 em um arquivo limpo e organizado com apenas os dados que precisamos.**

### O que você precisa antes de executar?
1. Ter o arquivo `COTAHIST_A2025.TXT` na pasta `data_b3/`
   - **Onde baixar:** Você pode baixar os arquivos históricos de cotações da B3 no site oficial: [Historical Quotes - B3](https://www.b3.com.br/en_us/market-data-and-indices/data-services/market-data/historical-data/equities/historical-quotes/)
   - O arquivo COTAHIST contém dados históricos de todas as ações negociadas na bolsa
2. Ter instalado: `b3fileparser` (instale com: `pip install b3fileparser`)
3. Opcional: `pyarrow` para salvar em formato Parquet (instale com: `pip install pyarrow`)

### Como executar?
```bash
python carregar_dados_formato_planilha_spread.py
```

---

## calcular_spreads.py

### O que este script faz?

Este script é o **"calculador de spreads"**. Ele pega o arquivo limpo criado pelo script anterior e calcula as diferenças de preço entre as ações, gerando relatórios e estatísticas.

### Passo a Passo Detalhado:

#### **ETAPA 1: Carregar o dataset unificado**
- O script abre o arquivo `dataset_unificado.csv` criado pelo script anterior
- Verifica se o arquivo existe (se não existir, avisa que precisa executar o primeiro script primeiro)
- Mostra quantos registros tem, quais ações estão presentes e qual o período dos dados

#### **ETAPA 2: Calcular Spread Itausa (ITSA3 vs ITSA4)**
- Para cada dia, o script:
  1. Pega o preço máximo da ITSA3
  2. Pega o preço máximo da ITSA4
  3. Calcula a diferença entre eles (em reais e em percentual)
  4. Identifica qual ação teve o maior preço naquele dia
  5. Cria uma tabela com todas essas informações

**Exemplo prático:**
- Dia 20/01/2025: ITSA3 = R$ 9,34 | ITSA4 = R$ 9,24
- Diferença: R$ 0,10 (1,08%)
- Resultado: "3 Maior" (ITSA3 foi mais cara)

#### **ETAPA 3: Calcular Spread Bradesco (BBDC3 vs BBDC4)**
- Faz a mesma coisa, mas para as ações do Bradesco
- Compara BBDC3 com BBDC4 dia a dia

#### **ETAPA 4: Calcular Spread Petrobras (PETR3 vs PETR4)**
- Compara PETR3 com PETR4
- Calcula as diferenças de preço

#### **ETAPA 5: Calcular Spread Santander ((SANB3 + SANB4) vs SANB11)**
- Este é um pouco diferente:
  - Soma o preço de SANB3 + SANB4
  - Compara essa soma com o preço de SANB11 (que é uma ação unitária)
  - Isso porque 1 ação SANB11 equivale a 1 SANB3 + 1 SANB4

**Exemplo prático:**
- SANB3 = R$ 11,91 | SANB4 = R$ 13,26 | Soma = R$ 25,17
- SANB11 = R$ 25,18
- Diferença: R$ 0,01 (0,04%)
- Resultado: "11 Maior" (SANB11 foi ligeiramente mais cara)

#### **ETAPA 6: Adicionar Thresholds (Limiares)**
- O script cria "marcadores" para identificar quando o spread é significativo
- Por exemplo, marca com "sim" ou "não" se o spread é maior que:
  - R$ 0,10
  - R$ 0,15
  - R$ 0,20
  - R$ 0,30
  - E assim por diante (cada empresa tem thresholds diferentes)
- Isso ajuda a identificar rapidamente dias com spreads interessantes para operação

**Exemplo:**
- Se o spread é R$ 0,25, então:
  - `>_0.10R$` = "sim" (é maior que R$ 0,10)
  - `>_0.15R$` = "sim" (é maior que R$ 0,15)
  - `>_0.20R$` = "sim" (é maior que R$ 0,20)
  - `>_0.30R$` = "não" (não é maior que R$ 0,30)

#### **ETAPA 7: Calcular Estatísticas**
- Para cada spread calculado, o script gera estatísticas:
  - **Média:** Qual a diferença percentual média entre as ações
  - **Mínima:** Qual foi a menor diferença encontrada
  - **Máxima:** Qual foi a maior diferença encontrada
  - **Mais comum:** Qual ação geralmente é mais cara
  - **Contadores:** Quantos dias tiveram spread maior que R$ 0,10, R$ 0,15, etc.

**Exemplo de estatísticas:**
```
SPREAD ITAUSA (ITSA3 vs ITSA4):
  Média: 0.84%
  Mínima: 0.00%
  Máxima: 5.13%
  Qual maior mais comum: 3 Maior (ITSA3 geralmente é mais cara)
  
  Spread > R$ 0,10: 73 dias (29,20% dos dias)
  Spread > R$ 0,15: 56 dias (22,40% dos dias)
```

#### **ETAPA 8: Gerar Relatório de Spreads > R$ 0,10**
- Cria um arquivo markdown (`relatorio_spreads_maior_010.md`) com:
  - Ranking dos ativos por quantidade de spreads significativos
  - Tabela comparativa
  - Detalhamento de cada ativo

#### **ETAPA 9: Gerar Relatório do Dataset**
- Cria um arquivo markdown (`data_b3/relatorio_dataset.md`) com:
  - Estatísticas gerais do dataset
  - Informações de cada ativo (preços, volumes, etc.)
  - **Ordenado por quantidade de spreads > R$ 0,10** (os ativos com mais oportunidades aparecem primeiro)

### Resumo Simples:
**Este script pega os dados organizados, calcula as diferenças de preço entre ações relacionadas, identifica oportunidades e gera relatórios fáceis de entender.**

### O que você precisa antes de executar?
1. Ter executado o script `carregar_dados_formato_planilha_spread.py` primeiro
2. Ter o arquivo `dataset_unificado.csv` na pasta `data_b3/`

### Como executar?
```bash
python calcular_spreads.py
```

---

## Ordem de Execução

**IMPORTANTE:** Os scripts devem ser executados nesta ordem:

1. **Primeiro:** Execute `carregar_dados_formato_planilha_spread.py`
   - Isso cria o arquivo `dataset_unificado.csv`
   
2. **Depois:** Execute `calcular_spreads.py`
   - Isso usa o arquivo criado no passo 1
   - Se você tentar executar este primeiro, ele vai dar erro dizendo que o dataset não existe

### Fluxo Visual:

```
┌─────────────────────────────────────────┐
│  COTAHIST_A2025.TXT (arquivo da B3)    │
│  (arquivo gigante com todos os dados)   │
└──────────────┬──────────────────────────┘
               │
               │ carregar_dados_formato_planilha_spread.py
               │ (filtra e organiza)
               ▼
┌─────────────────────────────────────────┐
│  dataset_unificado.csv                 │
│  (arquivo limpo e organizado)          │
└──────────────┬──────────────────────────┘
               │
               │ calcular_spreads.py
               │ (calcula diferenças e gera relatórios)
               ▼
┌─────────────────────────────────────────┐
│  relatorio_spreads_maior_010.md        │
│  relatorio_dataset.md                   │
│  (relatórios em formato markdown)       │
└─────────────────────────────────────────┘
```

---

## Arquivos Gerados

### Por `carregar_dados_formato_planilha_spread.py`:
- **`data_b3/dataset_unificado.csv`**: Arquivo principal com todos os dados organizados
- **`data_b3/dataset_unificado.parquet`** (opcional): Versão mais eficiente do arquivo acima

### Por `calcular_spreads.py`:
- **`relatorio_spreads_maior_010.md`**: Relatório focado em spreads maiores que R$ 0,10
- **`data_b3/relatorio_dataset.md`**: Relatório completo do dataset, ordenado por oportunidades de spread

---

## Dicas e Observações

### Para Iniciantes:

1. **Não tenha pressa:** Os scripts podem levar alguns minutos para processar, especialmente o primeiro que lê um arquivo muito grande.

2. **Leia as mensagens:** Os scripts mostram mensagens informativas durante a execução. Leia com atenção para entender o que está acontecendo.

3. **Erros comuns:**
   - **"Dataset não encontrado"**: Execute o primeiro script antes do segundo
   - **"b3fileparser não instalado"**: Instale com `pip install b3fileparser`
   - **"Arquivo B3 não encontrado"**: Coloque o arquivo COTAHIST_A2025.TXT na pasta `data_b3/`

4. **Formato dos arquivos:**
   - **CSV**: Pode ser aberto no Excel, Google Sheets ou qualquer editor de texto
   - **MD (Markdown)**: Pode ser visualizado em qualquer editor de texto ou visualizador de Markdown

### Conceitos Importantes:

- **Spread**: Diferença de preço entre duas ações relacionadas
- **Threshold (Limiar)**: Um valor de referência para identificar spreads significativos
- **Arbitragem**: Estratégia de comprar uma ação mais barata e vender a mais cara para lucrar com a diferença
- **ON (Ordinária)**: Tipo de ação com direito a voto
- **PN (Preferencial)**: Tipo de ação com prioridade em dividendos
- **Unit**: Ação que combina características de ON e PN

---

## Perguntas Frequentes

**P: Posso executar os scripts em qualquer ordem?**
R: Não. Sempre execute primeiro `carregar_dados_formato_planilha_spread.py` e depois `calcular_spreads.py`.

**P: O que acontece se eu executar o segundo script sem ter executado o primeiro?**
R: O script vai avisar que o arquivo `dataset_unificado.csv` não existe e pedir para executar o primeiro script.

**P: Posso adicionar mais ações para análise?**
R: Sim, mas você precisaria modificar os scripts para incluir os novos códigos de ações.

**P: Os relatórios são atualizados automaticamente?**
R: Não. Você precisa executar os scripts novamente quando quiser atualizar os dados.

**P: Quanto tempo leva para executar?**
R: Depende do tamanho do arquivo da B3, mas geralmente:
- Primeiro script: 1-5 minutos
- Segundo script: 10-30 segundos

---

## Recursos e Links Úteis

### Dados Históricos da B3
- **Site oficial para download de dados históricos:** [Historical Quotes - B3](https://www.b3.com.br/en_us/market-data-and-indices/data-services/market-data/historical-data/equities/historical-quotes/)
  - Neste site você pode baixar os arquivos COTAHIST com dados históricos de cotações
  - Os arquivos são disponibilizados mensalmente e anualmente
  - Formato: arquivos de texto (.TXT) com dados estruturados

### Ferramentas e Bibliotecas
- **b3fileparser**: Biblioteca Python para processar arquivos da B3
- **pandas**: Biblioteca Python para manipulação de dados (já incluída no projeto)
- **pyarrow**: Biblioteca opcional para formato Parquet (mais eficiente que CSV)

---

## Suporte

Se encontrar problemas ou tiver dúvidas:
1. Verifique se todos os arquivos necessários estão no lugar certo
2. Verifique se todas as dependências estão instaladas
3. Leia as mensagens de erro com atenção - elas geralmente explicam o problema

---

**Última atualização:** Janeiro 2026
