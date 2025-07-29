/**
 * NFT Minting Manager for Portfolio Mandala
 * Handles the minting process and contract interactions
 */

class NFTMinting {
    constructor() {
        this.contractAddress = null; // Will be set from backend
        this.contractABI = null; // Will be loaded from backend
        this.contract = null;
        this.isMinting = false;
        
        this.init();
    }
    
    async init() {
        // Load contract information from backend
        await this.loadContractInfo();
        this.setupEventListeners();
    }
    
    async loadContractInfo() {
        try {
            // Use global config from frontend
            if (window.API_CONFIG?.CONTRACT_ADDRESS) {
                this.contractAddress = window.API_CONFIG.CONTRACT_ADDRESS;
                console.log('Contract address loaded from config:', this.contractAddress);
            }
            
            // Load ABI from serverless API
            const apiUrl = window.API_CONFIG?.BASE_URL || 'https://pm-trader-art-api.vercel.app/api';
            const response = await fetch(`${apiUrl}/nft/contract-info`);
            const data = await response.json();
            
            if (data.success && data.contract) {
                this.contractABI = data.contract.abi;
                console.log('Contract ABI loaded successfully');
            } else {
                console.warn('Contract ABI not available:', data.message);
            }
        } catch (error) {
            console.error('Error loading contract info:', error);
        }
    }
    
    setupEventListeners() {
        // Listen for mandala generation completion to check mint status
        document.addEventListener('mandalaGenerated', (event) => {
            this.checkMintStatus(event.detail.portfolio.trader_address);
        });
    }
    
    async checkMintStatus(traderAddress) {
        if (!this.contractAddress || !traderAddress) return;
        
        try {
            const apiUrl = window.API_CONFIG?.BASE_URL || 'https://pm-trader-art-api.vercel.app/api';
            const response = await fetch(`${apiUrl}/nft/mint-status/${traderAddress}`);
            const data = await response.json();
            
            this.updateMintButton(traderAddress, data);
        } catch (error) {
            console.error('Error checking mint status:', error);
        }
    }
    
    updateMintButton(traderAddress, mintStatus) {
        const mintButton = document.getElementById('mint-nft-btn');
        const walletConnection = window.walletConnection;
        
        if (!mintButton) return;
        
        // Check if user can mint (owns the wallet address)
        const canMint = walletConnection && walletConnection.canUserMint(traderAddress);
        const hasAlreadyMinted = mintStatus.has_minted;
        
        if (hasAlreadyMinted) {
            mintButton.textContent = '✅ Already Minted';
            mintButton.disabled = true;
            mintButton.classList.add('minted');
            mintButton.title = `NFT #${mintStatus.token_id} already minted`;
        } else if (!walletConnection.isWalletConnected()) {
            mintButton.textContent = 'Connect Wallet to Mint';
            mintButton.disabled = true;
            mintButton.classList.remove('minted');
            mintButton.title = 'Connect your wallet first';
        } else if (!canMint) {
            mintButton.textContent = 'Can Only Mint Your Own';
            mintButton.disabled = true;
            mintButton.classList.remove('minted');
            mintButton.title = 'You can only mint NFTs for your own wallet address';
        } else {
            mintButton.textContent = '🎨 Mint NFT';
            mintButton.disabled = false;
            mintButton.classList.remove('minted');
            mintButton.title = `Mint your portfolio mandala as an NFT (${mintStatus.estimated_cost || 'Cost TBD'})`;
        }
        
        mintButton.style.display = 'inline-block';
    }
    
