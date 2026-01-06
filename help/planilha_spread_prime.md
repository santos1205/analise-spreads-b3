# Análise da Planilha: aula_spread_prime.xlsx

## Visão Geral

Este arquivo Excel contém análises de **spread trading** (pairs trading) para três pares de ações brasileiras, focando na comparação entre ações ordinárias (ON) e preferenciais (PN), além de units.

### Resumo de Períodos

| Planilha | Primeira Data | Última Data | Período | Total Registros |
|----------|---------------|-------------|---------|-----------------|
| **Spread Itausa** | 10/04/2014 | 15/03/2022 | 7.9 anos (2.896 dias) | 1.960 |
| **Spread Bradesco** | 17/02/2014 | 16/03/2022 | 8.1 anos (2.949 dias) | 1.997 |
| **Spread Santander** | 03/01/2017 | 16/03/2022 | 5.2 anos (1.898 dias) | 1.280 |

## Estrutura das Planilhas

O arquivo possui **3 planilhas principais**:

1. **Spread Itausa** - Comparação ITSA3 vs ITSA4
2. **Spread Bradesco** - Comparação BBDC3 vs BBDC4  
3. **Spread Santander** - Comparação (SANB3 + SANB4) vs SANB11

---

## 1. Spread Itausa

### Informações Gerais
- **Ativos comparados**: ITSA3 (ON) vs ITSA4 (PN)
- **Total de registros**: 1.960 registros
- **Período**: 10/04/2014 a 15/03/2022 (7.9 anos - 2.896 dias)

### Estrutura de Dados

#### Colunas Principais:
- **Data**: Data da negociação
- **Máxima 3**: Preço máximo do dia de ITSA3
- **Máxima 4**: Preço máximo do dia de ITSA4
- **Qual Maior**: Indica qual ativo teve maior preço (ex: "3 Maior" = ITSA3 maior)
- **Dif R%**: Diferença percentual entre os preços

#### Thresholds de Decisão:
- **Colunas ">"**: Indicam se a diferença percentual é **maior** que:
  - 0.1% (10 pontos base)
  - 0.15% (15 pontos base)
  - 0.2% (20 pontos base)
  - 0.25% (25 pontos base)
  - 0.3% (30 pontos base)

- **Colunas "<"**: Indicam se a diferença percentual é **menor** que:
  - 0.05% (5 pontos base)
  - 0.1% (10 pontos base)
  - 0.2% (20 pontos base)
  - 0.3% (30 pontos base)

#### Valores dos Indicadores:
- **"sim"**: Threshold atingido
- **"não"**: Threshold não atingido

#### Exemplo de Dados:
```
Data: 2022-03-15
Máxima 3: 10.04
Máxima 4: 9.95
Qual Maior: 3 Maior
Dif R%: 0.09%
> 0.1%: não
< 0.1%: sim
```

#### Informações Adicionais:
- **Tag Along**: ON = 0.8, PN = 0.8
- **Dividendo**: ON = 1, PN = 1
- **Volatilidade**: 0.025 (2.5%)

---

## 2. Spread Bradesco

### Informações Gerais
- **Ativos comparados**: BBDC3 (ON) vs BBDC4 (PN)
- **Total de registros**: 1.997 registros
- **Período**: 17/02/2014 a 16/03/2022 (8.1 anos - 2.949 dias)

### Estrutura de Dados

#### Colunas Principais:
- **Data**: Data da negociação
- **Máxima 3**: Preço máximo do dia de BBDC3
- **Máxima 4**: Preço máximo do dia de BBDC4
- **Qual Maior**: Indica qual ativo teve maior preço (ex: "4 Maior" = BBDC4 maior)
- **Dif R%**: Diferença percentual entre os preços
- **Preço justo PN**: Cálculo do preço justo da preferencial

#### Thresholds de Decisão:
- **Múltiplas colunas ">"**: Indicam se a diferença percentual é **maior** que valores de:
  - 0.1% até 8.6% (mais de 50 thresholds diferentes)
  - Valores incrementais: 0.1, 0.15, 0.2, 0.25, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.2, 1.3, 1.6, 1.8, 2.0, 2.19, 2.40, 2.60, 2.80, 3.00, 3.2, 3.4, 3.6, 3.8, 4.0, 4.2, 4.4, 4.6, 4.8, 5.0, 5.2, 5.4, 5.6, 5.8, 6.0, 6.2, 6.4, 6.6, 6.8, 7.0, 7.2, 7.4, 7.6, 7.8, 8.0, 8.2, 8.4, 8.6

#### Características Especiais:
- **Diferença percentual maior**: Típicamente entre 3.5% e 4.5% (spread mais amplo que Itausa)
- **Mais thresholds**: Sistema mais granular de identificação de oportunidades

#### Exemplo de Dados:
```
Data: 2022-03-16
Máxima 3: 17.26
Máxima 4: 21.00
Qual Maior: 4 Maior
Dif R%: 3.74%
> 0.1%: sim
> 0.15%: sim
> 0.2%: sim
...
```

#### Informações Adicionais:
- **Tag Along**: ON = 1, PN = 0.8
- **Dividendo**: ON = 0.9, PN = 1
- **Volatilidade**: 0.029 (2.9%)

---

## 3. Spread Santander

### Informações Gerais
- **Ativos comparados**: (SANB3 + SANB4) vs SANB11 (Unit)
- **Total de registros**: 1.280 registros
- **Período**: 03/01/2017 a 16/03/2022 (5.2 anos - 1.898 dias)

### Estrutura de Dados

