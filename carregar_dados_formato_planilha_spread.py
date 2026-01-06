"""
Script para carregar dados dos arquivos COTAHIST_A2024.TXT e COTAHIST_A2025.TXT da B3
para os ativos identificados na estrutura da planilha aula_spread_prime.xlsx

Baseado no layout da planilha:
- Spread Itausa: ITSA3 vs ITSA4
- Spread Bradesco: BBDC3 vs BBDC4
- Spread Santander: (SANB3 + SANB4) vs SANB11
"""

import pandas as pd
from pathlib import Path

print('='*70)
print('CARREGANDO DADOS B3 PARA ATIVOS DA PLANILHA')
print('='*70)

# ============================================================================
# ETAPA 1: Identificar ativos baseado na estrutura da planilha
# ============================================================================
print('\n' + '='*70)
print('ETAPA 1: IDENTIFICANDO ATIVOS DA PLANILHA')
print('='*70)

# Baseado no help/planilha_spread_prime.md:
# - Spread Itausa: ITSA3 (ON) vs ITSA4 (PN)
# - Spread Bradesco: BBDC3 (ON) vs BBDC4 (PN)
# - Spread Santander: (SANB3 + SANB4) vs SANB11 (Unit)

ativos_necessarios = {'ITSA3', 'ITSA4', 'BBDC3', 'BBDC4', 'SANB3', 'SANB4', 'SANB11'}

print(f'\n  Ativos identificados na estrutura da planilha:')
print(f'    - Spread Itausa: ITSA3, ITSA4')
print(f'    - Spread Bradesco: BBDC3, BBDC4')
print(f'    - Spread Santander: SANB3, SANB4, SANB11')
print(f'\n  Total de ativos: {len(ativos_necessarios)}')
print(f'  Ativos: {sorted(ativos_necessarios)}')

# ============================================================================
# ETAPA 2: Carregar arquivos B3
# ============================================================================
print('\n' + '='*70)
print('ETAPA 2: CARREGANDO ARQUIVOS B3')
print('='*70)

arquivo_2024 = Path('data_b3/COTAHIST_A2024.TXT')
arquivo_2025 = Path('data_b3/COTAHIST_A2025.TXT')

# Verificar quais arquivos existem
arquivos_para_processar = []
if arquivo_2024.exists():
    arquivos_para_processar.append(arquivo_2024)
    print(f'\nArquivo encontrado: {arquivo_2024}')
    print(f'  Tamanho: {arquivo_2024.stat().st_size / (1024*1024):.2f} MB')
else:
    print(f'\nAVISO: Arquivo nao encontrado: {arquivo_2024}')

if arquivo_2025.exists():
    arquivos_para_processar.append(arquivo_2025)
    print(f'\nArquivo encontrado: {arquivo_2025}')
    print(f'  Tamanho: {arquivo_2025.stat().st_size / (1024*1024):.2f} MB')
else:
    print(f'\nAVISO: Arquivo nao encontrado: {arquivo_2025}')

if len(arquivos_para_processar) == 0:
    print(f'\nERRO: Nenhum arquivo B3 encontrado!')
    print(f'  Procurando por: {arquivo_2024} ou {arquivo_2025}')
    exit(1)

print(f'\nTotal de arquivos para processar: {len(arquivos_para_processar)}')
print('  (Isso pode levar alguns minutos...)')

try:
    from b3fileparser.b3parser import B3Parser
    
    parser = B3Parser.create_parser(engine='pandas')
    
    # Lista para armazenar dados de cada arquivo
    lista_dados = []
    
    # Processar cada arquivo
    for arquivo in arquivos_para_processar:
        print(f'\nProcessando: {arquivo.name}...')
        dados_arquivo = parser.read_b3_file(str(arquivo))
        print(f'  Registros carregados: {len(dados_arquivo):,}')
        lista_dados.append(dados_arquivo)
    
    # Combinar todos os dados
    print(f'\nCombinando dados de {len(lista_dados)} arquivo(s)...')
    dados_b3 = pd.concat(lista_dados, ignore_index=True)
    
    print(f'\nOK - Arquivos B3 processados!')
    print(f'  Total de registros combinados: {len(dados_b3):,}')
    
    # Limpar códigos
    dados_b3['CODIGO_DE_NEGOCIACAO'] = dados_b3['CODIGO_DE_NEGOCIACAO'].astype(str).str.strip()
    
