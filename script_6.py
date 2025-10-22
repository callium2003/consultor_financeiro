
# Análise de adequação à meta e resumo final 2026-2028

print("\n" + "="*100)
print("ANÁLISE DE ADEQUAÇÃO À META DE R$ 7.000 A R$ 10.000/MÊS (2026-2028)")
print("="*100)

meta_minima = 7000
meta_maxima = 10000

for cenario in ['Realista', 'Otimista', 'Pessimista']:
    print(f"\n{'='*100}")
    print(f"CENÁRIO: {cenario.upper()}")
    print('='*100)
    
    for estrategia in ['Sem Reinvestimento', 'Reinvest 15%', 'Reinvest 20%']:
        df_filtrado = df_todos_resultados[
            (df_todos_resultados['Cenário'] == cenario) & 
            (df_todos_resultados['Estratégia'] == estrategia)
        ]
        
        print(f"\n--- {estrategia} ---")
        
        for ano in [2026, 2027, 2028]:
            renda = df_filtrado[df_filtrado['Ano'] == ano]['Renda Mensal Resgatada'].values[0]
            
            if renda >= meta_maxima:
                status = "✓✓ SUPERA META MÁXIMA"
            elif renda >= meta_minima:
                status = "✓ ATINGE META"
            else:
                status = "✗ ABAIXO DA META"
                
            print(f"{ano}: R$ {renda:,.2f}/mês - {status}")

# Criar tabela resumo final
print("\n" + "="*100)
print("TABELA RESUMO FINAL (2026-2028)")
print("="*100)

resumo_final_2026 = []
for cenario in ['Realista', 'Otimista', 'Pessimista']:
    for estrategia in ['Sem Reinvestimento', 'Reinvest 15%', 'Reinvest 20%']:
        df_filtrado = df_todos_resultados[
            (df_todos_resultados['Cenário'] == cenario) & 
            (df_todos_resultados['Estratégia'] == estrategia)
        ]
        
        if len(df_filtrado) > 0:
            renda_2026 = df_filtrado[df_filtrado['Ano'] == 2026]['Renda Mensal Resgatada'].values[0]
            renda_2027 = df_filtrado[df_filtrado['Ano'] == 2027]['Renda Mensal Resgatada'].values[0]
            renda_2028 = df_filtrado[df_filtrado['Ano'] == 2028]['Renda Mensal Resgatada'].values[0]
            capital_final_2028 = df_filtrado[df_filtrado['Ano'] == 2028]['Capital Final'].values[0]
            
            resumo_final_2026.append({
                'Cenário': cenario,
                'Estratégia': estrategia,
                'Renda Mensal 2026': renda_2026,
                'Renda Mensal 2027': renda_2027,
                'Renda Mensal 2028': renda_2028,
                'Capital Final 2028': capital_final_2028,
                'Total Resgatado 3 anos': (renda_2026 * 12) + (renda_2027 * 12) + (renda_2028 * 12)
            })

df_resumo_final_2026 = pd.DataFrame(resumo_final_2026)
print(df_resumo_final_2026.to_string(index=False))

df_resumo_final_2026.to_csv('tabela_resumo_final_2026_2028.csv', index=False, encoding='utf-8-sig')

# Análise de melhor e pior caso
print("\n" + "="*100)
print("ANÁLISE DE MELHOR E PIOR CASO (2026-2028)")
print("="*100)

melhor_renda_2026 = df_resumo_final_2026['Renda Mensal 2026'].max()
pior_renda_2026 = df_resumo_final_2026['Renda Mensal 2026'].min()

melhor_renda_2028 = df_resumo_final_2026['Renda Mensal 2028'].max()
pior_renda_2028 = df_resumo_final_2026['Renda Mensal 2028'].min()

melhor_capital_2028 = df_resumo_final_2026['Capital Final 2028'].max()
pior_capital_2028 = df_resumo_final_2026['Capital Final 2028'].min()

melhor_total_resgate = df_resumo_final_2026['Total Resgatado 3 anos'].max()

print(f"\n### EM 2026 (Primeiro Ano)")
print(f"Melhor renda mensal: R$ {melhor_renda_2026:,.2f}")
print(f"Pior renda mensal: R$ {pior_renda_2026:,.2f}")
print(f"Diferença: R$ {melhor_renda_2026 - pior_renda_2026:,.2f} ({((melhor_renda_2026/pior_renda_2026 - 1)*100):.1f}%)")

