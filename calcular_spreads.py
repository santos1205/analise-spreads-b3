"""
Script para calcular spreads usando o dataset unificado
Seguindo a lógica da planilha aula_spread_prime.xlsx
"""

import pandas as pd
from pathlib import Path

print('='*70)
print('CALCULANDO SPREADS - DATASET UNIFICADO')
print('='*70)

# ============================================================================
# ETAPA 1: Carregar dataset unificado
# ============================================================================
print('\n' + '='*70)
print('ETAPA 1: CARREGANDO DATASET UNIFICADO')
print('='*70)

dataset_path = Path('data_b3/dataset_unificado.csv')

if not dataset_path.exists():
    print(f'\nERRO: Dataset nao encontrado: {dataset_path}')
    print('  Execute primeiro: python carregar_dados_formato_planilha_spread.py')
    exit(1)

print(f'\nCarregando: {dataset_path}')
dados = pd.read_csv(dataset_path)

# Converter data
dados['Data'] = pd.to_datetime(dados['Data'])

print(f'\nOK - Dataset carregado!')
print(f'  Total de registros: {len(dados):,}')
print(f'  Ativos: {sorted(dados["Ticker"].unique())}')
print(f'  Periodo: {dados["Data"].min().strftime("%d/%m/%Y")} a {dados["Data"].max().strftime("%d/%m/%Y")}')

# ============================================================================
# ETAPA 2: Calcular Spread Itausa (ITSA3 vs ITSA4)
# ============================================================================
print('\n' + '='*70)
print('ETAPA 2: CALCULANDO SPREAD ITAUSA (ITSA3 vs ITSA4)')
print('='*70)

def calcular_spread_par(dados, ticker1, ticker2, nome_spread):
    """Calcula spread entre dois ativos"""
    
    # Filtrar dados dos dois ativos
    dados_t1 = dados[dados['Ticker'] == ticker1].copy()
    dados_t2 = dados[dados['Ticker'] == ticker2].copy()
    
    # Fazer merge por data
    spread = pd.merge(
        dados_t1[['Data', 'Maxima']],
        dados_t2[['Data', 'Maxima']],
        on='Data',
        suffixes=(f'_{ticker1}', f'_{ticker2}')
    )
    
    spread = spread.rename(columns={
        f'Maxima_{ticker1}': f'Maxima_{ticker1[-1]}',  # Máxima 3
        f'Maxima_{ticker2}': f'Maxima_{ticker2[-1]}'   # Máxima 4
    })
    
    # Calcular qual maior
    spread['Qual_Maior'] = spread.apply(
        lambda row: f'{ticker1[-1]} Maior' if row[f'Maxima_{ticker1[-1]}'] > row[f'Maxima_{ticker2[-1]}'] 
        else f'{ticker2[-1]} Maior' if row[f'Maxima_{ticker2[-1]}'] > row[f'Maxima_{ticker1[-1]}']
        else 'Iguais',
        axis=1
    )
    
    # Calcular diferença em reais (DIF)
    spread['Dif_R$'] = abs(
        spread[f'Maxima_{ticker1[-1]}'] - spread[f'Maxima_{ticker2[-1]}']
    )
    
    # Calcular diferença percentual
    spread['Dif_R%'] = abs(
        (spread[f'Maxima_{ticker1[-1]}'] - spread[f'Maxima_{ticker2[-1]}']) / 
        spread[f'Maxima_{ticker2[-1]}'] * 100
    )
    
    return spread

# Calcular spread Itausa
spread_itausa = calcular_spread_par(dados, 'ITSA3', 'ITSA4', 'Itausa')

print(f'\n  Registros calculados: {len(spread_itausa)}')
print(f'\n  Primeiras 5 linhas:')
print(spread_itausa.head().to_string())

# ============================================================================
# ETAPA 3: Calcular Spread Bradesco (BBDC3 vs BBDC4)
# ============================================================================
print('\n' + '='*70)
print('ETAPA 3: CALCULANDO SPREAD BRADESCO (BBDC3 vs BBDC4)')
print('='*70)

