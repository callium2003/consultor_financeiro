// Site enhancements and simulator logic
document.addEventListener('DOMContentLoaded', function() {
    const menuToggle = document.getElementById('menuToggle');
    const navMenu = document.querySelector('.nav-menu');

    /**
     * Atualiza atributos de acessibilidade e estado visual do menu mobile.
     * @param {boolean} isOpen
     */
    const navMediaQuery = window.matchMedia ? window.matchMedia('(min-width: 769px)') : null;
    const isDesktopViewport = () => navMediaQuery ? navMediaQuery.matches : window.innerWidth >= 769;

    const setMenuState = (isOpen) => {
        if (!menuToggle || !navMenu) {
            return;
        }
        navMenu.classList.toggle('active', isOpen);
        menuToggle.setAttribute('aria-expanded', String(isOpen));
        menuToggle.setAttribute('aria-label', isOpen ? 'Fechar menu principal' : 'Abrir menu principal');

        if (!isDesktopViewport()) {
            navMenu.setAttribute('aria-hidden', String(!isOpen));
        } else {
            navMenu.removeAttribute('aria-hidden');
        }
    };

    /**
     * Ajusta automaticamente o menu quando o viewport muda (mobile ↔ desktop).
     */
    const handleNavigationBreakpoint = () => {
        if (!menuToggle || !navMenu) {
            return;
        }

        if (isDesktopViewport()) {
            navMenu.classList.remove('active');
            menuToggle.setAttribute('aria-expanded', 'false');
            menuToggle.setAttribute('aria-label', 'Abrir menu principal');
            navMenu.removeAttribute('aria-hidden');
        } else {
            const isExpanded = menuToggle.getAttribute('aria-expanded') === 'true';
            navMenu.setAttribute('aria-hidden', String(!isExpanded));
        }
    };

    if (menuToggle && navMenu) {
        handleNavigationBreakpoint();

        menuToggle.addEventListener('click', () => {
            const isExpanded = menuToggle.getAttribute('aria-expanded') === 'true';
            setMenuState(!isExpanded);
        });

        menuToggle.addEventListener('keydown', (event) => {
            if (event.key === 'Enter' || event.key === ' ') {
                event.preventDefault();
                const isExpanded = menuToggle.getAttribute('aria-expanded') === 'true';
                setMenuState(!isExpanded);
            }
        });

        const navLinks = document.querySelectorAll('.nav-menu a');
        navLinks.forEach(link => {
            link.addEventListener('click', () => {
                if (!isDesktopViewport()) {
                    setMenuState(false);
                }
            });
        });

        if (navMediaQuery) {
            if (typeof navMediaQuery.addEventListener === 'function') {
                navMediaQuery.addEventListener('change', handleNavigationBreakpoint);
            } else if (typeof navMediaQuery.addListener === 'function') {
                navMediaQuery.addListener(handleNavigationBreakpoint);
            }
        } else {
            window.addEventListener('resize', handleNavigationBreakpoint);
        }
    }

    // Smooth scroll
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    // Animate elements on scroll
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in');
            }
        });
    }, observerOptions);
    
    // Observe all cards
    document.querySelectorAll('.card').forEach(card => {
        observer.observe(card);
    });
    
    // Format numbers
    function formatCurrency(value) {
        return new Intl.NumberFormat('pt-BR', {
            style: 'currency',
            currency: 'BRL'
        }).format(value);
    }
    
    // Add tooltips to data points
    const statValues = document.querySelectorAll('.stat-value, .big-number');
    statValues.forEach(stat => {
        stat.setAttribute('title', 'Clique para mais detalhes');
    });
    
    // Print functionality
    window.printPage = function() {
        window.print();
    };
    
    // Export data functionality (placeholder)
    window.exportData = function(format) {
        alert(`Exportando dados em formato ${format}. Funcionalidade em desenvolvimento.`);
    };

    // Investment simulator
    const investmentRates = [
        { year: 2026, rate: 0.0973 },
        { year: 2027, rate: 0.0892 },
        { year: 2028, rate: 0.0874 }
    ];

    const simulatorForm = document.getElementById('simulatorForm');
    const simulatorResults = document.getElementById('simulatorResults');
    const resultsGrid = document.getElementById('simulatorResultsGrid');
    const totalWithdrawnEl = document.getElementById('simulatorTotalWithdrawn');
    const finalCapitalEl = document.getElementById('simulatorFinalCapital');
    const totalReinvestedEl = document.getElementById('simulatorTotalReinvested');
    const resetButton = document.getElementById('simulatorReset');
    const simulatorMessage = document.getElementById('simulatorMessage');
    const loadingIndicator = document.getElementById('simulatorLoading');
    const submitButton = simulatorForm ? simulatorForm.querySelector('.simulator-submit') : null;

    const clearFormMessage = () => {
        if (simulatorMessage) {
            simulatorMessage.textContent = '';
            simulatorMessage.className = 'form-message';
        }
    };

    const displayFormMessage = (message, type = 'info') => {
        if (!simulatorMessage) {
            return;
        }
        simulatorMessage.textContent = message;
        simulatorMessage.className = `form-message form-message--${type} is-visible`;
    };

    const setLoading = (isLoading) => {
        if (loadingIndicator) {
            loadingIndicator.classList.toggle('hidden', !isLoading);
        }

        if (submitButton) {
            submitButton.disabled = isLoading;
            if (isLoading) {
                submitButton.setAttribute('aria-disabled', 'true');
            } else {
                submitButton.removeAttribute('aria-disabled');
            }
        }
    };

    if (simulatorForm && simulatorResults && resultsGrid) {
        simulatorForm.addEventListener('input', () => {
            clearFormMessage();
        });

        simulatorForm.addEventListener('submit', function(event) {
            event.preventDefault();

            const initialInvestmentValue = parseFloat(simulatorForm.initialInvestment.value);
            const reinvestmentValue = parseFloat(simulatorForm.reinvestmentRate.value);

            if (!Number.isFinite(initialInvestmentValue) || initialInvestmentValue <= 0) {
                displayFormMessage('Informe um valor inicial válido para a simulação.', 'error');
                simulatorResults.classList.add('hidden');
                simulatorForm.initialInvestment.focus();
                return;
            }

            if (!Number.isFinite(reinvestmentValue)) {
                displayFormMessage('Informe um percentual de reinvestimento válido.', 'error');
                simulatorResults.classList.add('hidden');
                simulatorForm.reinvestmentRate.focus();
                return;
            }

            const sanitizedPercent = Math.min(Math.max(reinvestmentValue, 0), 100);
            const reinvestmentPercent = sanitizedPercent / 100;
            simulatorForm.reinvestmentRate.value = Number.isInteger(sanitizedPercent)
                ? sanitizedPercent
                : sanitizedPercent.toFixed(1);

            clearFormMessage();
            simulatorResults.classList.add('hidden');
            resultsGrid.innerHTML = '';
            setLoading(true);

            let currentCapital = initialInvestmentValue;
            let totalWithdrawn = 0;
            let totalReinvested = 0;
            const percentAdjusted = sanitizedPercent !== reinvestmentValue;

            window.setTimeout(() => {
                investmentRates.forEach(data => {
                    const annualReturn = currentCapital * data.rate;
                    const reinvested = annualReturn * reinvestmentPercent;
                    const withdrawn = annualReturn - reinvested;
                    const monthlyIncome = withdrawn / 12;
                    const endingCapital = currentCapital + reinvested;

                    totalWithdrawn += withdrawn;
                    totalReinvested += reinvested;
                    const ratePercent = (data.rate * 100).toFixed(2).replace('.', ',');

                    const card = document.createElement('div');
                    card.className = 'simulator-result-card';
                    card.innerHTML = `
                        <div class="result-card-header">
                            <span class="result-year">${data.year}</span>
                            <span class="result-rate">${ratePercent}% líquido</span>
                        </div>
                        <div class="result-metric">
                            <span class="result-label">Renda mensal média</span>
                            <span class="result-value">${formatCurrency(monthlyIncome)}</span>
                        </div>
                        <div class="result-metric">
                            <span class="result-label">Total líquido no ano</span>
                            <span class="result-value">${formatCurrency(withdrawn)}</span>
                        </div>
                        <div class="result-metric">
                            <span class="result-label">Reinvestimento no ano</span>
                            <span class="result-value">${formatCurrency(reinvested)}</span>
                        </div>
                        <div class="result-metric">
                            <span class="result-label">Patrimônio ao fim do ano</span>
                            <span class="result-value">${formatCurrency(endingCapital)}</span>
                        </div>
                    `;

                    resultsGrid.appendChild(card);
                    currentCapital = endingCapital;
                });

                totalWithdrawnEl.textContent = formatCurrency(totalWithdrawn);
                finalCapitalEl.textContent = formatCurrency(currentCapital);
                totalReinvestedEl.textContent = formatCurrency(totalReinvested);

                const successMessage = percentAdjusted
                    ? `Ajustamos o percentual de reinvestimento para ${sanitizedPercent}% para manter os limites de 0% a 100%.`
                    : 'Simulação concluída! Confira os resultados projetados abaixo.';

                displayFormMessage(successMessage, percentAdjusted ? 'info' : 'success');

                simulatorResults.classList.remove('hidden');
                simulatorResults.scrollIntoView({ behavior: 'smooth', block: 'start' });
                setLoading(false);
            }, 150);
        });

        if (resetButton) {
            resetButton.addEventListener('click', function() {
                simulatorForm.reset();
                resultsGrid.innerHTML = '';
                totalWithdrawnEl.textContent = '--';
                finalCapitalEl.textContent = '--';
                totalReinvestedEl.textContent = '--';
                simulatorResults.classList.add('hidden');
                simulatorForm.initialInvestment.focus();
                setLoading(false);
                clearFormMessage();
            });
        }
    }

    // Add active state to navigation based on scroll position
    window.addEventListener('scroll', function() {
        const sections = document.querySelectorAll('.section');
        const navLinks = document.querySelectorAll('.nav-menu a');

        let current = '';
        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            const sectionHeight = section.clientHeight;
            if (window.pageYOffset >= sectionTop - 60) {
                current = section.getAttribute('id');
            }
        });
        
        navLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href') === `#${current}`) {
                link.classList.add('active');
            }
        });
    });
    
    // Add comparison calculator
    window.calculateComparison = function() {
        const aluguel = parseFloat(prompt('Digite o valor do aluguel mensal (R$):'));
        if (isNaN(aluguel)) return;
        
        const taxaAdmin = aluguel * 0.08;
        const iptu = 150;
        const baseIR = aluguel - taxaAdmin - iptu;
        const ir = (baseIR * 0.225) - 662.77;
        const liquido = baseIR - ir - 200;
        
        const resultado = `
            Aluguel Bruto: ${formatCurrency(aluguel)}
            Taxa Admin (8%): ${formatCurrency(taxaAdmin)}
            IPTU: ${formatCurrency(iptu)}
            IR: ${formatCurrency(ir)}
            Líquido Final: ${formatCurrency(liquido)}
            
            Vs Investimento: ${formatCurrency(8108.49)}
            Diferença: ${formatCurrency(8108.49 - liquido)}
        `;
        
        alert(resultado);
    };
    
    // Console easter egg
    console.log('%c💰 Análise de Investimentos', 'font-size: 20px; font-weight: bold; color: #1e3a8a;');
    console.log('%cDados baseados no Boletim Focus do Banco Central - Outubro 2025', 'font-size: 12px; color: #64748b;');
    console.log('%cPara mais informações: contato@exemplo.com', 'font-size: 12px; color: #10b981;');
});

// Add CSS class for fade-in animation
const style = document.createElement('style');
style.textContent = `
    .fade-in {
        animation: fadeIn 0.6s ease-out forwards;
    }
    
    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .nav-menu a.active {
        color: var(--primary);
        border-bottom: 2px solid var(--primary);
    }
`;
document.head.appendChild(style);
