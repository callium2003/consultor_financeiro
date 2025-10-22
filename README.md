# Site de Análise de Investimentos

## 📋 Descrição

Site completo e profissional contendo análise detalhada de investimentos para geração de renda passiva de R$ 7.000 a R$ 10.000 mensais com capital de R$ 1 milhão.

## 🎯 Conteúdo Incluído

### Análises Completas
- ✅ Carteira recomendada com R$ 1 milhão (alocação e impostos)
- ✅ Projeções financeiras 2026-2028 (3 cenários: Realista, Otimista, Pessimista)
- ✅ Análise tributária detalhada (alíquotas efetivas, economia com isentos)
- ✅ Comparação: Imóvel alugado vs Vender e investir
- ✅ Recomendações estratégicas e passo a passo

### Visualizações
- 📊 5 gráficos profissionais incorporados
- 📈 Tabelas interativas com dados reais
- 💡 Cards informativos e comparativos
- 📱 Design 100% responsivo (mobile-first)

## 🚀 Como Usar

### Opção 1: Abrir Localmente
1. Baixe os 3 arquivos:
   - `index.html`
   - `styles.css`
   - `script.js`

2. Coloque todos na mesma pasta

3. Abra `index.html` no navegador

### Opção 2: Hospedar Online
Você pode hospedar gratuitamente em:
- **GitHub Pages** (recomendado)
- **Netlify**
- **Vercel**
- **Cloudflare Pages**

#### Passo a passo GitHub Pages:
```bash
1. Crie um repositório no GitHub
2. Faça upload dos 3 arquivos
3. Vá em Settings > Pages
4. Selecione branch "main" e pasta "root"
5. Salve e aguarde alguns minutos
6. Seu site estará em: https://seu-usuario.github.io/nome-repo
```

## 📁 Estrutura de Arquivos

```
analise-investimentos/
├── index.html          # Página principal (HTML5 semântico)
├── styles.css          # Estilos modernos (Flexbox/Grid)
├── script.js           # Interatividade (JavaScript vanilla)
├── README.md           # Este arquivo
└── dados/              # (opcional) Pasta para arquivos CSV
    ├── carteira_detalhada_com_impostos.csv
    ├── tabela_resumo_final_2026_2028.csv
    ├── totais_impostos_por_cenario_ano.csv
    ├── comparacao_alugar_vs_investir.csv
    └── projecao_completa_2026_2028.csv
```

## 🎨 Seções do Site

### 1. Hero Section
- Título principal
- Estatísticas principais em destaque
- Call-to-action

### 2. Resumo Executivo
- Objetivo viável
- Projeção realista
- Estratégia otimizada

### 3. Carteira Recomendada
- Gráfico de alocação (pizza)
- Tabela de composição por ativo
- Destaque para vantagens tributárias

### 4. Projeções 2026-2028
- Gráfico de evolução da renda mensal
- 3 cards de cenários (Realista, Otimista, Pessimista)
- Premissas macroeconômicas

### 5. Análise Tributária
- Gráfico de composição (renda líquida vs impostos)
- Tabela de alíquotas efetivas
- Economia com ativos isentos

### 6. Imóvel vs Investir
- Gráfico comparativo
- Cards lado a lado com prós/contras
- Análise de breakeven

### 7. Recomendações
- Estratégia recomendada
- Passo a passo de implementação
- Cronograma de rendimentos

## 🛠️ Tecnologias Utilizadas

- **HTML5**: Estrutura semântica moderna
- **CSS3**: Flexbox, Grid, Animações, Variáveis CSS
- **JavaScript**: Vanilla JS (sem frameworks)
- **Google Fonts**: Inter (tipografia profissional)
- **Design System**: Paleta de cores consistente

## 🎨 Paleta de Cores

```css
--primary: #1e3a8a (Azul Escuro)
--secondary: #10b981 (Verde)
--danger: #ef4444 (Vermelho)
--warning: #f59e0b (Amarelo)
--info: #3b82f6 (Azul Claro)
--gray-50 a 900: Escala de cinzas
```

## ✨ Recursos Especiais

### Responsividade
- ✅ Desktop (1200px+)
- ✅ Tablet (768px - 1199px)
- ✅ Mobile (< 768px)

### Interatividade
- Menu hambúrguer mobile
- Scroll suave entre seções
- Animações ao rolar a página
- Active state na navegação
- Calculadora de comparação

### Acessibilidade
- Semântica HTML5
- Contraste adequado (WCAG AA)
- Navegação por teclado
- Textos alternativos

### Performance
- CSS otimizado
- JavaScript vanilla (leve)
- Imagens dos gráficos via URL
- Sem dependências externas pesadas

## 📱 Compatibilidade

### Navegadores Suportados
- ✅ Chrome 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Edge 90+
- ✅ Opera 76+

### Dispositivos
- ✅ Desktop/Laptop
- ✅ Tablet (iPad, Android)
- ✅ Smartphone (iOS, Android)

## 🔧 Personalização

### Alterar Cores
Edite as variáveis CSS no início do `styles.css`:
```css
:root {
    --primary: #1e3a8a;
    --secondary: #10b981;
    /* ... outras cores ... */
}
```

### Adicionar Novas Seções
1. Copie estrutura de uma seção existente no `index.html`
2. Adicione novo link no menu
3. Ajuste estilos no `styles.css` se necessário

### Incluir Arquivos CSV
1. Crie pasta `dados/`
2. Adicione os arquivos CSV
3. Crie links de download no HTML:
```html
<a href="dados/carteira_detalhada.csv" download>Baixar CSV</a>
```

## 📊 Dados e Fontes

Todos os dados são baseados em:
- **Boletim Focus** - Banco Central do Brasil (Out/2025)
- **Tesouro Direto** - Taxas atualizadas
- **B3** - Bolsa de Valores (FIIs e Ações)
- **Receita Federal** - Legislação tributária vigente

## 🚧 Melhorias Futuras (Opcional)

### Funcionalidades Adicionais
- [ ] Calculadora interativa de renda
- [ ] Simulador de cenários personalizados
- [ ] Gráficos dinâmicos com Chart.js
- [ ] Exportação de relatório em PDF
- [ ] Modo escuro (dark mode)
- [ ] Comparação com outros valores de capital
- [ ] Newsletter para atualizações

### Integrações
- [ ] Google Analytics para métricas
- [ ] Chatbot para dúvidas frequentes
- [ ] Formulário de contato
- [ ] Compartilhamento em redes sociais

## 📄 Licença

Este projeto é de código aberto e pode ser usado livremente para fins educacionais e pessoais.

## 📞 Suporte

Para dúvidas ou sugestões sobre o site:
- Abra uma issue no GitHub
- Envie email para: contato@exemplo.com

## ⚠️ Aviso Legal

**Importante:** Este site contém análise financeira para fins educacionais e informativos. Não constitui recomendação de investimento. Consulte sempre um profissional certificado antes de tomar decisões financeiras.

---

**Desenvolvido com 💰 para planejamento financeiro inteligente**

Data da Análise: Outubro 2025  
Última Atualização: Outubro 2025