from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

DATA_DIR = Path(__file__).resolve().parent / "dados"

# Load the data
df = pd.read_csv(DATA_DIR / 'projecao_sem_reinvestimento.csv')

# Create the figure
fig = go.Figure()

# Get unique scenarios and sort them for consistent ordering
scenarios = ['Realista', 'Otimista', 'Pessimista']
colors = ['#1FB8CD', '#2E8B57', '#D2BA4C']  # Using theme colors: cyan, green, yellow

# Add line for each scenario
for i, scenario in enumerate(scenarios):
    scenario_data = df[df['Cenário'] == scenario].sort_values('Ano')
    
    fig.add_trace(go.Scatter(
        x=scenario_data['Ano'],
        y=scenario_data['Renda Mensal Líquida'],
        mode='lines+markers+text',
        name=scenario,
        line=dict(color=colors[i], width=3),
        marker=dict(size=8, color=colors[i]),
        text=[f'R$ {val:,.0f}' for val in scenario_data['Renda Mensal Líquida']],
        textposition='top center',
        textfont=dict(size=10)
    ))

# Add horizontal reference lines
fig.add_hline(y=7000, line_dash="dash", line_color="#DB4545", 
              annotation_text="Target Min", annotation_position="bottom right")
fig.add_hline(y=10000, line_dash="dash", line_color="#DB4545",
              annotation_text="Target Max", annotation_position="top right")

# Update layout
fig.update_layout(
    title="Renda Mensal - Sem Reinvest",
    xaxis_title="Ano",
    yaxis_title="Renda Mensal (R$)",
    legend=dict(orientation='h', yanchor='bottom', y=1.05, xanchor='center', x=0.5)
)

# Format Y-axis as Brazilian currency
fig.update_yaxes(tickformat=',.0f', tickprefix='R$ ')

# Format X-axis to show years properly
fig.update_xaxes(tickmode='linear', tick0=2025, dtick=1)

# Update traces for better visibility
fig.update_traces(cliponaxis=False)

# Save the chart
fig.write_image("chart.png")
fig.write_image("chart.svg", format="svg")

print("Chart saved successfully!")