spread_bradesco = calcular_spread_par(dados, 'BBDC3', 'BBDC4', 'Bradesco')

print(f'\n  Registros calculados: {len(spread_bradesco)}')
print(f'\n  Primeiras 5 linhas:')
print(spread_bradesco.head().to_string())

# ============================================================================
# ETAPA 4: Calcular Spread Petrobras (PETR3 vs PETR4)
# ============================================================================
print('\n' + '='*70)
print('ETAPA 4: CALCULANDO SPREAD PETROBRAS (PETR3 vs PETR4)')
print('='*70)

spread_petrobras = calcular_spread_par(dados, 'PETR3', 'PETR4', 'Petrobras')

print(f'\n  Registros calculados: {len(spread_petrobras)}')
print(f'\n  Primeiras 5 linhas:')
print(spread_petrobras.head().to_string())

# ============================================================================
# ETAPA 5: Calcular Spread Santander ((SANB3 + SANB4) vs SANB11)
# ============================================================================
print('\n' + '='*70)
print('ETAPA 5: CALCULANDO SPREAD SANTANDER ((SANB3+SANB4) vs SANB11)')
print('='*70)

# Filtrar dados
dados_sanb3 = dados[dados['Ticker'] == 'SANB3'][['Data', 'Maxima']].copy()
dados_sanb4 = dados[dados['Ticker'] == 'SANB4'][['Data', 'Maxima']].copy()
dados_sanb11 = dados[dados['Ticker'] == 'SANB11'][['Data', 'Maxima']].copy()

# Fazer merge
spread_santander = pd.merge(
    dados_sanb3.rename(columns={'Maxima': 'Maxima_3'}),
    dados_sanb4.rename(columns={'Maxima': 'Maxima_4'}),
    on='Data'
)
spread_santander = pd.merge(
    spread_santander,
    dados_sanb11.rename(columns={'Maxima': 'Maxima_11'}),
    on='Data'
)

# Calcular total 3+4
spread_santander['Maxima_3_4'] = spread_santander['Maxima_3'] + spread_santander['Maxima_4']

# Calcular qual maior
spread_santander['Qual_Maior'] = spread_santander.apply(
    lambda row: '11 Maior' if row['Maxima_11'] > row['Maxima_3_4']
    else '3 e 4 Maior' if row['Maxima_3_4'] > row['Maxima_11']
    else 'Iguais',
    axis=1
)

# Calcular diferença em reais (DIF)
spread_santander['Dif_R$'] = abs(
    spread_santander['Maxima_3_4'] - spread_santander['Maxima_11']
)

# Calcular diferença percentual
spread_santander['Dif_R%'] = abs(
    (spread_santander['Maxima_3_4'] - spread_santander['Maxima_11']) / 
    spread_santander['Maxima_11'] * 100
)

print(f'\n  Registros calculados: {len(spread_santander)}')
print(f'\n  Primeiras 5 linhas:')
print(spread_santander[['Data', 'Maxima_3', 'Maxima_4', 'Maxima_3_4', 'Maxima_11', 'Qual_Maior', 'Dif_R%']].head().to_string())

# ============================================================================
# ETAPA 6: Adicionar Thresholds
# ============================================================================
print('\n' + '='*70)
print('ETAPA 6: ADICIONANDO THRESHOLDS')
print('='*70)

def adicionar_thresholds(spread_df, thresholds_maior, thresholds_menor=None, usar_reais=True):
    """Adiciona colunas de thresholds ao DataFrame
    
    Args:
        usar_reais: Se True, usa Dif_R$ (reais), se False usa Dif_R% (percentual)
    """
    
    coluna_base = 'Dif_R$' if usar_reais else 'Dif_R%'
    sufixo = 'R$' if usar_reais else '%'
    
    # Thresholds "maior que"
    for th in thresholds_maior:
        col_name = f'>_{th}{sufixo}'
        spread_df[col_name] = spread_df[coluna_base].apply(
            lambda x: 'sim' if x > th else 'nao'
        )
    
    # Thresholds "menor que" (se fornecidos)
    if thresholds_menor:
        for th in thresholds_menor:
            col_name = f'<_{th}{sufixo}'
            spread_df[col_name] = spread_df[coluna_base].apply(
                lambda x: 'sim' if x < th else 'nao'
            )
    
    return spread_df