    async mintNFT(traderAddress) {
        if (this.isMinting) return;
        
        const walletConnection = window.walletConnection;
        
        if (!walletConnection.isWalletConnected()) {
            MandalaApp.showToast('Please connect your wallet first', 'error');
            return;
        }
        
        if (!walletConnection.canUserMint(traderAddress)) {
            MandalaApp.showToast('You can only mint NFTs for your own wallet address', 'error');
            return;
        }
        
        this.isMinting = true;
        this.setMintingState(true);
        
        try {
            // Get transaction data from backend
            const response = await fetch('/api/nft/prepare-mint', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    trader_address: traderAddress
                })
            });
            
            const data = await response.json();
            
            if (!data.success) {
                throw new Error(data.error || 'Failed to prepare minting transaction');
            }
            
            // Show confirmation dialog with gas estimate
            const confirmed = await this.showMintConfirmation(data.transaction, data.gas_estimate);
            if (!confirmed) {
                this.setMintingState(false);
                this.isMinting = false;
                return;
            }
            
            // Execute the transaction
            const txHash = await this.executeTransaction(data.transaction);
            
            if (txHash) {
                MandalaApp.showToast('Transaction submitted! Waiting for confirmation...', 'info');
                
                // Wait for transaction confirmation
                await this.waitForTransactionConfirmation(txHash, traderAddress);
            }
            
        } catch (error) {
            console.error('Minting error:', error);
            MandalaApp.showToast(error.message || 'Minting failed', 'error');
        } finally {
            this.setMintingState(false);
            this.isMinting = false;
        }
    }
    
    async showMintConfirmation(transaction, gasEstimate) {
        return new Promise((resolve) => {
            const modal = document.createElement('div');
            modal.className = 'mint-confirmation-modal';
            modal.innerHTML = `
                <div class=\"modal-content\">
                    <h3>Confirm NFT Minting</h3>
                    <div class=\"confirmation-details\">
                        <p><strong>Network:</strong> Polygon Amoy Testnet</p>
                        <p><strong>Estimated Gas:</strong> ${gasEstimate?.formatted || 'Calculating...'}</p>
                        <p><strong>Cost:</strong> ~$${gasEstimate?.usd_cost || '0.01'} USD</p>
                    </div>
                    <div class=\"confirmation-warning\">
                        <p>⚠️ You can only mint one NFT per wallet address.</p>
                        <p>This action cannot be undone.</p>
                    </div>
                    <div class=\"modal-actions\">
                        <button class=\"action-btn secondary cancel-btn\">Cancel</button>
                        <button class=\"action-btn confirm-btn\">Confirm Mint</button>
                    </div>
                </div>
            `;
            
            document.body.appendChild(modal);
            
            modal.querySelector('.cancel-btn').onclick = () => {
                document.body.removeChild(modal);
                resolve(false);
            };
            
            modal.querySelector('.confirm-btn').onclick = () => {
                document.body.removeChild(modal);
                resolve(true);
            };
            
            // Close on background click
            modal.onclick = (e) => {
                if (e.target === modal) {
                    document.body.removeChild(modal);
                    resolve(false);
                }
            };
        });
    }
    
    async executeTransaction(transactionData) {
        try {
            const provider = window.ethereum;
            
            // Add the connected account as the 'from' address
            const accounts = await provider.request({ method: 'eth_accounts' });
            if (accounts.length === 0) {
                throw new Error('No wallet connected');
            }
            
            const txData = {
                ...transactionData,
                from: accounts[0]
            };
            
            const txHash = await provider.request({
                method: 'eth_sendTransaction',
                params: [txData]
            });
            
            return txHash;
        } catch (error) {
            if (error.code === 4001) {
                throw new Error('Transaction rejected by user');
            } else {
                throw new Error(`Transaction failed: ${error.message}`);
            }
        }
    }
    
    async waitForTransactionConfirmation(txHash, traderAddress) {
        try {
            // Poll for transaction status
            const maxAttempts = 60; // 5 minutes max
            let attempts = 0;
            
            const checkStatus = async () => {
                attempts++;
                
                try {
                    const response = await fetch('/api/nft/transaction-status', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({
                            tx_hash: txHash,
                            trader_address: traderAddress
                        })
                    });
                    
                    const data = await response.json();
                    
                    if (data.status === 'confirmed') {
                        MandalaApp.showToast('🎉 NFT minted successfully!', 'success');
                        this.onMintSuccess(data.token_id, txHash);
                        return;
                    } else if (data.status === 'failed') {
                        throw new Error(data.error || 'Transaction failed');
                    } else if (data.status === 'pending' && attempts < maxAttempts) {
                        // Keep checking
                        setTimeout(checkStatus, 5000);
                        return;
                    } else {
                        throw new Error('Transaction timeout');
                    }
                } catch (error) {
                    if (attempts < maxAttempts) {
                        setTimeout(checkStatus, 5000);
                    } else {
                        throw error;
                    }
                }
            };
            
            await checkStatus();
            
        } catch (error) {
            console.error('Transaction confirmation error:', error);
            MandalaApp.showToast(`Transaction may have failed: ${error.message}`, 'error');
        }
    }
    
    onMintSuccess(tokenId, txHash) {
        // Update UI to show successful mint
        const mintButton = document.getElementById('mint-nft-btn');
        if (mintButton) {
            mintButton.textContent = '✅ Minted!';
            mintButton.disabled = true;
            mintButton.classList.add('minted');
        }
        
        // Show success details
        this.showMintSuccessModal(tokenId, txHash);
        
        // Refresh mint status
        const traderAddress = window.walletConnection.getConnectedAccount();
        if (traderAddress) {
            setTimeout(() => {
                this.checkMintStatus(traderAddress);
            }, 2000);
        }
    }
    
    showMintSuccessModal(tokenId, txHash) {
        const modal = document.createElement('div');
        modal.className = 'success-modal';
        modal.innerHTML = `
            <div class=\"modal-content\">
                <div class=\"success-icon\">🎉</div>
                <h3>NFT Minted Successfully!</h3>
                <div class=\"success-details\">
                    <p><strong>Token ID:</strong> #${tokenId}</p>
                    <p><strong>Transaction:</strong> 
                        <a href=\"https://www.oklink.com/amoy/tx/${txHash}\" target=\"_blank\">
                            ${txHash.slice(0, 10)}...${txHash.slice(-8)}
                        </a>
                    </p>
                </div>
                <div class=\"success-actions\">
                    <button class=\"action-btn\" onclick=\"this.parentElement.parentElement.parentElement.remove()\">
                        Close
                    </button>
                </div>
            </div>
        `;
        
        document.body.appendChild(modal);
        
        // Auto-close after 10 seconds
        setTimeout(() => {
            if (document.body.contains(modal)) {
                document.body.removeChild(modal);
            }
        }, 10000);
    }
    
    setMintingState(isMinting) {
        const mintButton = document.getElementById('mint-nft-btn');
        if (mintButton) {
            if (isMinting) {
                mintButton.textContent = '⏳ Minting...';
                mintButton.disabled = true;
                mintButton.classList.add('loading');
            } else {
                mintButton.classList.remove('loading');
                // Button text will be updated by updateMintButton
            }
        }
    }
}

// Initialize NFT minting when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.nftMinting = new NFTMinting();
});