except ImportError:
    print('\nERRO: b3fileparser nao instalado!')
    print('  Instale com: pip install b3fileparser')
    exit(1)
except Exception as e:
    print(f'\nERRO ao processar arquivo(s) B3: {e}')
    import traceback
    traceback.print_exc()
    exit(1)

# ============================================================================
# ETAPA 3: Filtrar dados B3 pelos ativos da planilha
# ============================================================================
print('\n' + '='*70)
print('ETAPA 3: FILTRANDO DADOS B3 PELOS ATIVOS DA PLANILHA')
print('='*70)

# Filtrar apenas os ativos que estão na planilha
dados_filtrados = dados_b3[dados_b3['CODIGO_DE_NEGOCIACAO'].isin(ativos_necessarios)].copy()

print(f'\n  Registros antes do filtro: {len(dados_b3):,}')
print(f'  Registros apos filtro: {len(dados_filtrados):,}')

# Verificar quais ativos foram encontrados
ativos_encontrados = dados_filtrados['CODIGO_DE_NEGOCIACAO'].unique()
print(f'\n  Ativos encontrados no arquivo B3:')
for ativo in sorted(ativos_encontrados):
    count = len(dados_filtrados[dados_filtrados['CODIGO_DE_NEGOCIACAO'] == ativo])
    print(f'    - {ativo}: {count:,} registros')

# Verificar se algum ativo não foi encontrado
ativos_nao_encontrados = ativos_necessarios - set(ativos_encontrados)
if ativos_nao_encontrados:
    print(f'\n  AVISO - Ativos nao encontrados no arquivo B3:')
    for ativo in sorted(ativos_nao_encontrados):
        print(f'    - {ativo}')
    
    # Procurar variações (ex: SANB11 pode estar como SANB11T ou similar)
    print(f'\n  Procurando variacoes dos ativos nao encontrados...')
    ativos_com_variacoes = ativos_necessarios.copy()
    
    for ativo_faltando in sorted(ativos_nao_encontrados):
        matches = dados_b3[dados_b3['CODIGO_DE_NEGOCIACAO'].str.contains(ativo_faltando[:4], case=False, na=False)]
        if len(matches) > 0:
            variacoes = matches['CODIGO_DE_NEGOCIACAO'].unique()[:5]
            print(f'    {ativo_faltando}: Variacoes encontradas: {list(variacoes)}')
            # Adicionar a primeira variação encontrada
            if len(variacoes) > 0:
                ativos_com_variacoes.add(variacoes[0])
                print(f'      -> Adicionando {variacoes[0]} ao conjunto de ativos')
    
    # Refazer filtro com variações
    dados_filtrados = dados_b3[dados_b3['CODIGO_DE_NEGOCIACAO'].isin(ativos_com_variacoes)].copy()
    ativos_encontrados = dados_filtrados['CODIGO_DE_NEGOCIACAO'].unique()
    print(f'\n  Apos incluir variacoes: {len(dados_filtrados):,} registros')

# ============================================================================
# ETAPA 4: Preparar dados para junção
# ============================================================================
print('\n' + '='*70)
print('ETAPA 4: PREPARANDO DADOS PARA JUNCAO')
print('='*70)

# Converter data no B3
dados_filtrados['DATA_DO_PREGAO'] = pd.to_datetime(dados_filtrados['DATA_DO_PREGAO'], errors='coerce')

# Selecionar colunas importantes do B3
colunas_b3 = [
    'CODIGO_DE_NEGOCIACAO',
    'DATA_DO_PREGAO',
    'PRECO_DE_ABERTURA',
    'PRECO_MAXIMO',
    'PRECO_MINIMO',
    'PRECO_ULTIMO_NEGOCIO',
    'QUANTIDADE_NEGOCIADA',
    'VOLUME_TOTAL_NEGOCIADO',
    'NUMERO_DE_NEGOCIOS'
]

