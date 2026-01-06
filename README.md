# Spread App - Análise de Spreads de Ações

Aplicação Python para análise de spreads entre diferentes tipos de ações de empresas brasileiras listadas na B3.

## 📋 Sobre o Projeto

Este projeto analisa **spreads** (diferenças de preço) entre diferentes classes de ações das mesmas empresas, permitindo identificar oportunidades de arbitragem.

### Empresas Analisadas

- **Itausa** (ITSA3 vs ITSA4)
- **Bradesco** (BBDC3 vs BBDC4)
- **Petrobras** (PETR3 vs PETR4)
- **Santander** ((SANB3 + SANB4) vs SANB11)

## 🚀 Como Usar

### Pré-requisitos

1. Python 3.7 ou superior
2. Instalar dependências:
   ```bash
   pip install pandas b3fileparser
   ```
   Opcional (para formato Parquet):
   ```bash
   pip install pyarrow
   ```

3. Baixar arquivos históricos da B3:
   - Acesse: [Historical Quotes - B3](https://www.b3.com.br/en_us/market-data-and-indices/data-services/market-data/historical-data/equities/historical-quotes/)
   - Baixe os arquivos `COTAHIST_A2024.TXT` e/ou `COTAHIST_A2025.TXT`
   - Coloque-os na pasta `data_b3/`

### Execução

**IMPORTANTE:** Execute os scripts nesta ordem:

1. **Carregar e processar dados da B3:**
   ```bash
   python carregar_dados_formato_planilha_spread.py
   ```
   - Processa os arquivos COTAHIST da B3
   - Filtra apenas os ativos necessários
   - Gera o arquivo `data_b3/dataset_unificado.csv`

2. **Calcular spreads e gerar relatórios:**
   ```bash
   python calcular_spreads.py
   ```
   - Calcula spreads entre as ações
   - Adiciona thresholds (limiares)
   - Gera estatísticas
   - Cria relatórios em Markdown

## 📁 Estrutura do Projeto

```
spread_app/
├── data_b3/                    # Dados (ignorado no Git)
│   ├── COTAHIST_A2024.TXT     # Arquivo histórico B3 (2024)
│   ├── COTAHIST_A2025.TXT     # Arquivo histórico B3 (2025)
│   ├── dataset_unificado.csv   # Dataset processado
│   └── relatorio_dataset.md    # Relatório do dataset
├── help/                       # Documentação auxiliar
│   ├── aula_spread_prime.xlsx
│   ├── blue_chips_spread.md
│   └── planilha_spread_prime.md
├── calcular_spreads.py         # Script principal - cálculo de spreads
├── carregar_dados_formato_planilha_spread.py  # Script - carregamento de dados
├── GUIA_SCRIPTS_PYTHON.md     # Guia detalhado dos scripts
├── relatorio_spreads_maior_010.md  # Relatório de spreads > R$ 0,10
└── README.md                   # Este arquivo
```

## 📊 Arquivos Gerados

### Por `carregar_dados_formato_planilha_spread.py`:
- `data_b3/dataset_unificado.csv` - Dataset com dados organizados
- `data_b3/dataset_unificado.parquet` (opcional) - Versão otimizada

### Por `calcular_spreads.py`:
- `relatorio_spreads_maior_010.md` - Ranking de ativos por spreads > R$ 0,10
- `data_b3/relatorio_dataset.md` - Relatório completo do dataset

## 📖 Documentação

Para entender detalhadamente o que cada script faz, consulte:
- **[GUIA_SCRIPTS_PYTHON.md](GUIA_SCRIPTS_PYTHON.md)** - Guia completo e detalhado em linguagem simples

## 🔧 Tecnologias Utilizadas

- **Python 3**
- **pandas** - Manipulação de dados
- **b3fileparser** - Processamento de arquivos da B3
- **pyarrow** (opcional) - Formato Parquet

## 📝 Conceitos Importantes

- **Spread**: Diferença de preço entre duas ações relacionadas
- **Threshold (Limiar)**: Valor de referência para identificar spreads significativos
- **Arbitragem**: Estratégia de comprar a ação mais barata e vender a mais cara
- **ON (Ordinária)**: Ação com direito a voto
- **PN (Preferencial)**: Ação com prioridade em dividendos
- **Unit**: Ação que combina características de ON e PN

## ⚠️ Observações

- Os arquivos da pasta `data_b3/` são grandes e não são versionados no Git
- Execute sempre o primeiro script antes do segundo
- Os relatórios são gerados a cada execução (não são atualizados automaticamente)

## 📄 Licença

Este projeto é para uso pessoal/educacional.

---

**Última atualização:** Janeiro 2026

