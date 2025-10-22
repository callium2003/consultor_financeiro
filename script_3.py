
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent / "dados"
DATA_DIR.mkdir(exist_ok=True)

# RESUMO COMPARATIVO - Corrigido
print("\n" + "="*100)
print("RESUMO COMPARATIVO - RENDA MENSAL RESGATADA")
print("="*100)

# Criar resumo consolidado
resumo_completo = []

# Sem reinvestimento
for _, row in df_sem_reinvest.iterrows():
    resumo_completo.append({
        'Cenário': row['Cenário'],
        'Estratégia': 'Sem Reinvestimento',
        'Ano': row['Ano'],
        'Capital': row['Capital'],
        'Renda Mensal': row['Renda Mensal Líquida']
    })

# Com 15%
for _, row in df_reinvest_15.iterrows():
    cenario_base = row['Cenário'].replace(' - Reinvest 15%', '')
    resumo_completo.append({
        'Cenário': cenario_base,
        'Estratégia': 'Reinvest 15%',
        'Ano': row['Ano'],
        'Capital': row['Capital Final'],
        'Renda Mensal': row['Renda Mensal Resgatada']
    })

# Com 20%
for _, row in df_reinvest_20.iterrows():
    cenario_base = row['Cenário'].replace(' - Reinvest 20%', '')
    resumo_completo.append({
        'Cenário': cenario_base,
        'Estratégia': 'Reinvest 20%',
        'Ano': row['Ano'],
        'Capital': row['Capital Final'],
        'Renda Mensal': row['Renda Mensal Resgatada']
    })

df_resumo_completo = pd.DataFrame(resumo_completo)
df_resumo_completo.to_csv(DATA_DIR / 'resumo_comparativo_completo.csv', index=False, encoding='utf-8-sig')

# Tabela pivotada para melhor visualização
print("\n### RENDA MENSAL RESGATADA POR ANO E CENÁRIO")
for cenario in ['Realista', 'Otimista', 'Pessimista']:
    print(f"\n--- CENÁRIO {cenario.upper()} ---")
    df_temp = df_resumo_completo[df_resumo_completo['Cenário'] == cenario]
    pivot = df_temp.pivot(index='Ano', columns='Estratégia', values='Renda Mensal')
    print(pivot.to_string())

print("\n" + "="*100)
print("CAPITAL ACUMULADO AO FINAL DE 2027")
print("="*100)
for cenario in ['Realista', 'Otimista', 'Pessimista']:
    print(f"\n--- CENÁRIO {cenario.upper()} ---")
    df_temp = df_resumo_completo[(df_resumo_completo['Cenário'] == cenario) & (df_resumo_completo['Ano'] == 2027)]
    pivot_capital = df_temp.set_index('Estratégia')['Capital']
    print(pivot_capital.to_string())

# Criar tabela resumo final
print("\n" + "="*100)
print("TABELA RESUMO FINAL - COMPARAÇÃO DE TODAS AS ESTRATÉGIAS")
print("="*100)

resumo_final = []
for cenario in ['Realista', 'Otimista', 'Pessimista']:
    for estrategia in ['Sem Reinvestimento', 'Reinvest 15%', 'Reinvest 20%']:
        df_filtrado = df_resumo_completo[
            (df_resumo_completo['Cenário'] == cenario) & 
            (df_resumo_completo['Estratégia'] == estrategia)
        ]
        
        if len(df_filtrado) > 0:
            renda_2025 = df_filtrado[df_filtrado['Ano'] == 2025]['Renda Mensal'].values[0]
            renda_2026 = df_filtrado[df_filtrado['Ano'] == 2026]['Renda Mensal'].values[0]
            renda_2027 = df_filtrado[df_filtrado['Ano'] == 2027]['Renda Mensal'].values[0]
            capital_final_2027 = df_filtrado[df_filtrado['Ano'] == 2027]['Capital'].values[0]
            
            resumo_final.append({
                'Cenário': cenario,
                'Estratégia': estrategia,
                'Renda Mensal 2025': renda_2025,
                'Renda Mensal 2026': renda_2026,
                'Renda Mensal 2027': renda_2027,
                'Capital Final 2027': capital_final_2027,
                'Total Resgatado 3 anos': (renda_2025 * 12) + (renda_2026 * 12) + (renda_2027 * 12)
            })

df_resumo_final = pd.DataFrame(resumo_final)
print(df_resumo_final.to_string(index=False))

df_resumo_final.to_csv(DATA_DIR / 'tabela_resumo_final.csv', index=False, encoding='utf-8-sig')

print("\n" + "="*100)
print("Arquivos CSV gerados com sucesso!")
print("="*100)