dados_b3_final = dados_filtrados[colunas_b3].copy()

# Renomear colunas para facilitar
dados_b3_final.columns = [
    'Ticker',
    'Data',
    'Abertura',
    'Maxima',
    'Minima',
    'Fechamento',
    'Volume_Qtd',
    'Volume_R$',
    'Numero_Negocios'
]

print(f'\n  Dados B3 preparados:')
print(f'    - {len(dados_b3_final):,} registros')
print(f'    - {len(dados_b3_final.columns)} colunas')
print(f'    - Periodo: {dados_b3_final["Data"].min().strftime("%d/%m/%Y")} a {dados_b3_final["Data"].max().strftime("%d/%m/%Y")}')

# ============================================================================
# ETAPA 5: Criar dataset unificado
# ============================================================================
print('\n' + '='*70)
print('ETAPA 5: CRIANDO DATASET UNIFICADO')
print('='*70)

# Criar DataFrame unificado
dataset_unificado = dados_b3_final.copy()

print(f'\n  Dataset unificado criado:')
print(f'    - {len(dataset_unificado):,} registros')
print(f'    - {len(dataset_unificado.columns)} colunas')
print(f'    - Ativos: {sorted(dataset_unificado["Ticker"].unique())}')

# Estatísticas por ativo
print(f'\n  Estatisticas por ativo:')
for ticker in sorted(dataset_unificado['Ticker'].unique()):
    dados_ticker = dataset_unificado[dataset_unificado['Ticker'] == ticker]
    print(f'    - {ticker}: {len(dados_ticker):,} registros')
    print(f'      Periodo: {dados_ticker["Data"].min().strftime("%d/%m/%Y")} a {dados_ticker["Data"].max().strftime("%d/%m/%Y")}')

# ============================================================================
# ETAPA 6: Salvar dataset unificado
# ============================================================================
print('\n' + '='*70)
print('ETAPA 6: SALVANDO DATASET UNIFICADO')
print('='*70)

output_path = Path('data_b3/dataset_unificado.csv')
dataset_unificado.to_csv(output_path, index=False, encoding='utf-8-sig')

print(f'\n  Dataset salvo em: {output_path}')
print(f'  Tamanho: {output_path.stat().st_size / (1024*1024):.2f} MB')

# Também salvar em Parquet (mais eficiente) - opcional
try:
    output_parquet = Path('data_b3/dataset_unificado.parquet')
    dataset_unificado.to_parquet(output_parquet, index=False, compression='snappy')
    print(f'  Dataset (Parquet) salvo em: {output_parquet}')
    print(f'  Tamanho: {output_parquet.stat().st_size / (1024*1024):.2f} MB')
except ImportError:
    print(f'  Parquet nao disponivel (instale pyarrow: pip install pyarrow)')
except Exception as e:
    print(f'  Erro ao salvar Parquet: {e}')

# ============================================================================
# RESUMO FINAL
# ============================================================================
print('\n' + '='*70)
print('RESUMO FINAL')
print('='*70)

print(f'\n  Dados carregados e unificados com sucesso!')
print(f'\n  Ativos identificados (baseado na estrutura da planilha):')
print(f'    - {len(ativos_necessarios)} ativos: {sorted(ativos_necessarios)}')
print(f'\n  Arquivo B3:')
print(f'    - {len(dados_b3):,} registros totais')
print(f'    - {len(dados_filtrados):,} registros filtrados')
print(f'\n  Dataset Unificado:')
print(f'    - {len(dataset_unificado):,} registros')
print(f'    - {len(dataset_unificado.columns)} colunas')
print(f'    - Periodo: {dataset_unificado["Data"].min().strftime("%d/%m/%Y")} a {dataset_unificado["Data"].max().strftime("%d/%m/%Y")}')

print(f'\n  Arquivos gerados:')
print(f'    - {output_path}')
try:
    if output_parquet.exists():
        print(f'    - {output_parquet}')
except:
    pass

print('\n' + '='*70)
print('CONCLUIDO!')
print('='*70)

