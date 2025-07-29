// Mandala viewer functionality for dedicated mandala pages
class MandalaViewer {
    constructor() {
        this.traderAddress = window.traderAddress;
        this.loadingContainer = document.getElementById('loading-container');
        this.mandalaViewer = document.getElementById('mandala-viewer');
        this.errorDisplay = document.getElementById('error-display');
        this.mandalaCanvas = document.getElementById('mandala-canvas');
        this.portfolioStats = document.getElementById('portfolio-stats');
        
        this.currentSVG = null;
        this.currentPortfolio = null;
        
        this.init();
    }

    init() {
        this.addEventListeners();
        this.loadMandala();
    }

    addEventListeners() {
        // Download button
        const downloadBtn = document.getElementById('download-btn');
        if (downloadBtn) {
            downloadBtn.addEventListener('click', this.downloadSVG.bind(this));
        }

        // Fullscreen button
        const fullscreenBtn = document.getElementById('fullscreen-btn');
        if (fullscreenBtn) {
            fullscreenBtn.addEventListener('click', this.toggleFullscreen.bind(this));
        }

        // Share button
        const shareBtn = document.getElementById('share-btn');
        if (shareBtn) {
            shareBtn.addEventListener('click', this.shareMandala.bind(this));
        }

        // Retry button
        const retryBtn = document.getElementById('retry-btn');
        if (retryBtn) {
            retryBtn.addEventListener('click', this.loadMandala.bind(this));
        }

        // Keyboard shortcuts
        document.addEventListener('keydown', this.handleKeydown.bind(this));

        // Handle fullscreen changes
        document.addEventListener('fullscreenchange', this.handleFullscreenChange.bind(this));
        document.addEventListener('webkitfullscreenchange', this.handleFullscreenChange.bind(this));
        document.addEventListener('mozfullscreenchange', this.handleFullscreenChange.bind(this));
        document.addEventListener('MSFullscreenChange', this.handleFullscreenChange.bind(this));
    }

    async loadMandala() {
        if (!this.traderAddress) {
            this.showError('No trader address provided');
            return;
        }

        this.showLoading();

        try {
            const response = await fetch(`/api/mandala/${this.traderAddress}`);
            const data = await response.json();

            if (data.success) {
                this.displayMandala(data.svg, data.portfolio);
            } else {
                this.showError(data.error || 'Failed to load mandala');
            }
        } catch (error) {
            console.error('Error loading mandala:', error);
            this.showError('Network error. Please check your connection and try again.');
        }
    }

    displayMandala(svg, portfolio) {
        this.currentSVG = svg;
        this.currentPortfolio = portfolio;

        // Display the SVG
        if (this.mandalaCanvas) {
            this.mandalaCanvas.innerHTML = svg;
            
            // Add interaction to the SVG
            const svgElement = this.mandalaCanvas.querySelector('svg');
            if (svgElement) {
                this.enhanceSVG(svgElement);
            }
        }

        // Display portfolio stats
        this.displayPortfolioStats(portfolio);

        // Show the viewer
        this.showViewer();

        // Update page title
        document.title = `Mandala for ${MandalaApp.formatAddress(portfolio.trader_address)} - Portfolio Mandala`;
    }

    enhanceSVG(svgElement) {
        // Make SVG interactive
        svgElement.style.transition = 'transform 0.3s ease';
        
        // Add hover effects
        svgElement.addEventListener('mouseenter', () => {
            svgElement.style.transform = 'scale(1.02)';
        });

        svgElement.addEventListener('mouseleave', () => {
            svgElement.style.transform = 'scale(1)';
        });

        // Add click to copy functionality
        svgElement.style.cursor = 'pointer';
        svgElement.title = 'Click to copy address';
        svgElement.addEventListener('click', () => {
            MandalaApp.copyToClipboard(this.currentPortfolio.trader_address)
                .then(() => MandalaApp.showToast('Address copied to clipboard!'))
                .catch(() => MandalaApp.showToast('Failed to copy address', 'error'));
        });
    }