# Thresholds Itausa (em reais)
thresholds_itausa_maior = [0.1, 0.15, 0.2, 0.25, 0.3]  # R$ 0,10, R$ 0,15, etc.
thresholds_itausa_menor = [0.05, 0.1, 0.2, 0.3]  # R$ 0,05, R$ 0,10, etc.
spread_itausa = adicionar_thresholds(spread_itausa, thresholds_itausa_maior, thresholds_itausa_menor, usar_reais=True)

# Thresholds Bradesco (em reais - muitos thresholds)
thresholds_bradesco = [0.1, 0.15, 0.2, 0.25, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 
                       1.2, 1.3, 1.6, 1.8, 2.0, 2.2, 2.4, 2.6, 2.8, 3.0, 3.2, 3.4, 3.6, 
                       3.8, 4.0, 4.2, 4.4, 4.6, 4.8, 5.0, 5.2, 5.4, 5.6, 5.8, 6.0, 6.2, 
                       6.4, 6.6, 6.8, 7.0, 7.2, 7.4, 7.6, 7.8, 8.0, 8.2, 8.4, 8.6]  # Em reais
spread_bradesco = adicionar_thresholds(spread_bradesco, thresholds_bradesco, usar_reais=True)

# Thresholds Petrobras (em reais)
thresholds_petrobras = [0.1, 0.15, 0.2, 0.25, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 
                       1.2, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0]  # Em reais
spread_petrobras = adicionar_thresholds(spread_petrobras, thresholds_petrobras, usar_reais=True)

# Thresholds Santander (em reais)
thresholds_santander = [0.1, 0.15, 0.2, 0.25, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]  # Em reais
spread_santander = adicionar_thresholds(spread_santander, thresholds_santander, usar_reais=True)

print('\n  Thresholds adicionados para todos os spreads!')

# ============================================================================
# ETAPA 7: Estatísticas
# ============================================================================
print('\n' + '='*70)
print('ETAPA 7: ESTATISTICAS DOS SPREADS')
print('='*70)

def calcular_estatisticas_spread(spread_df, nome):
    """Calcula estatísticas detalhadas do spread"""
    total = len(spread_df)
    
    print(f'\n  {nome}:')
    print(f'    Periodo: {spread_df["Data"].min().strftime("%d/%m/%Y")} a {spread_df["Data"].max().strftime("%d/%m/%Y")}')
    print(f'    Total de registros: {total:,}')
    print(f'\n    Estatisticas Dif R%:')
    print(f'      Media: {spread_df["Dif_R%"].mean():.4f}%')
    print(f'      Minima: {spread_df["Dif_R%"].min():.4f}%')
    print(f'      Maxima: {spread_df["Dif_R%"].max():.4f}%')
    print(f'      Qual maior mais comum: {spread_df["Qual_Maior"].value_counts().index[0]}')
    
    print(f'\n    Registros por threshold (em REAIS):')
    th_010 = len(spread_df[spread_df['Dif_R$'] > 0.10])
    th_015 = len(spread_df[spread_df['Dif_R$'] > 0.15])
    th_020 = len(spread_df[spread_df['Dif_R$'] > 0.20])
    th_030 = len(spread_df[spread_df['Dif_R$'] > 0.30])
    
    print(f'      Spread > R$ 0,10: {th_010:,} registros ({th_010/total*100:.2f}%)')
    print(f'      Spread > R$ 0,15: {th_015:,} registros ({th_015/total*100:.2f}%)')
    print(f'      Spread > R$ 0,20: {th_020:,} registros ({th_020/total*100:.2f}%)')
    print(f'      Spread > R$ 0,30: {th_030:,} registros ({th_030/total*100:.2f}%)')
    
    return {
        'total': total,
        'th_010': th_010,
        'th_015': th_015,
        'th_020': th_020,
        'th_030': th_030
    }

