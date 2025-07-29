// Contract configuration for NFT minting
// This file will be updated after contract deployment

const CONTRACT_CONFIG = {
    // Update this after deployment
    contractAddress: '0x98Ef066332b16d0f427ae936F0a3662c5ae68890',
    
    // Network configuration for Polygon Amoy testnet
    network: {
        chainId: '0x13882', // 80002 in hex
        chainName: 'Polygon Amoy Testnet',
        nativeCurrency: {
            name: 'MATIC',
            symbol: 'MATIC',
            decimals: 18
        },
        rpcUrls: ['https://rpc-amoy.polygon.technology/'],
        blockExplorerUrls: ['https://www.oklink.com/amoy']
    },
    
    // Contract metadata
    name: 'Portfolio Mandala',
    symbol: 'PMANDALA',
    
    // API endpoints
    baseTokenURI: 'http://localhost:5000/api/nft/metadata/',
    contractURI: 'http://localhost:5000/api/nft/contract-metadata'
};

// Export for use in other files
if (typeof module !== 'undefined' && module.exports) {
    module.exports = CONTRACT_CONFIG;
}