
# Análise adicional - Meta de R$ 7-10k/mês

print("\n" + "="*100)
print("ANÁLISE DE ADEQUAÇÃO À META DE R$ 7.000 A R$ 10.000/MÊS")
print("="*100)

meta_minima = 7000
meta_maxima = 10000

print("\n### AVALIAÇÃO POR CENÁRIO E ESTRATÉGIA")

for cenario in ['Realista', 'Otimista', 'Pessimista']:
    print(f"\n{'='*100}")
    print(f"CENÁRIO: {cenario.upper()}")
    print('='*100)
    
    for estrategia in ['Sem Reinvestimento', 'Reinvest 15%', 'Reinvest 20%']:
        df_filtrado = df_resumo_completo[
            (df_resumo_completo['Cenário'] == cenario) & 
            (df_resumo_completo['Estratégia'] == estrategia)
        ]
        
        print(f"\n--- {estrategia} ---")
        
        for ano in [2025, 2026, 2027]:
            renda = df_filtrado[df_filtrado['Ano'] == ano]['Renda Mensal'].values[0]
            
            if renda >= meta_maxima:
                status = "✓✓ SUPERA META MÁXIMA"
            elif renda >= meta_minima:
                status = "✓ ATINGE META"
            else:
                status = "✗ ABAIXO DA META"
                
            print(f"{ano}: R$ {renda:,.2f}/mês - {status}")

# Criar gráfico comparativo simplificado
print("\n" + "="*100)
print("COMPARAÇÃO VISUAL - RENDA MENSAL AO LONGO DOS ANOS")
print("="*100)

for cenario in ['Realista', 'Otimista', 'Pessimista']:
    print(f"\n{cenario.upper()}:")
    print("-" * 90)
    
    df_temp = df_resumo_completo[df_resumo_completo['Cenário'] == cenario]
    
    for estrategia in ['Sem Reinvestimento', 'Reinvest 15%', 'Reinvest 20%']:
        valores = df_temp[df_temp['Estratégia'] == estrategia]['Renda Mensal'].values
        print(f"{estrategia:25s}: ", end="")
        print(" → ".join([f"R$ {v:,.0f}" for v in valores]))

# Melhor e pior caso
print("\n" + "="*100)
print("ANÁLISE DE MELHOR E PIOR CASO")
print("="*100)

melhor_renda_2025 = df_resumo_final['Renda Mensal 2025'].max()
pior_renda_2025 = df_resumo_final['Renda Mensal 2025'].min()

melhor_renda_2027 = df_resumo_final['Renda Mensal 2027'].max()
pior_renda_2027 = df_resumo_final['Renda Mensal 2027'].min()

melhor_capital_2027 = df_resumo_final['Capital Final 2027'].max()
pior_capital_2027 = df_resumo_final['Capital Final 2027'].min()

print(f"\n### EM 2025 (Primeiro Ano)")
print(f"Melhor renda mensal: R$ {melhor_renda_2025:,.2f}")
print(f"Pior renda mensal: R$ {pior_renda_2025:,.2f}")
print(f"Diferença: R$ {melhor_renda_2025 - pior_renda_2025:,.2f} ({((melhor_renda_2025/pior_renda_2025 - 1)*100):.1f}%)")

print(f"\n### EM 2027 (Terceiro Ano)")
print(f"Melhor renda mensal: R$ {melhor_renda_2027:,.2f}")
print(f"Pior renda mensal: R$ {pior_renda_2027:,.2f}")
print(f"Diferença: R$ {melhor_renda_2027 - pior_renda_2027:,.2f} ({((melhor_renda_2027/pior_renda_2027 - 1)*100):.1f}%)")

print(f"\n### CAPITAL ACUMULADO EM 2027")
print(f"Melhor caso: R$ {melhor_capital_2027:,.2f}")
print(f"Pior caso: R$ {pior_capital_2027:,.2f}")
print(f"Diferença: R$ {melhor_capital_2027 - pior_capital_2027:,.2f} ({((melhor_capital_2027/pior_capital_2027 - 1)*100):.1f}%)")

# Identificar melhor estratégia
print("\n" + "="*100)
print("RECOMENDAÇÃO ESTRATÉGICA")
print("="*100)

print("\n### PARA MAXIMIZAR RENDA MENSAL IMEDIATA:")
linha_max_renda = df_resumo_final.loc[df_resumo_final['Renda Mensal 2025'].idxmax()]
print(f"Cenário: {linha_max_renda['Cenário']}")
print(f"Estratégia: {linha_max_renda['Estratégia']}")
print(f"Renda 2025: R$ {linha_max_renda['Renda Mensal 2025']:,.2f}/mês")

print("\n### PARA MAXIMIZAR CRESCIMENTO PATRIMONIAL:")
linha_max_capital = df_resumo_final.loc[df_resumo_final['Capital Final 2027'].idxmax()]
print(f"Cenário: {linha_max_capital['Cenário']}")
print(f"Estratégia: {linha_max_capital['Estratégia']}")
print(f"Capital 2027: R$ {linha_max_capital['Capital Final 2027']:,.2f}")
print(f"Renda 2027: R$ {linha_max_capital['Renda Mensal 2027']:,.2f}/mês")

print("\n### PARA EQUILIBRAR RENDA E CRESCIMENTO:")
print("Recomendação: Cenário Realista com Reinvestimento de 15%")
linha_equilibrio = df_resumo_final[
    (df_resumo_final['Cenário'] == 'Realista') & 
    (df_resumo_final['Estratégia'] == 'Reinvest 15%')
].iloc[0]
print(f"Renda 2025: R$ {linha_equilibrio['Renda Mensal 2025']:,.2f}/mês")
print(f"Renda 2027: R$ {linha_equilibrio['Renda Mensal 2027']:,.2f}/mês")
print(f"Capital 2027: R$ {linha_equilibrio['Capital Final 2027']:,.2f}")
print(f"Total resgatado em 3 anos: R$ {linha_equilibrio['Total Resgatado 3 anos']:,.2f}")