stats_itausa = calcular_estatisticas_spread(spread_itausa, 'SPREAD ITAUSA (ITSA3 vs ITSA4)')

stats_bradesco = calcular_estatisticas_spread(spread_bradesco, 'SPREAD BRADESCO (BBDC3 vs BBDC4)')

stats_petrobras = calcular_estatisticas_spread(spread_petrobras, 'SPREAD PETROBRAS (PETR3 vs PETR4)')

if len(spread_santander) > 0:
    stats_santander = calcular_estatisticas_spread(spread_santander, 'SPREAD SANTANDER ((SANB3+SANB4) vs SANB11)')
else:
    print(f'\n  SPREAD SANTANDER ((SANB3+SANB4) vs SANB11):')
    print(f'    AVISO: Nenhum registro encontrado!')
    print(f'    SANB11 nao esta no dataset unificado.')
    print(f'    Verifique se SANB11 foi incluido no carregamento dos dados.')
    stats_santander = None

# ============================================================================
# ETAPA 8: Gerar relatório de spreads > R$ 0,10
# ============================================================================
print('\n' + '='*70)
print('ETAPA 8: GERANDO RELATORIO DE SPREADS > R$ 0,10')
print('='*70)

# Coletar dados de spreads > R$ 0,10
relatorio_spreads = []

# Itausa
spreads_itausa_010 = len(spread_itausa[spread_itausa['Dif_R$'] > 0.10])
relatorio_spreads.append({
    'Ativo': 'Itausa (ITSA3 vs ITSA4)',
    'Total_Registros': len(spread_itausa),
    'Spreads_>_0.10': spreads_itausa_010,
    'Percentual': (spreads_itausa_010 / len(spread_itausa) * 100) if len(spread_itausa) > 0 else 0,
    'Media_Dif_R%': spread_itausa['Dif_R%'].mean()
})

# Bradesco
spreads_bradesco_010 = len(spread_bradesco[spread_bradesco['Dif_R$'] > 0.10])
relatorio_spreads.append({
    'Ativo': 'Bradesco (BBDC3 vs BBDC4)',
    'Total_Registros': len(spread_bradesco),
    'Spreads_>_0.10': spreads_bradesco_010,
    'Percentual': (spreads_bradesco_010 / len(spread_bradesco) * 100) if len(spread_bradesco) > 0 else 0,
    'Media_Dif_R%': spread_bradesco['Dif_R%'].mean()
})

# Petrobras
spreads_petrobras_010 = len(spread_petrobras[spread_petrobras['Dif_R$'] > 0.10])
relatorio_spreads.append({
    'Ativo': 'Petrobras (PETR3 vs PETR4)',
    'Total_Registros': len(spread_petrobras),
    'Spreads_>_0.10': spreads_petrobras_010,
    'Percentual': (spreads_petrobras_010 / len(spread_petrobras) * 100) if len(spread_petrobras) > 0 else 0,
    'Media_Dif_R%': spread_petrobras['Dif_R%'].mean()
})

# Santander
if len(spread_santander) > 0:
    spreads_santander_010 = len(spread_santander[spread_santander['Dif_R$'] > 0.10])
    relatorio_spreads.append({
        'Ativo': 'Santander ((SANB3+SANB4) vs SANB11)',
        'Total_Registros': len(spread_santander),
        'Spreads_>_0.10': spreads_santander_010,
        'Percentual': (spreads_santander_010 / len(spread_santander) * 100) if len(spread_santander) > 0 else 0,
        'Media_Dif_R%': spread_santander['Dif_R%'].mean()
    })

# Ordenar por quantidade de spreads > R$ 0,10 (decrescente)
relatorio_spreads.sort(key=lambda x: x['Spreads_>_0.10'], reverse=True)

