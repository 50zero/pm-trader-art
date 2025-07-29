// Mandala generation and display functionality
class MandalaGenerator {
    constructor() {
        this.form = document.getElementById('mandala-form');
        this.addressInput = document.getElementById('trader-address');
        this.generateBtn = document.getElementById('generate-btn');
        this.resultsSection = document.getElementById('results-section');
        this.errorSection = document.getElementById('error-section');
        this.mandalaDisplay = document.getElementById('mandala-display');
        this.portfolioInfo = document.getElementById('portfolio-info');
        
        this.init();
    }

    init() {
        this.addEventListeners();
        this.setupValidation();
    }

    addEventListeners() {
        if (this.form) {
            this.form.addEventListener('submit', this.handleSubmit.bind(this));
        }

        // Download button
        const downloadBtn = document.getElementById('download-btn');
        if (downloadBtn) {
            downloadBtn.addEventListener('click', this.downloadSVG.bind(this));
        }

        // New mandala button
        const newMandalaBtn = document.getElementById('new-mandala-btn');
        if (newMandalaBtn) {
            newMandalaBtn.addEventListener('click', this.resetForm.bind(this));
        }

        // Retry button
        const retryBtn = document.getElementById('retry-btn');
        if (retryBtn) {
            retryBtn.addEventListener('click', this.retryGeneration.bind(this));
        }

        // Address input validation
        if (this.addressInput) {
            this.addressInput.addEventListener('input', this.validateAddress.bind(this));
            this.addressInput.addEventListener('paste', this.handlePaste.bind(this));
        }
    }

    setupValidation() {
        if (!this.addressInput) return;

        // Real-time validation
        this.addressInput.addEventListener('input', (e) => {
            const value = e.target.value;
            const isValid = MandalaApp.isValidAddress(value);
            
            e.target.style.borderColor = value.length === 0 ? '' : 
                isValid ? 'var(--neon-green)' : 'var(--neon-pink)';
        });
    }

    async handleSubmit(e) {
        e.preventDefault();
        
        const address = this.addressInput.value.trim();
        if (!MandalaApp.isValidAddress(address)) {
            this.showError('Please enter a valid Ethereum address');
            return;
        }

        await this.generateMandala(address);
    }

    handlePaste(e) {
        // Clean pasted address
        setTimeout(() => {
            const value = this.addressInput.value.trim();
            this.addressInput.value = value;
        }, 0);
    }

    validateAddress() {
        const address = this.addressInput.value.trim();
        const isValid = address.length === 0 || MandalaApp.isValidAddress(address);
        
        if (this.generateBtn) {
            this.generateBtn.disabled = !isValid || address.length === 0;
        }
        
        return isValid;
    }

    async generateMandala(address) {
        this.setLoadingState(true);
        this.hideError();

        try {
            // Use serverless API endpoint
            const apiUrl = window.API_CONFIG?.BASE_URL || 'https://pm-trader-art-api.vercel.app/api';
            const response = await fetch(`${apiUrl}/mandala/${address}`);
            
            if (!response.ok) {
                // Handle HTTP error status
                const errorData = await response.json().catch(() => ({}));
                throw new Error(errorData.error || `HTTP ${response.status}: ${response.statusText}`);
            }

            const data = await response.json();

            if (data.success) {
                this.displayMandala(data.svg, data.portfolio);
                MandalaApp.showToast('Mandala generated successfully!', 'success');
                
                // Emit event for NFT minting integration
                document.dispatchEvent(new CustomEvent('mandalaGenerated', {
                    detail: { portfolio: data.portfolio, svg: data.svg }
                }));
            } else {
                this.showError(data.error || 'Failed to generate mandala');
            }
        } catch (error) {
            console.error('Error generating mandala:', error);
            this.showError(error.message || 'Network error. Please check your connection and try again.');
        } finally {
            this.setLoadingState(false);
        }
    }