    displayPortfolioStats(portfolio) {
        if (!this.portfolioStats) return;

        const categoryColors = {
            politics: '#FF0040',
            crypto: '#00FF41',
            sports: '#0080FF',
            entertainment: '#FF00FF',
            technology: '#8000FF',
            economics: '#00FFFF',
            other: '#FFFFFF'
        };

        const topMarkets = portfolio.top_markets || [];
        
        const html = `
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-icon">💰</div>
                    <div class="stat-content">
                        <div class="stat-value">$${MandalaApp.formatNumber(portfolio.total_volume)}</div>
                        <div class="stat-label">Total Volume</div>
                    </div>
                </div>
                
                <div class="stat-card">
                    <div class="stat-icon">📊</div>
                    <div class="stat-content">
                        <div class="stat-value">${portfolio.trade_count}</div>
                        <div class="stat-label">Total Trades</div>
                    </div>
                </div>
                
                <div class="stat-card">
                    <div class="stat-icon">🏷️</div>
                    <div class="stat-content">
                        <div class="stat-value">${Object.keys(portfolio.category_percentages).length}</div>
                        <div class="stat-label">Categories</div>
                    </div>
                </div>
            </div>

            <div class="categories-section">
                <h3>Category Distribution</h3>
                <div class="categories-list">
                    ${Object.entries(portfolio.category_percentages)
                        .sort(([,a], [,b]) => b - a)
                        .map(([category, percentage]) => `
                            <div class="category-bar">
                                <div class="category-header">
                                    <span class="category-name">
                                        <div class="category-dot" style="background-color: ${categoryColors[category] || '#FFFFFF'}"></div>
                                        ${category.charAt(0).toUpperCase() + category.slice(1)}
                                    </span>
                                    <span class="category-percentage">${percentage.toFixed(1)}%</span>
                                </div>
                                <div class="progress-bar">
                                    <div class="progress-fill" style="width: ${percentage}%; background-color: ${categoryColors[category] || '#FFFFFF'}"></div>
                                </div>
                            </div>
                        `).join('')}
                </div>
            </div>

            ${topMarkets.length > 0 ? `
                <div class="markets-section">
                    <h3>Top Markets</h3>
                    <div class="markets-list">
                        ${topMarkets.slice(0, 5).map(market => `
                            <div class="market-item">
                                <div class="market-name">${market.question}</div>
                                <div class="market-volume">$${MandalaApp.formatNumber(market.volume)}</div>
                            </div>
                        `).join('')}
                    </div>
                </div>
            ` : ''}
        `;

        this.portfolioStats.innerHTML = html;
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
        a.download = `portfolio_mandala_${MandalaApp.formatAddress(this.currentPortfolio.trader_address)}.svg`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);

        MandalaApp.showToast('Mandala downloaded successfully!');
    }

    async shareMandala() {
        const url = window.location.href;
        
        if (navigator.share) {
            try {
                await navigator.share({
                    title: 'Portfolio Mandala',
                    text: `Check out this portfolio mandala for ${MandalaApp.formatAddress(this.currentPortfolio.trader_address)}`,
                    url: url
                });
                MandalaApp.showToast('Shared successfully!');
            } catch (error) {
                // User cancelled sharing
                if (error.name !== 'AbortError') {
                    this.copyUrlToClipboard(url);
                }
            }
        } else {
            this.copyUrlToClipboard(url);
        }
    }

    copyUrlToClipboard(url) {
        MandalaApp.copyToClipboard(url)
            .then(() => MandalaApp.showToast('URL copied to clipboard!'))
            .catch(() => MandalaApp.showToast('Failed to copy URL', 'error'));
    }

    toggleFullscreen() {
        if (!this.mandalaCanvas) return;

        if (!document.fullscreenElement && !document.webkitFullscreenElement && 
            !document.mozFullScreenElement && !document.msFullscreenElement) {
            // Enter fullscreen
            if (this.mandalaCanvas.requestFullscreen) {
                this.mandalaCanvas.requestFullscreen();
            } else if (this.mandalaCanvas.webkitRequestFullscreen) {
                this.mandalaCanvas.webkitRequestFullscreen();
            } else if (this.mandalaCanvas.mozRequestFullScreen) {
                this.mandalaCanvas.mozRequestFullScreen();
            } else if (this.mandalaCanvas.msRequestFullscreen) {
                this.mandalaCanvas.msRequestFullscreen();
            }
        } else {
            // Exit fullscreen
            if (document.exitFullscreen) {
                document.exitFullscreen();
            } else if (document.webkitExitFullscreen) {
                document.webkitExitFullscreen();
            } else if (document.mozCancelFullScreen) {
                document.mozCancelFullScreen();
            } else if (document.msExitFullscreen) {
                document.msExitFullscreen();
            }
        }
    }

    handleFullscreenChange() {
        const fullscreenBtn = document.getElementById('fullscreen-btn');
        if (!fullscreenBtn) return;

        const isFullscreen = document.fullscreenElement || document.webkitFullscreenElement ||
                           document.mozFullScreenElement || document.msFullscreenElement;
        
        fullscreenBtn.textContent = isFullscreen ? '✕ Exit Fullscreen' : '⛶ Fullscreen';
    }

    handleKeydown(e) {
        switch (e.key) {
            case 'f':
            case 'F':
                if (e.ctrlKey || e.metaKey) {
                    e.preventDefault();
                    this.toggleFullscreen();
                }
                break;
            case 's':
            case 'S':
                if (e.ctrlKey || e.metaKey) {
                    e.preventDefault();
                    this.downloadSVG();
                }
                break;
            case 'Escape':
                if (document.fullscreenElement) {
                    this.toggleFullscreen();
                }
                break;
        }
    }

    showLoading() {
        if (this.loadingContainer) this.loadingContainer.style.display = 'block';
        if (this.mandalaViewer) this.mandalaViewer.style.display = 'none';
        if (this.errorDisplay) this.errorDisplay.style.display = 'none';
    }

    showViewer() {
        if (this.loadingContainer) this.loadingContainer.style.display = 'none';
        if (this.mandalaViewer) this.mandalaViewer.style.display = 'block';
        if (this.errorDisplay) this.errorDisplay.style.display = 'none';
    }

    showError(message) {
        if (this.loadingContainer) this.loadingContainer.style.display = 'none';
        if (this.mandalaViewer) this.mandalaViewer.style.display = 'none';
        if (this.errorDisplay) {
            this.errorDisplay.style.display = 'block';
            const errorText = document.getElementById('error-text');
            if (errorText) {
                errorText.textContent = message;
            }
        }
        
        MandalaApp.showToast(message, 'error');
    }
}