print(f"\n### EM 2028 (Terceiro Ano)")
print(f"Melhor renda mensal: R$ {melhor_renda_2028:,.2f}")
print(f"Pior renda mensal: R$ {pior_renda_2028:,.2f}")
print(f"Diferença: R$ {melhor_renda_2028 - pior_renda_2028:,.2f} ({((melhor_renda_2028/pior_renda_2028 - 1)*100):.1f}%)")

print(f"\n### CAPITAL ACUMULADO EM 2028")
print(f"Melhor caso: R$ {melhor_capital_2028:,.2f}")
print(f"Pior caso: R$ {pior_capital_2028:,.2f}")
print(f"Diferença: R$ {melhor_capital_2028 - pior_capital_2028:,.2f} ({((melhor_capital_2028/pior_capital_2028 - 1)*100):.1f}%)")

print(f"\n### TOTAL RESGATADO EM 3 ANOS")
print(f"Maior valor: R$ {melhor_total_resgate:,.2f}")

# Recomendação estratégica
print("\n" + "="*100)
print("RECOMENDAÇÃO ESTRATÉGICA (2026-2028)")
print("="*100)

print("\n### PARA MAXIMIZAR RENDA MENSAL IMEDIATA:")
linha_max_renda = df_resumo_final_2026.loc[df_resumo_final_2026['Renda Mensal 2026'].idxmax()]
print(f"Cenário: {linha_max_renda['Cenário']}")
print(f"Estratégia: {linha_max_renda['Estratégia']}")
print(f"Renda 2026: R$ {linha_max_renda['Renda Mensal 2026']:,.2f}/mês")
print(f"Renda 2028: R$ {linha_max_renda['Renda Mensal 2028']:,.2f}/mês")

print("\n### PARA MAXIMIZAR CRESCIMENTO PATRIMONIAL:")
linha_max_capital = df_resumo_final_2026.loc[df_resumo_final_2026['Capital Final 2028'].idxmax()]
print(f"Cenário: {linha_max_capital['Cenário']}")
print(f"Estratégia: {linha_max_capital['Estratégia']}")
print(f"Capital 2028: R$ {linha_max_capital['Capital Final 2028']:,.2f}")
print(f"Renda 2028: R$ {linha_max_capital['Renda Mensal 2028']:,.2f}/mês")

print("\n### PARA EQUILIBRAR RENDA E CRESCIMENTO:")
print("Recomendação: Cenário Realista com Reinvestimento de 15%")
linha_equilibrio = df_resumo_final_2026[
    (df_resumo_final_2026['Cenário'] == 'Realista') & 
    (df_resumo_final_2026['Estratégia'] == 'Reinvest 15%')
].iloc[0]
print(f"Renda 2026: R$ {linha_equilibrio['Renda Mensal 2026']:,.2f}/mês")
print(f"Renda 2028: R$ {linha_equilibrio['Renda Mensal 2028']:,.2f}/mês")
print(f"Capital 2028: R$ {linha_equilibrio['Capital Final 2028']:,.2f}")
print(f"Total resgatado em 3 anos: R$ {linha_equilibrio['Total Resgatado 3 anos']:,.2f}")

# Comparação visual
print("\n" + "="*100)
print("COMPARAÇÃO VISUAL - RENDA MENSAL AO LONGO DOS ANOS (2026-2028)")
print("="*100)

for cenario in ['Realista', 'Otimista', 'Pessimista']:
    print(f"\n{cenario.upper()}:")
    print("-" * 90)
    
    df_temp = df_todos_resultados[df_todos_resultados['Cenário'] == cenario]
    
    for estrategia in ['Sem Reinvestimento', 'Reinvest 15%', 'Reinvest 20%']:
        valores = df_temp[df_temp['Estratégia'] == estrategia]['Renda Mensal Resgatada'].values
        print(f"{estrategia:25s}: ", end="")
        print(" → ".join([f"R$ {v:,.0f}" for v in valores]))

print("\n" + "="*100)
print("ARQUIVOS CSV GERADOS COM SUCESSO!")
print("="*100)
