
from pathlib import Path

import numpy as np
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "dados"
DATA_DIR.mkdir(exist_ok=True)

capital_inicial = 1_000_000

# Alocação
alocacao_tesouro_ipca = 0.25
alocacao_cdb = 0.25
alocacao_lci_lca = 0.20
alocacao_fii = 0.15
alocacao_acoes = 0.10
alocacao_reserva = 0.05

# IR
ir_rf = 0.175
ir_lci_lca_2025 = 0.0  # Isento em 2025
ir_lci_lca_2026_2027 = 0.05  # 5% a partir de 2026

def calcular_projecao_sem_reinvestimento(cenario_nome, cenario_data):
    """Calcula projeção sem reinvestimento"""
    
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
        
        # Aplicar IR
        if ano == 2025:
            renda_lci_lca_liquida = renda_lci_lca_bruta  # Isento em 2025
        else:
            renda_lci_lca_liquida = renda_lci_lca_bruta * (1 - ir_lci_lca_2026_2027)
        
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
        renda_mensal_liquida = renda_anual_liquida / 12
        
        resultados.append({
            'Cenário': cenario_nome,
            'Ano': ano,
            'Capital': capital_acumulado,
            'Renda Anual Bruta': renda_anual_bruta,
            'IR Pago': ir_pago,
            'Renda Anual Líquida': renda_anual_liquida,
            'Renda Mensal Líquida': renda_mensal_liquida
        })
        
        # Capital permanece o mesmo (sem reinvestimento)
    
    return pd.DataFrame(resultados)

def calcular_projecao_com_reinvestimento(cenario_nome, cenario_data, taxa_reinvest):
    """Calcula projeção COM reinvestimento"""
    
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
        
        # Aplicar IR
        if ano == 2025:
            renda_lci_lca_liquida = renda_lci_lca_bruta
        else:
            renda_lci_lca_liquida = renda_lci_lca_bruta * (1 - ir_lci_lca_2026_2027)
        
        renda_tesouro_liquida = renda_tesouro_bruta * (1 - ir_rf)
        renda_cdb_liquida = renda_cdb_bruta * (1 - ir_rf)
        renda_fii_liquida = renda_fii_bruta
        renda_acoes_liquida = renda_acoes_bruta
        renda_reserva_liquida = renda_reserva_bruta * (1 - ir_rf)
        
        # Total
        renda_anual_bruta = (renda_tesouro_bruta + renda_cdb_bruta + renda_lci_lca_bruta + 
                             renda_fii_bruta + renda_acoes_bruta + renda_reserva_bruta)
        renda_anual_liquida = (renda_tesouro_liquida + renda_cdb_liquida + renda_lci_lca_liquida + 
                               renda_fii_liquida + renda_acoes_liquida + renda_reserva_liquida)
        
        ir_pago = renda_anual_bruta - renda_anual_liquida
        renda_mensal_liquida = renda_anual_liquida / 12
        
        # Calcular valores para resgate e reinvestimento
        valor_reinvestido = renda_anual_liquida * taxa_reinvest
        valor_resgatado = renda_anual_liquida - valor_reinvestido
        renda_mensal_resgatada = valor_resgatado / 12
        
        resultados.append({
            'Cenário': f"{cenario_nome} - Reinvest {int(taxa_reinvest*100)}%",
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

# Carregar cenários
df_realista = pd.DataFrame(cenario_realista)
df_otimista = pd.DataFrame(cenario_otimista)
df_pessimista = pd.DataFrame(cenario_pessimista)

# PROJEÇÕES SEM REINVESTIMENTO
print("\n" + "="*90)
print("PROJEÇÃO 1: SEM REINVESTIMENTO (Resgate de 100% da renda)")
print("="*90)

proj_realista_sem = calcular_projecao_sem_reinvestimento("Realista", df_realista)
proj_otimista_sem = calcular_projecao_sem_reinvestimento("Otimista", df_otimista)
proj_pessimista_sem = calcular_projecao_sem_reinvestimento("Pessimista", df_pessimista)

df_sem_reinvest = pd.concat([proj_realista_sem, proj_otimista_sem, proj_pessimista_sem])

print("\n### TODAS AS PROJEÇÕES - SEM REINVESTIMENTO")
print(df_sem_reinvest.to_string(index=False))

# Salvando
df_sem_reinvest.to_csv(DATA_DIR / 'projecao_sem_reinvestimento.csv', index=False, encoding='utf-8-sig')

print("\n" + "="*90)
print("RESUMO - RENDA MENSAL LÍQUIDA (SEM REINVESTIMENTO)")
print("="*90)
resumo_sem = df_sem_reinvest.pivot(index='Ano', columns='Cenário', values='Renda Mensal Líquida')
print(resumo_sem.to_string())