// Add additional CSS for viewer-specific styles
const viewerStyles = `
.stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: 1rem;
    margin-bottom: 2rem;
}

.stat-card {
    background: var(--accent-bg);
    padding: 1.5rem;
    border-radius: var(--border-radius);
    border: 1px solid rgba(255, 255, 255, 0.1);
    display: flex;
    align-items: center;
    gap: 1rem;
}

.stat-icon {
    font-size: 2rem;
}

.stat-value {
    font-size: 1.5rem;
    font-weight: 600;
    color: var(--neon-green);
    font-family: 'JetBrains Mono', monospace;
}

.stat-label {
    color: var(--secondary-text);
    font-size: 0.9rem;
}

.categories-section, .markets-section {
    margin-bottom: 2rem;
}

.categories-section h3, .markets-section h3 {
    color: var(--primary-text);
    margin-bottom: 1rem;
    font-size: 1.2rem;
}

.category-bar {
    margin-bottom: 1rem;
}

.category-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.5rem;
}

.category-name {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 0.9rem;
    text-transform: capitalize;
}

.category-dot {
    width: 10px;
    height: 10px;
    border-radius: 50%;
}

.category-percentage {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.85rem;
    color: var(--neon-cyan);
}

.progress-bar {
    width: 100%;
    height: 4px;
    background: rgba(255, 255, 255, 0.1);
    border-radius: 2px;
    overflow: hidden;
}

.progress-fill {
    height: 100%;
    transition: width 1s ease-out;
    opacity: 0.8;
}

.market-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.75rem 0;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.market-item:last-child {
    border-bottom: none;
}

.market-name {
    flex: 1;
    font-size: 0.9rem;
    color: var(--secondary-text);
    margin-right: 1rem;
}

.market-volume {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.85rem;
    color: var(--neon-green);
    font-weight: 500;
}

.mandala-canvas.fullscreen {
    background: var(--primary-bg);
    display: flex;
    align-items: center;
    justify-content: center;
}

.control-btn {
    padding: 0.5rem 1rem;
    background: var(--accent-bg);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: var(--border-radius);
    color: var(--primary-text);
    cursor: pointer;
    transition: var(--transition);
    font-size: 0.9rem;
}

.control-btn:hover {
    border-color: var(--neon-cyan);
    color: var(--neon-cyan);
}

.viewer-controls {
    display: flex;
    gap: 1rem;
    margin-bottom: 1rem;
    justify-content: center;
}

@media (max-width: 768px) {
    .stats-grid {
        grid-template-columns: 1fr;
    }
    
    .viewer-controls {
        flex-wrap: wrap;
    }
    
    .control-btn {
        flex: 1;
        min-width: 120px;
    }
}
`;

const viewerStyleSheet = document.createElement('style');
viewerStyleSheet.textContent = viewerStyles;
document.head.appendChild(viewerStyleSheet);

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.mandalaViewer = new MandalaViewer();
});