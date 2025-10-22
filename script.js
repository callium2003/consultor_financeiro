// Mobile Menu Toggle
document.addEventListener('DOMContentLoaded', function() {
    const menuToggle = document.getElementById('menuToggle');
    const navMenu = document.querySelector('.nav-menu');
    
    menuToggle.addEventListener('click', function() {
        navMenu.classList.toggle('active');
    });
    
    // Close menu when clicking on a link
    const navLinks = document.querySelectorAll('.nav-menu a');
    navLinks.forEach(link => {
        link.addEventListener('click', function() {
            navMenu.classList.remove('active');
        });
    });
    
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