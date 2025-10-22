
from pathlib import Path

import numpy as np
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "dados"
DATA_DIR.mkdir(exist_ok=True)

# CAPITAL INICIAL ATUALIZADO
capital_inicial = 1_000_000  # R$ 1 milhão

# PROJEÇÕES DO BOLETIM FOCUS (Outubro 2025)
# Fonte: Banco Central - Focus

# Selic projetada
selic_2025 = 0.15  # 15%
selic_2026 = 0.1225  # 12.25%
selic_2027 = 0.1050  # 10.50%
selic_2028 = 0.1000  # 10.00%

# IPCA projetado
ipca_2025 = 0.0470  # 4.70%
ipca_2026 = 0.0427  # 4.27%
ipca_2027 = 0.0383  # 3.83%
ipca_2028 = 0.0360  # 3.60%

# CENÁRIO 1: REALISTA (baseado no Focus)
# Rentabilidades esperadas por ativo
cenario_realista = {
    'ano': [2025, 2026, 2027],
    'selic': [0.15, 0.1225, 0.1050],
    'ipca': [0.0470, 0.0427, 0.0383],
    'tesouro_ipca_juro_real': [0.075, 0.065, 0.060],  # Juro real esperado
    'cdb_percentual_cdi': [1.00, 1.00, 1.00],  # 100% CDI
    'lci_lca_percentual_cdi': [0.90, 0.90, 0.90],  # 90% CDI
    'fii_dy': [0.09, 0.095, 0.10],  # DY esperado (melhora com queda de juros)
    'acoes_dy': [0.08, 0.09, 0.095],  # DY esperado
}

# CENÁRIO 2: OTIMISTA (inflação controlada, juros caem mais rápido)
cenario_otimista = {
    'ano': [2025, 2026, 2027],
    'selic': [0.15, 0.11, 0.09],  # Queda mais agressiva
    'ipca': [0.0450, 0.0380, 0.0340],  # Inflação controlada
    'tesouro_ipca_juro_real': [0.075, 0.070, 0.065],
    'cdb_percentual_cdi': [1.00, 1.00, 1.00],
    'lci_lca_percentual_cdi': [0.90, 0.90, 0.90],
    'fii_dy': [0.09, 0.105, 0.115],  # Maior valorização
    'acoes_dy': [0.08, 0.10, 0.11],  # Melhor cenário corporativo
}

# CENÁRIO 3: PESSIMISTA (inflação persistente, juros altos por mais tempo)
cenario_pessimista = {
    'ano': [2025, 2026, 2027],
    'selic': [0.15, 0.14, 0.125],  # Juros permanecem elevados
    'ipca': [0.0500, 0.0480, 0.0450],  # Inflação acima da meta
    'tesouro_ipca_juro_real': [0.075, 0.060, 0.055],
    'cdb_percentual_cdi': [1.00, 1.00, 1.00],
    'lci_lca_percentual_cdi': [0.90, 0.90, 0.90],
    'fii_dy': [0.09, 0.085, 0.09],  # Menos valorização
    'acoes_dy': [0.08, 0.08, 0.085],  # Cenário corporativo mais fraco
}

df_realista = pd.DataFrame(cenario_realista)
df_otimista = pd.DataFrame(cenario_otimista)
df_pessimista = pd.DataFrame(cenario_pessimista)

# ALOCAÇÃO RECOMENDADA (Conservador-Moderado)
alocacao = {
    'Tesouro IPCA+ Juros Semestrais': 0.25,
    'CDB 100% CDI': 0.25,
    'LCI/LCA 90% CDI': 0.20,
    'FIIs': 0.15,
    'Ações Dividendos': 0.10,
    'Reserva Emergência': 0.05
}

# Alíquotas de IR
ir_renda_fixa = 0.175  # 17.5%
ir_lci_lca = 0.05  # 5% a partir de 2026

print("="*90)
print("ANÁLISE DE INVESTIMENTOS - R$ 1 MILHÃO")
print("PROJEÇÃO PARA 3 ANOS (2025-2027)")
print("="*90)

print("\n" + "="*90)
print("PREMISSAS MACROECONÔMICAS - CENÁRIOS")
print("="*90)

print("\n### CENÁRIO REALISTA (Base: Boletim Focus - BC)")
print(df_realista.to_string(index=False))

print("\n### CENÁRIO OTIMISTA (Inflação controlada, juros caem mais)")
print(df_otimista.to_string(index=False))

print("\n### CENÁRIO PESSIMISTA (Inflação persistente, juros altos)")
print(df_pessimista.to_string(index=False))

# Salvando premissas
df_realista.to_csv(DATA_DIR / 'premissas_cenario_realista.csv', index=False, encoding='utf-8-sig')
df_otimista.to_csv(DATA_DIR / 'premissas_cenario_otimista.csv', index=False, encoding='utf-8-sig')
df_pessimista.to_csv(DATA_DIR / 'premissas_cenario_pessimista.csv', index=False, encoding='utf-8-sig')

print("\n" + "="*90)
print("ALOCAÇÃO RECOMENDADA DA CARTEIRA")
print("="*90)
for ativo, percentual in alocacao.items():
    valor = capital_inicial * percentual
    print(f"{ativo}: {percentual*100:.0f}% = R$ {valor:,.2f}")