# Gerar arquivo markdown
relatorio_path = Path('relatorio_spreads_maior_010.md')
with open(relatorio_path, 'w', encoding='utf-8') as f:
    f.write('# Relatório de Spreads > R$ 0,10\n\n')
    f.write(f'**Data de geração:** {pd.Timestamp.now().strftime("%d/%m/%Y %H:%M:%S")}\n\n')
    f.write('## Resumo\n\n')
    f.write('Este relatório apresenta os ativos ordenados pela quantidade de spreads maiores que R$ 0,10.\n\n')
    f.write('---\n\n')
    f.write('## Ranking de Ativos por Quantidade de Spreads > R$ 0,10\n\n')
    f.write('| Posição | Ativo | Total de Registros | Spreads > R$ 0,10 | Percentual | Média Dif R% |\n')
    f.write('|---------|-------|-------------------|-------------------|------------|-------------|\n')
    
    for idx, item in enumerate(relatorio_spreads, 1):
        f.write(f"| {idx} | {item['Ativo']} | {item['Total_Registros']:,} | "
                f"{item['Spreads_>_0.10']:,} | {item['Percentual']:.2f}% | "
                f"{item['Media_Dif_R%']:.4f}% |\n")
    
    f.write('\n---\n\n')
    f.write('## Detalhamento por Ativo\n\n')
    
    for item in relatorio_spreads:
        f.write(f"### {item['Ativo']}\n\n")
        f.write(f"- **Total de registros:** {item['Total_Registros']:,}\n")
        f.write(f"- **Spreads > R$ 0,10:** {item['Spreads_>_0.10']:,} ({item['Percentual']:.2f}%)\n")
        f.write(f"- **Média de diferença percentual:** {item['Media_Dif_R%']:.4f}%\n\n")

print(f'\n  Relatório gerado: {relatorio_path}')
print(f'\n  Ranking de ativos por spreads > R$ 0,10:')
for idx, item in enumerate(relatorio_spreads, 1):
    print(f'    {idx}. {item["Ativo"]}: {item["Spreads_>_0.10"]:,} spreads ({item["Percentual"]:.2f}%)')

# ============================================================================
# ETAPA 9: Gerar relatório do dataset ordenado por spreads > R$ 0,10
# ============================================================================
print('\n' + '='*70)
print('ETAPA 9: GERANDO RELATORIO DO DATASET (ORDENADO POR SPREADS > R$ 0,10)')
print('='*70)

# Criar mapeamento de tickers para spreads > 0,10
ticker_spread_map = {}
for item in relatorio_spreads:
    if 'ITSA' in item['Ativo']:
        ticker_spread_map['ITSA3'] = item['Spreads_>_0.10']
        ticker_spread_map['ITSA4'] = item['Spreads_>_0.10']
    elif 'Bradesco' in item['Ativo'] or 'BBDC' in item['Ativo']:
        ticker_spread_map['BBDC3'] = item['Spreads_>_0.10']
        ticker_spread_map['BBDC4'] = item['Spreads_>_0.10']
    elif 'Petrobras' in item['Ativo'] or 'PETR' in item['Ativo']:
        ticker_spread_map['PETR3'] = item['Spreads_>_0.10']
        ticker_spread_map['PETR4'] = item['Spreads_>_0.10']
    elif 'Santander' in item['Ativo'] or 'SANB' in item['Ativo']:
        ticker_spread_map['SANB3'] = item['Spreads_>_0.10']
        ticker_spread_map['SANB4'] = item['Spreads_>_0.10']
        ticker_spread_map['SANB11'] = item['Spreads_>_0.10']

# Calcular estatísticas por ativo
estatisticas_ativos = []
for ticker in dados['Ticker'].unique():
    dados_ticker = dados[dados['Ticker'] == ticker]
    spreads_010 = ticker_spread_map.get(ticker, 0)
    estatisticas_ativos.append({
        'Ticker': ticker,
        'Registros': len(dados_ticker),
        'Preco_Max_Media': dados_ticker['Maxima'].mean(),
        'Preco_Max_Min': dados_ticker['Maxima'].min(),
        'Preco_Max_Max': dados_ticker['Maxima'].max(),
        'Volume_Total': dados_ticker['Volume_R$'].sum(),
        'Spreads_>_0.10': spreads_010
    })

# Ordenar por spreads > 0,10 (decrescente)
estatisticas_ativos.sort(key=lambda x: x['Spreads_>_0.10'], reverse=True)

