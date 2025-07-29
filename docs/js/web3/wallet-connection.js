/**
 * Wallet Connection Manager for Portfolio Mandala NFT
 * Handles Web3 wallet connections and network management
 */

class WalletConnection {
    constructor() {
        this.isConnected = false;
        this.currentAccount = null;
        this.provider = null;
        this.web3 = null;
        this.chainId = null;
        
        // Polygon Amoy testnet configuration
        this.targetNetwork = {
            chainId: '0x13882', // 80002 in hex
            chainName: 'Polygon Amoy Testnet',
            nativeCurrency: {
                name: 'MATIC',
                symbol: 'MATIC',
                decimals: 18
            },
            rpcUrls: ['https://rpc-amoy.polygon.technology/'],
            blockExplorerUrls: ['https://www.oklink.com/amoy']
        };
        
        this.init();
    }
    
    async init() {
        // Check if wallet is already connected
        if (typeof window.ethereum !== 'undefined') {
            this.provider = window.ethereum;
            
            // Check if already connected
            const accounts = await this.provider.request({ method: 'eth_accounts' });
            if (accounts.length > 0) {
                await this.handleAccountsChanged(accounts);
            }
            
            // Set up event listeners
            this.provider.on('accountsChanged', this.handleAccountsChanged.bind(this));
            this.provider.on('chainChanged', this.handleChainChanged.bind(this));
            this.provider.on('disconnect', this.handleDisconnect.bind(this));
        }
        
        this.updateUI();
    }
    
    async connectWallet() {
        if (typeof window.ethereum === 'undefined') {
            this.showError('MetaMask is not installed. Please install MetaMask to continue.');
            window.open('https://metamask.io/download.html', '_blank');
            return false;
        }
        
        try {
            // Request account access
            const accounts = await this.provider.request({ method: 'eth_requestAccounts' });
            
            if (accounts.length > 0) {
                await this.handleAccountsChanged(accounts);
                
                // Check and switch to correct network
                await this.ensureCorrectNetwork();
                
                MandalaApp.showToast('Wallet connected successfully!', 'success');
                return true;
            }
            
            return false;
        } catch (error) {
            console.error('Error connecting wallet:', error);
            this.showError(this.parseWalletError(error));
            return false;
        }
    }
    
    async disconnectWallet() {
        this.isConnected = false;
        this.currentAccount = null;
        this.provider = null;
        this.web3 = null;
        this.chainId = null;
        
        this.updateUI();
        MandalaApp.showToast('Wallet disconnected', 'info');
    }
    
    async handleAccountsChanged(accounts) {
        if (accounts.length === 0) {
            await this.disconnectWallet();
        } else {
            this.currentAccount = accounts[0];
            this.isConnected = true;
            
            // Get current chain ID
            this.chainId = await this.provider.request({ method: 'eth_chainId' });
            
            this.updateUI();
            this.onAccountChanged(this.currentAccount);
        }
    }
    
    async handleChainChanged(chainId) {
        this.chainId = chainId;
        this.updateUI();
        
        // Reload the page to reset the dapp state
        window.location.reload();
    }
    
    async handleDisconnect() {
        await this.disconnectWallet();
    }
    
    async ensureCorrectNetwork() {
        if (!this.provider) return false;
        
        const currentChainId = await this.provider.request({ method: 'eth_chainId' });
        
        if (currentChainId !== this.targetNetwork.chainId) {
            try {
                // Try to switch to the target network
                await this.provider.request({
                    method: 'wallet_switchEthereumChain',
                    params: [{ chainId: this.targetNetwork.chainId }]
                });
                return true;
            } catch (switchError) {
                // If the network doesn't exist, add it
                if (switchError.code === 4902) {
                    try {
                        await this.provider.request({
                            method: 'wallet_addEthereumChain',
                            params: [this.targetNetwork]
                        });
                        return true;
                    } catch (addError) {
                        console.error('Error adding network:', addError);
                        this.showError('Failed to add Polygon Amoy network. Please add it manually.');
                        return false;
                    }
                } else {
                    console.error('Error switching network:', switchError);
                    this.showError('Please switch to Polygon Amoy testnet manually.');
                    return false;
                }
            }
        }
        
        return true;
    }
    
