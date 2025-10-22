from pathlib import Path

import pandas as pd
import plotly.graph_objects as go

DATA_DIR = Path(__file__).resolve().parent / "dados"

# Load the data
df = pd.read_csv(DATA_DIR / 'projecao_completa_2026_2028.csv')

# Check unique scenarios and strategies
print("Unique Cenários:", df['Cenário'].unique())
print("Unique Estratégias:", df['Estratégia'].unique())

# Create the figure
fig = go.Figure()

# Define colors and line styles
colors = {'Realista': '#1FB8CD', 'Otimista': '#2E8B57', 'Pessimista': '#D2BA4C'}
line_styles = {'Sem Reinvestimento': 'solid', 'Reinvest 15%': 'dash', 'Reinvest 20%': 'dot'}

# Create lines for each combination
for cenario in df['Cenário'].unique():
    for estrategia in df['Estratégia'].unique():
        # Filter data for this combination
        subset = df[(df['Cenário'] == cenario) & (df['Estratégia'] == estrategia)]
        
        # Determine line style based on strategy
        line_style = 'solid'
        if '15%' in estrategia:
            line_style = 'dash'
        elif '20%' in estrategia:
            line_style = 'dot'
        
        # Add trace
        fig.add_trace(go.Scatter(
            x=subset['Ano'],
            y=subset['Renda Mensal Resgatada'],
            mode='lines+markers',
            name=f'{cenario} {estrategia}',
            line=dict(color=colors[cenario], dash=line_style, width=2),
            marker=dict(size=4)
        ))

# Add horizontal reference line at R$ 7,000
fig.add_hline(y=7000, line_dash="dash", line_color="red", 
              annotation_text="Min Target", annotation_position="bottom right")

# Update layout
fig.update_layout(
    title="Projeção Renda Mensal 2026-2028",
    xaxis_title="Year",
    yaxis_title="Monthly Income (R$)",
    legend=dict(orientation='v', yanchor='top', y=1, xanchor='left', x=1.02)
)

# Format Y-axis as Brazilian currency
fig.update_yaxes(tickformat=",.0f", tickprefix="R$ ")

# Update x-axis
fig.update_xaxes(dtick=1)

# Save the chart
fig.write_image("chart.png")
fig.write_image("chart.svg", format="svg")

print("Chart saved successfully!")