
# PROJEÇÕES COM REINVESTIMENTO - 15% e 20%

print("\n" + "="*90)
print("PROJEÇÃO 2: COM REINVESTIMENTO DE 15% DA RENDA")
print("="*90)

proj_realista_15 = calcular_projecao_com_reinvestimento("Realista", df_realista, 0.15)
proj_otimista_15 = calcular_projecao_com_reinvestimento("Otimista", df_otimista, 0.15)
proj_pessimista_15 = calcular_projecao_com_reinvestimento("Pessimista", df_pessimista, 0.15)

df_reinvest_15 = pd.concat([proj_realista_15, proj_otimista_15, proj_pessimista_15])

print("\n### PROJEÇÃO COM 15% DE REINVESTIMENTO")
print(df_reinvest_15.to_string(index=False))

# Salvando
df_reinvest_15.to_csv('projecao_reinvestimento_15pct.csv', index=False, encoding='utf-8-sig')

print("\n" + "="*90)
print("PROJEÇÃO 3: COM REINVESTIMENTO DE 20% DA RENDA")
print("="*90)

proj_realista_20 = calcular_projecao_com_reinvestimento("Realista", df_realista, 0.20)
proj_otimista_20 = calcular_projecao_com_reinvestimento("Otimista", df_otimista, 0.20)
proj_pessimista_20 = calcular_projecao_com_reinvestimento("Pessimista", df_pessimista, 0.20)

df_reinvest_20 = pd.concat([proj_realista_20, proj_otimista_20, proj_pessimista_20])

print("\n### PROJEÇÃO COM 20% DE REINVESTIMENTO")
print(df_reinvest_20.to_string(index=False))

# Salvando
df_reinvest_20.to_csv('projecao_reinvestimento_20pct.csv', index=False, encoding='utf-8-sig')

# RESUMO COMPARATIVO
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
        'Renda Mensal': row['Renda Mensal']
    })

df_resumo_completo = pd.DataFrame(resumo_completo)
df_resumo_completo.to_csv('resumo_comparativo_completo.csv', index=False, encoding='utf-8-sig')

# Tabela pivotada para melhor visualização
print("\n### RENDA MENSAL RESGATADA POR ANO E CENÁRIO")
for cenario in ['Realista', 'Otimista', 'Pessimista']:
    print(f"\n--- CENÁRIO {cenario.upper()} ---")
    df_temp = df_resumo_completo[df_resumo_completo['Cenário'] == cenario]
    pivot = df_temp.pivot(index='Ano', columns='Estratégia', values='Renda Mensal')
    print(pivot.to_string())

print("\n### CAPITAL ACUMULADO AO FINAL DE 2027")
for cenario in ['Realista', 'Otimista', 'Pessimista']:
    print(f"\n--- CENÁRIO {cenario.upper()} ---")
    df_temp = df_resumo_completo[df_resumo_completo['Cenário'] == cenario]
    pivot_capital = df_temp[df_temp['Ano'] == 2027].pivot(columns='Estratégia', values='Capital')
    print(pivot_capital.to_string(index=False))
