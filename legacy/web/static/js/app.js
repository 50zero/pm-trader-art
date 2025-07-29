// Base app functionality
class MandalaApp {
    constructor() {
        this.init();
    }

    init() {
        this.addEventListeners();
        this.startBackgroundAnimations();
    }

    addEventListeners() {
        // Global event listeners that apply to all pages
        document.addEventListener('click', this.handleGlobalClick.bind(this));
        
        // Add smooth scrolling for anchor links
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', (e) => {
                e.preventDefault();
                const target = document.querySelector(anchor.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({ behavior: 'smooth' });
                }
            });
        });
    }

    handleGlobalClick(e) {
        // Handle clicks on example addresses
        if (e.target.classList.contains('example-btn')) {
            const address = e.target.dataset.address;
            const addressInput = document.getElementById('trader-address');
            if (addressInput) {
                addressInput.value = address;
                this.animateInput(addressInput);
            }
        }
    }

    animateInput(input) {
        input.style.transform = 'scale(1.02)';
        input.style.borderColor = 'var(--neon-cyan)';
        input.style.boxShadow = '0 0 20px rgba(0, 255, 255, 0.3)';
        
        setTimeout(() => {
            input.style.transform = '';
            input.style.borderColor = '';
            input.style.boxShadow = '';
        }, 300);
    }

    startBackgroundAnimations() {
        // Add random delays to floating particles
        const particles = document.querySelectorAll('.particle');
        particles.forEach((particle, index) => {
            const delay = Math.random() * 8;
            particle.style.animationDelay = `${delay}s`;
            
            // Random starting position
            particle.style.left = `${Math.random() * 100}%`;
        });

        // Create additional floating elements
        this.createFloatingElements();
    }

    createFloatingElements() {
        const container = document.querySelector('.floating-particles');
        if (!container) return;

        // Add more subtle floating elements
        for (let i = 0; i < 20; i++) {
            const element = document.createElement('div');
            element.className = 'floating-dot';
            element.style.cssText = `
                position: absolute;
                width: 1px;
                height: 1px;
                background: rgba(0, 255, 155, 0.4);
                left: ${Math.random() * 100}%;
                animation: float ${8 + Math.random() * 8}s linear infinite;
                animation-delay: ${Math.random() * 8}s;
            `;
            container.appendChild(element);
        }
    }

    // Utility functions
    static isValidAddress(address) {
        return /^0x[a-fA-F0-9]{40}$/.test(address);
    }

    static formatAddress(address) {
        if (!address || address.length < 10) return address;
        return `${address.slice(0, 6)}...${address.slice(-4)}`;
    }

    static formatNumber(num) {
        if (num >= 1000000) {
            return (num / 1000000).toFixed(1) + 'M';
        } else if (num >= 1000) {
            return (num / 1000).toFixed(1) + 'K';
        }
        return num.toLocaleString();
    }

    static copyToClipboard(text) {
        if (navigator.clipboard && window.isSecureContext) {
            return navigator.clipboard.writeText(text);
        } else {
            // Fallback for older browsers
            const textArea = document.createElement('textarea');
            textArea.value = text;
            textArea.style.position = 'fixed';
            textArea.style.left = '-999999px';
            textArea.style.top = '-999999px';
            document.body.appendChild(textArea);
            textArea.focus();
            textArea.select();
            
            return new Promise((resolve, reject) => {
                if (document.execCommand('copy')) {
                    textArea.remove();
                    resolve();
                } else {
                    textArea.remove();
                    reject();
                }
            });
        }
    }

    static showToast(message, type = 'info') {
        // Create and show a toast notification
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.textContent = message;
        toast.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: var(--secondary-bg);
            color: var(--primary-text);
            padding: 1rem 1.5rem;
            border-radius: var(--border-radius);
            border: 1px solid ${type === 'error' ? 'var(--neon-pink)' : 'var(--neon-green)'};
            z-index: 9999;
            animation: slideIn 0.3s ease-out;
        `;

        document.body.appendChild(toast);

        // Remove after 3 seconds
        setTimeout(() => {
            toast.style.animation = 'slideOut 0.3s ease-in';
            setTimeout(() => toast.remove(), 300);
        }, 3000);
    }
}

// Add CSS for toast animations
const toastStyles = `
@keyframes slideIn {
    from { transform: translateX(100%); opacity: 0; }
    to { transform: translateX(0); opacity: 1; }
}

@keyframes slideOut {
    from { transform: translateX(0); opacity: 1; }
    to { transform: translateX(100%); opacity: 0; }
}
`;

const styleSheet = document.createElement('style');
styleSheet.textContent = toastStyles;
document.head.appendChild(styleSheet);

// Initialize the app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.mandalaApp = new MandalaApp();
});