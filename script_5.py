
from pathlib import Path

import numpy as np
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "dados"
DATA_DIR.mkdir(exist_ok=True)

# CAPITAL INICIAL PERMANECE R$ 1 MILHÃO
capital_inicial = 1_000_000

# PROJEÇÕES COMEÇANDO EM 2026 (ATÉ 2028)
# Fonte: Boletim Focus - Banco Central

# CENÁRIO 1: REALISTA (baseado no Focus)
cenario_realista_2026 = {
    'ano': [2026, 2027, 2028],
    'selic': [0.1225, 0.1050, 0.1000],
    'ipca': [0.0427, 0.0383, 0.0360],
    'tesouro_ipca_juro_real': [0.065, 0.060, 0.058],
    'cdb_percentual_cdi': [1.00, 1.00, 1.00],
    'lci_lca_percentual_cdi': [0.90, 0.90, 0.90],
    'fii_dy': [0.095, 0.10, 0.105],
    'acoes_dy': [0.09, 0.095, 0.10],
}

# CENÁRIO 2: OTIMISTA
cenario_otimista_2026 = {
    'ano': [2026, 2027, 2028],
    'selic': [0.11, 0.09, 0.085],
    'ipca': [0.0380, 0.0340, 0.0320],
    'tesouro_ipca_juro_real': [0.070, 0.065, 0.062],
    'cdb_percentual_cdi': [1.00, 1.00, 1.00],
    'lci_lca_percentual_cdi': [0.90, 0.90, 0.90],
    'fii_dy': [0.105, 0.115, 0.125],
    'acoes_dy': [0.10, 0.11, 0.12],
}

# CENÁRIO 3: PESSIMISTA
cenario_pessimista_2026 = {
    'ano': [2026, 2027, 2028],
    'selic': [0.14, 0.125, 0.12],
    'ipca': [0.0480, 0.0450, 0.0420],
    'tesouro_ipca_juro_real': [0.060, 0.055, 0.052],
    'cdb_percentual_cdi': [1.00, 1.00, 1.00],
    'lci_lca_percentual_cdi': [0.90, 0.90, 0.90],
    'fii_dy': [0.085, 0.09, 0.095],
    'acoes_dy': [0.08, 0.085, 0.09],
}

df_realista_2026 = pd.DataFrame(cenario_realista_2026)
df_otimista_2026 = pd.DataFrame(cenario_otimista_2026)
df_pessimista_2026 = pd.DataFrame(cenario_pessimista_2026)

# Alocação mantida
alocacao_tesouro_ipca = 0.25
alocacao_cdb = 0.25
alocacao_lci_lca = 0.20
alocacao_fii = 0.15
alocacao_acoes = 0.10
alocacao_reserva = 0.05

# IR
ir_rf = 0.175
ir_lci_lca = 0.05  # 5% a partir de 2026

def calcular_projecao_2026(cenario_nome, cenario_data, taxa_reinvest=0):
    """Calcula projeção a partir de 2026"""
    
    resultados = []
    capital_acumulado = capital_inicial
    
    for i, row in cenario_data.iterrows():
        ano = int(row['ano'])
        selic = row['selic']
        ipca = row['ipca']
        tesouro_juro_real = row['tesouro_ipca_juro_real']
        cdb_perc = row['cdb_percentual_cdi']
        lci_perc = row['lci_lca_percentual_cdi']
        fii_dy = row['fii_dy']
        acoes_dy = row['acoes_dy']
        
        # Rentabilidade nominal do Tesouro IPCA+
        rent_tesouro = (1 + ipca) * (1 + tesouro_juro_real) - 1
        
        # Renda bruta por ativo
        renda_tesouro_bruta = capital_acumulado * alocacao_tesouro_ipca * rent_tesouro
        renda_cdb_bruta = capital_acumulado * alocacao_cdb * (selic * cdb_perc)
        renda_lci_lca_bruta = capital_acumulado * alocacao_lci_lca * (selic * lci_perc)
        renda_fii_bruta = capital_acumulado * alocacao_fii * fii_dy
        renda_acoes_bruta = capital_acumulado * alocacao_acoes * acoes_dy
        renda_reserva_bruta = capital_acumulado * alocacao_reserva * selic
        
        # Aplicar IR (LCI/LCA com 5% a partir de 2026)
        renda_lci_lca_liquida = renda_lci_lca_bruta * (1 - ir_lci_lca)
        renda_tesouro_liquida = renda_tesouro_bruta * (1 - ir_rf)
        renda_cdb_liquida = renda_cdb_bruta * (1 - ir_rf)
        renda_fii_liquida = renda_fii_bruta  # Isento
        renda_acoes_liquida = renda_acoes_bruta  # Isento
        renda_reserva_liquida = renda_reserva_bruta * (1 - ir_rf)
        
        # Total
        renda_anual_bruta = (renda_tesouro_bruta + renda_cdb_bruta + renda_lci_lca_bruta + 
                             renda_fii_bruta + renda_acoes_bruta + renda_reserva_bruta)
        renda_anual_liquida = (renda_tesouro_liquida + renda_cdb_liquida + renda_lci_lca_liquida + 
                               renda_fii_liquida + renda_acoes_liquida + renda_reserva_liquida)
        
        ir_pago = renda_anual_bruta - renda_anual_liquida
        
        # Calcular valores para resgate e reinvestimento
        valor_reinvestido = renda_anual_liquida * taxa_reinvest
        valor_resgatado = renda_anual_liquida - valor_reinvestido
        renda_mensal_resgatada = valor_resgatado / 12
        
        if taxa_reinvest == 0:
            estrategia = "Sem Reinvestimento"
        else:
            estrategia = f"Reinvest {int(taxa_reinvest*100)}%"
        
        resultados.append({
            'Cenário': cenario_nome,
            'Estratégia': estrategia,
            'Ano': ano,
            'Capital Inicial': capital_acumulado,
            'Renda Anual Bruta': renda_anual_bruta,
            'IR Pago': ir_pago,
            'Renda Anual Líquida': renda_anual_liquida,
            'Valor Reinvestido': valor_reinvestido,
            'Valor Resgatado': valor_resgatado,
            'Capital Final': capital_acumulado + valor_reinvestido,
            'Renda Mensal Resgatada': renda_mensal_resgatada
        })
        
        # Atualizar capital para próximo ano
        capital_acumulado = capital_acumulado + valor_reinvestido
    
    return pd.DataFrame(resultados)