# Gerar arquivo markdown
relatorio_dataset_path = Path('data_b3/relatorio_dataset.md')
with open(relatorio_dataset_path, 'w', encoding='utf-8') as f:
    f.write('# Relatório do Dataset Unificado\n\n')
    f.write(f'**Gerado em:** {pd.Timestamp.now().strftime("%d/%m/%Y %H:%M:%S")}\n\n')
    f.write(f'**Dataset:** `{dataset_path}`\n\n')
    f.write(f'**Total de registros:** {len(dados):,}\n\n')
    f.write(f'**Período:** {dados["Data"].min().strftime("%d/%m/%Y")} a {dados["Data"].max().strftime("%d/%m/%Y")}\n\n')
    f.write(f'**Ativos:** {", ".join(sorted(dados["Ticker"].unique()))}\n\n')
    f.write('> **Nota:** Os ativos estão ordenados em ordem decrescente pela quantidade de spreads > R$ 0,10.\n\n')
    f.write('---\n\n')
    f.write('## Estatísticas por Ativo (Ordenado por Spreads > R$ 0,10)\n\n')
    f.write('| Ativo | Registros | Preço Máx - Média | Preço Máx - Min | Preço Máx - Max | Volume Total (R$) | Spreads > R$ 0,10 |\n')
    f.write('|-------|-----------|-------------------|-----------------|-----------------|-------------------|-------------------|\n')
    
    for stat in estatisticas_ativos:
        f.write(f"| {stat['Ticker']} | {stat['Registros']:,} | "
                f"R$ {stat['Preco_Max_Media']:.2f} | "
                f"R$ {stat['Preco_Max_Min']:.2f} | "
                f"R$ {stat['Preco_Max_Max']:.2f} | "
                f"R$ {stat['Volume_Total']:,.2f} | "
                f"{stat['Spreads_>_0.10']:,} |\n")
    
    f.write('\n---\n\n')
    f.write('## Detalhamento por Ativo\n\n')
    
    for stat in estatisticas_ativos:
        f.write(f"### {stat['Ticker']}\n\n")
        f.write(f"- **Registros:** {stat['Registros']:,}\n")
        f.write(f"- **Preço Máximo - Média:** R$ {stat['Preco_Max_Media']:.2f}\n")
        f.write(f"- **Preço Máximo - Mínimo:** R$ {stat['Preco_Max_Min']:.2f}\n")
        f.write(f"- **Preço Máximo - Máximo:** R$ {stat['Preco_Max_Max']:.2f}\n")
        f.write(f"- **Volume Total:** R$ {stat['Volume_Total']:,.2f}\n")
        f.write(f"- **Spreads > R$ 0,10:** {stat['Spreads_>_0.10']:,}\n\n")

print(f'\n  Relatório gerado: {relatorio_dataset_path}')
print(f'\n  Ativos ordenados por spreads > R$ 0,10:')
for idx, stat in enumerate(estatisticas_ativos, 1):
    print(f'    {idx}. {stat["Ticker"]}: {stat["Spreads_>_0.10"]:,} spreads')

# ============================================================================
# RESUMO FINAL
# ============================================================================
print('\n' + '='*70)
print('RESUMO FINAL')
print('='*70)

print(f'\n  Spreads calculados com sucesso!')
print(f'\n  Spreads processados:')
print(f'    - Spread Itausa (ITSA3 vs ITSA4): {len(spread_itausa)} registros')
print(f'    - Spread Bradesco (BBDC3 vs BBDC4): {len(spread_bradesco)} registros')
print(f'    - Spread Petrobras (PETR3 vs PETR4): {len(spread_petrobras)} registros')
print(f'    - Spread Santander ((SANB3+SANB4) vs SANB11): {len(spread_santander)} registros')
print(f'\n  Todos os spreads incluem:')
print(f'    - Data')
print(f'    - Precos maximos')
print(f'    - Qual maior')
print(f'    - Dif R%')
print(f'    - Thresholds (sim/nao)')

print('\n' + '='*70)
print('CONCLUIDO!')
print('='*70)