#### Colunas Principais:
- **Data**: Data da negociação
- **Máxima 3+4**: Soma dos preços máximos de SANB3 e SANB4
- **Máxima 11**: Preço máximo do dia de SANB11 (Unit)
- **Qual Maior**: Indica qual é maior:
  - "11 Maior" = SANB11 maior que (SANB3 + SANB4)
  - "3 e 4 Maior" = (SANB3 + SANB4) maior que SANB11
- **Dif R%**: Diferença percentual entre (SANB3 + SANB4) e SANB11
- **Preço justo Unit**: Cálculo do preço justo da unit
- **Dif R$ Unit**: Diferença em reais da unit

#### Thresholds de Decisão:
- **Colunas ">"**: Indicam se a diferença percentual é **maior** que:
  - 0.1%, 0.15%, 0.2%, 0.25%, 0.3%, 0.4%, 0.5%, 0.6%, 0.7%, 0.8%, 0.9%, 1.0%

#### Características Especiais:
- **Estratégia diferente**: Compara a **soma** de duas ações (ON + PN) com uma **unit**
- **Lógica de arbitragem**: Identifica quando comprar/vender units vs ações individuais
- **Diferenças menores**: Típicamente entre 0.05% e 0.65%

#### Exemplo de Dados:
```
Data: 2022-03-16
Máxima 3+4: 33.97
Máxima 11: 34.04
Qual Maior: 11 Maior
Dif R%: 0.07%
> 0.1%: não
> 0.15%: não
...
```

#### Informações Adicionais:
- **Tag Along**: ON = 1, PN = 1
- **Dividendo**: ON = 0.9, PN = 1
- **Total 3+4**: 75 (quantidade de ações 3+4 equivalente a 1 unit)
- **Total 11**: 1200 (quantidade de units)

---

## Conceitos e Estratégias Aplicadas

### 1. Pairs Trading / Spread Trading
Estratégia que explora a diferença de preço entre ativos correlacionados:
- **Long & Short**: Comprar o ativo subvalorizado e vender o supervalorizado
- **Convergência**: Espera-se que os preços voltem ao equilíbrio

### 2. Diferença Percentual (Dif R%)
Cálculo da diferença relativa entre os preços:
```
Dif R% = |Preço1 - Preço2| / Preço2 * 100
```

### 3. Thresholds de Decisão
Sistema de múltiplos níveis percentuais para:
- **Identificar oportunidades**: Quando o spread ultrapassa determinado nível
- **Gerenciar risco**: Diferentes níveis para diferentes estratégias
- **Timing de entrada/saída**: Decisões baseadas em múltiplos critérios

### 4. Volatilidade
Medida da variação dos preços:
- **Itausa**: 2.5% de volatilidade
- **Bradesco**: 2.9% de volatilidade
- Usado para projeções de máxima e mínima

### 5. Tag Along e Dividendos
Direitos dos acionistas que afetam a precificação:
- **Tag Along**: Direito de venda junto com controlador
- **Dividendo**: Proporção de distribuição de dividendos
- ON e PN podem ter direitos diferentes, justificando spreads

### 6. Projeções
Algumas planilhas incluem:
- **Proj. Máx**: Projeção de preço máximo
- **Proj Mín**: Projeção de preço mínimo
- Baseadas em volatilidade e histórico

---

## Padrões Identificados

### Itausa (ITSA3 vs ITSA4)
- Spreads **pequenos**: Típicamente entre 0.05% e 0.25%
- ITSA3 geralmente maior que ITSA4
- Thresholds mais conservadores (0.05% a 0.3%)

### Bradesco (BBDC3 vs BBDC4)
- Spreads **médios a grandes**: Típicamente entre 3.5% e 4.5%
- BBDC4 geralmente maior que BBDC3
- Thresholds muito granulares (0.1% até 8.6%)
- Sistema mais sofisticado de identificação

### Santander (SANB3+SANB4 vs SANB11)
- Spreads **pequenos**: Típicamente entre 0.03% e 0.65%
- Alternância entre qual é maior
- Estratégia de arbitragem entre units e ações individuais
- Thresholds moderados (0.1% até 1.0%)

---

## Aplicações Práticas

### Para Desenvolvimento do App

1. **Estrutura de Dados**:
   - Tabela principal com: Data, Preço1, Preço2, Dif R%, Qual Maior
   - Tabela de thresholds configuráveis
   - Tabela de indicadores binários (sim/não)

2. **Cálculos Necessários**:
   - Diferença percentual entre ativos
   - Identificação de qual ativo é maior
   - Comparação com múltiplos thresholds
   - Cálculo de preço justo (quando aplicável)

3. **Funcionalidades**:
   - Alertas quando thresholds são atingidos
   - Visualização de histórico de spreads
   - Gráficos de convergência/divergência
   - Backtesting de estratégias

4. **Configurações**:
   - Thresholds personalizáveis por par de ativos
   - Volatilidade configurável
   - Parâmetros de Tag Along e Dividendos

---

## Observações Técnicas

- **Formato de data**: Datetime (YYYY-MM-DD HH:MM:SS)
- **Encoding**: Possíveis caracteres especiais (ex: "Máxima" pode aparecer como "Mxima")
- **Valores nulos**: Algumas células podem estar vazias
- **Cabeçalhos**: Linha 2 (índice 2) contém os cabeçalhos principais
- **Dados começam**: Linha 3 (índice 3) em diante

---

## Próximos Passos Sugeridos

1. **Implementar parser** para ler e processar dados do Excel
2. **Criar schema de banco de dados** para armazenar histórico
3. **Desenvolver funções de cálculo** de spread e thresholds
4. **Implementar sistema de alertas** baseado em thresholds
5. **Criar visualizações** de histórico e tendências
6. **Adicionar funcionalidade de backtesting** de estratégias