    isOnCorrectNetwork() {
        return this.chainId === this.targetNetwork.chainId;
    }
    
    getNetworkName() {
        const networks = {
            '0x1': 'Ethereum Mainnet',
            '0x89': 'Polygon Mainnet',
            '0x13881': 'Polygon Mumbai',
            '0x13882': 'Polygon Amoy',
            '0x539': 'Local Network'
        };
        
        return networks[this.chainId] || 'Unknown Network';
    }
    
    updateUI() {
        const connectButton = document.getElementById('connect-wallet-btn');
        const walletInfo = document.getElementById('wallet-info');
        const addressInput = document.getElementById('trader-address');
        const networkWarning = document.getElementById('network-warning');
        
        if (connectButton) {
            if (this.isConnected) {
                connectButton.textContent = `${this.formatAddress(this.currentAccount)}`;
                connectButton.classList.add('connected');
                connectButton.title = 'Click to disconnect';
            } else {
                connectButton.textContent = 'Connect Wallet';
                connectButton.classList.remove('connected');
                connectButton.title = 'Connect your Web3 wallet';
            }
        }
        
        if (walletInfo) {
            if (this.isConnected) {
                walletInfo.innerHTML = `
                    <div class=\"wallet-status\">
                        <span class=\"status-indicator connected\"></span>
                        <span>Connected: ${this.formatAddress(this.currentAccount)}</span>
                        <span class=\"network-name\">${this.getNetworkName()}</span>
                    </div>
                `;
                walletInfo.style.display = 'block';
            } else {
                walletInfo.style.display = 'none';
            }
        }
        
        // Auto-fill address input if connected
        if (addressInput && this.isConnected) {
            addressInput.value = this.currentAccount;
            addressInput.dispatchEvent(new Event('input')); // Trigger validation
        }
        
        // Show network warning if on wrong network
        if (networkWarning) {
            if (this.isConnected && !this.isOnCorrectNetwork()) {
                networkWarning.innerHTML = `
                    <div class=\"warning-content\">
                        <span>⚠️ Please switch to Polygon Amoy testnet</span>
                        <button onclick=\"walletConnection.ensureCorrectNetwork()\" class=\"switch-network-btn\">Switch Network</button>
                    </div>
                `;
                networkWarning.style.display = 'block';
            } else {
                networkWarning.style.display = 'none';
            }
        }
    }
    
    onAccountChanged(account) {
        // Trigger mandala generation for connected account
        if (window.mandalaGenerator && account) {
            // Auto-generate mandala for connected account
            setTimeout(() => {
                const form = document.getElementById('mandala-form');
                if (form) {
                    form.dispatchEvent(new Event('submit'));
                }
            }, 500);
        }
    }
    
    formatAddress(address) {
        if (!address) return '';
        return `${address.slice(0, 6)}...${address.slice(-4)}`;
    }
    
    parseWalletError(error) {
        if (error.code === 4001) {
            return 'Connection rejected by user';
        } else if (error.code === -32002) {
            return 'Connection request already pending';
        } else if (error.message.includes('User rejected')) {
            return 'Connection rejected by user';
        } else {
            return `Connection failed: ${error.message}`;
        }
    }
    
    showError(message) {
        MandalaApp.showToast(message, 'error');
    }
    
    // Public methods for other components
    getConnectedAccount() {
        return this.currentAccount;
    }
    
    isWalletConnected() {
        return this.isConnected;
    }
    
    canUserMint(traderAddress) {
        return this.isConnected && 
               this.currentAccount && 
               this.currentAccount.toLowerCase() === traderAddress.toLowerCase() &&
               this.isOnCorrectNetwork();
    }
}

// Initialize wallet connection when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.walletConnection = new WalletConnection();
});