    displayMandala(svg, portfolio) {
        // Display the SVG
        if (this.mandalaDisplay) {
            this.mandalaDisplay.innerHTML = svg;
            
            // Add click to copy address functionality
            const svgElement = this.mandalaDisplay.querySelector('svg');
            if (svgElement) {
                svgElement.style.cursor = 'pointer';
                svgElement.title = 'Click to copy address';
                svgElement.addEventListener('click', () => {
                    MandalaApp.copyToClipboard(portfolio.trader_address)
                        .then(() => MandalaApp.showToast('Address copied to clipboard!'))
                        .catch(() => MandalaApp.showToast('Failed to copy address', 'error'));
                });
            }
        }

        // Display portfolio information
        this.displayPortfolioInfo(portfolio);

        // Show results section
        if (this.resultsSection) {
            this.resultsSection.style.display = 'block';
            this.resultsSection.scrollIntoView({ behavior: 'smooth' });
        }

        // Store current data for download
        this.currentSVG = svg;
        this.currentPortfolio = portfolio;
    }

    displayPortfolioInfo(portfolio) {
        if (!this.portfolioInfo) return;

        // Category colors mapping (should match the Python colors)
        const categoryColors = {
            politics: '#FF0040',
            crypto: '#00FF41',
            sports: '#0080FF',
            entertainment: '#FF00FF',
            technology: '#8000FF',
            economics: '#00FFFF',
            other: '#FFFFFF'
        };

        const html = `
            <h4>Portfolio Statistics</h4>
            <div class="stat-item">
                <span class="stat-label">Address</span>
                <span class="stat-value">${MandalaApp.formatAddress(portfolio.trader_address)}</span>
            </div>
            <div class="stat-item">
                <span class="stat-label">Total Volume</span>
                <span class="stat-value">$${MandalaApp.formatNumber(portfolio.total_volume)}</span>
            </div>
            <div class="stat-item">
                <span class="stat-label">Total Trades</span>
                <span class="stat-value">${portfolio.trade_count}</span>
            </div>
            <div class="stat-item">
                <span class="stat-label">Categories</span>
                <span class="stat-value">${Object.keys(portfolio.category_percentages).length}</span>
            </div>
            
            <div class="category-breakdown">
                <h4>Category Breakdown</h4>
                ${Object.entries(portfolio.category_percentages)
                    .sort(([,a], [,b]) => b - a)
                    .map(([category, percentage]) => `
                        <div class="category-item">
                            <div class="category-color" style="background-color: ${categoryColors[category] || '#FFFFFF'}"></div>
                            <span class="category-name">${category}</span>
                            <span class="category-percentage">${percentage.toFixed(1)}%</span>
                        </div>
                    `).join('')}
            </div>
        `;

        this.portfolioInfo.innerHTML = html;
    }

    downloadSVG() {
        if (!this.currentSVG || !this.currentPortfolio) {
            MandalaApp.showToast('No mandala to download', 'error');
            return;
        }

        const blob = new Blob([this.currentSVG], { type: 'image/svg+xml' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `mandala_${MandalaApp.formatAddress(this.currentPortfolio.trader_address)}.svg`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);

        MandalaApp.showToast('Mandala downloaded successfully!');
    }

    resetForm() {
        if (this.addressInput) {
            this.addressInput.value = '';
            this.addressInput.style.borderColor = '';
        }
        
        this.hideResults();
        this.hideError();
        
        if (this.addressInput) {
            this.addressInput.focus();
        }
    }

    retryGeneration() {
        if (this.addressInput && this.addressInput.value.trim()) {
            this.generateMandala(this.addressInput.value.trim());
        }
    }

    setLoadingState(loading) {
        if (this.generateBtn) {
            this.generateBtn.classList.toggle('loading', loading);
            this.generateBtn.disabled = loading;
        }
    }

    showError(message) {
        if (this.errorSection) {
            const errorMessage = document.getElementById('error-message');
            if (errorMessage) {
                errorMessage.textContent = message;
            }
            this.errorSection.style.display = 'block';
            this.errorSection.scrollIntoView({ behavior: 'smooth' });
        }
        
        this.hideResults();
        MandalaApp.showToast(message, 'error');
    }

    hideError() {
        if (this.errorSection) {
            this.errorSection.style.display = 'none';
        }
    }

    hideResults() {
        if (this.resultsSection) {
            this.resultsSection.style.display = 'none';
        }
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.mandalaGenerator = new MandalaGenerator();
});