print("="*100)
print("PROJEÇÃO DE INVESTIMENTOS - R$ 1 MILHÃO")
print("PERÍODO: 2026 A 2028 (3 ANOS)")
print("="*100)

print("\n" + "="*100)
print("PREMISSAS MACROECONÔMICAS - CENÁRIOS (2026-2028)")
print("="*100)

print("\n### CENÁRIO REALISTA (Base: Boletim Focus - BC)")
print(df_realista_2026.to_string(index=False))

print("\n### CENÁRIO OTIMISTA (Inflação controlada, juros caem mais)")
print(df_otimista_2026.to_string(index=False))

print("\n### CENÁRIO PESSIMISTA (Inflação persistente, juros altos)")
print(df_pessimista_2026.to_string(index=False))

# Salvando premissas
df_realista_2026.to_csv(DATA_DIR / 'premissas_2026_realista.csv', index=False, encoding='utf-8-sig')
df_otimista_2026.to_csv(DATA_DIR / 'premissas_2026_otimista.csv', index=False, encoding='utf-8-sig')
df_pessimista_2026.to_csv(DATA_DIR / 'premissas_2026_pessimista.csv', index=False, encoding='utf-8-sig')

# GERAR TODAS AS PROJEÇÕES
todos_resultados = []

for cenario_nome, cenario_data in [
    ('Realista', df_realista_2026),
    ('Otimista', df_otimista_2026),
    ('Pessimista', df_pessimista_2026)
]:
    for taxa in [0, 0.15, 0.20]:
        resultado = calcular_projecao_2026(cenario_nome, cenario_data, taxa)
        todos_resultados.append(resultado)

df_todos_resultados = pd.concat(todos_resultados, ignore_index=True)

# Salvar tudo
df_todos_resultados.to_csv(DATA_DIR / 'projecao_completa_2026_2028.csv', index=False, encoding='utf-8-sig')

print("\n" + "="*100)
print("RESUMO - RENDA MENSAL RESGATADA POR ANO, CENÁRIO E ESTRATÉGIA")
print("="*100)

for cenario in ['Realista', 'Otimista', 'Pessimista']:
    print(f"\n{'='*100}")
    print(f"CENÁRIO: {cenario.upper()}")
    print('='*100)
    
    df_temp = df_todos_resultados[df_todos_resultados['Cenário'] == cenario]
    pivot = df_temp.pivot(index='Ano', columns='Estratégia', values='Renda Mensal Resgatada')
    print(pivot.to_string())

print("\n" + "="*100)
print("CAPITAL ACUMULADO AO FINAL DE 2028")
print("="*100)

for cenario in ['Realista', 'Otimista', 'Pessimista']:
    print(f"\n{cenario.upper()}:")
    df_temp = df_todos_resultados[(df_todos_resultados['Cenário'] == cenario) & (df_todos_resultados['Ano'] == 2028)]
    pivot_capital = df_temp.set_index('Estratégia')['Capital Final']
    print(pivot_capital.to_string())
