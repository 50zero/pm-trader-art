"""
Web3 configuration for Portfolio Mandala NFT functionality
"""
import os
from typing import Dict, Any

# Polygon Amoy Testnet Configuration
AMOY_CONFIG = {
    'rpc_url': 'https://rpc-amoy.polygon.technology/',
    'chain_id': 80002,
    'currency_symbol': 'MATIC',
    'block_explorer': 'https://www.oklink.com/amoy',
    'network_name': 'Polygon Amoy Testnet'
}

# Contract Configuration (will be updated after deployment)
CONTRACT_CONFIG = {
    'address': os.getenv('CONTRACT_ADDRESS', ''),  # Set after deployment
    'abi_path': 'contracts/artifacts/contracts/PortfolioMandala.sol/PortfolioMandala.json',
    'name': 'Portfolio Mandala',
    'symbol': 'PMANDALA'
}

# Web3 Provider Configuration
WEB3_CONFIG = {
    'timeout': 30,
    'retries': 3,
    'gas_limit': 500000,
    'gas_price_multiplier': 1.1
}

# NFT Metadata Configuration
METADATA_CONFIG = {
    'base_uri': os.getenv('BASE_URI', 'http://localhost:5000/api/nft/metadata/'),
    'image_base_uri': os.getenv('IMAGE_BASE_URI', 'http://localhost:5000/api/mandala/'),
    'external_url_base': os.getenv('EXTERNAL_URL_BASE', 'http://localhost:5000/mandala/'),
    'description_template': "A unique portfolio mandala NFT representing the trading patterns of {trader_address} on Polymarket. This NFT visualizes their portfolio distribution across different market categories through an animated, artistic mandala pattern.",
    'attributes_mapping': {
        'total_volume': 'Total Volume',
        'trade_count': 'Trade Count',
        'categories_traded': 'Categories Traded',
        'dominant_category': 'Dominant Category'
    }
}

def get_network_config() -> Dict[str, Any]:
    """Get the current network configuration"""
    return AMOY_CONFIG

def get_contract_config() -> Dict[str, Any]:
    """Get the contract configuration"""
    return CONTRACT_CONFIG

def get_metadata_config() -> Dict[str, Any]:
    """Get the metadata configuration"""
    return METADATA_CONFIG