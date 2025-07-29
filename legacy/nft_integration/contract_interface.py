"""
Web3 contract interface for Portfolio Mandala NFT
"""
import json
import os
from typing import Optional, Dict, Any, List
from web3 import Web3
from web3.middleware import ExtraDataToPOAMiddleware
from web3.exceptions import ContractLogicError, TransactionNotFound
import logging

from .config import get_network_config, get_contract_config, WEB3_CONFIG

logger = logging.getLogger(__name__)

class PortfolioMandalaContract:
    def __init__(self):
        self.network_config = get_network_config()
        self.contract_config = get_contract_config()
        
        # Initialize Web3
        self.w3 = Web3(Web3.HTTPProvider(
            self.network_config['rpc_url'],
            request_kwargs={'timeout': WEB3_CONFIG['timeout']}
        ))
        
        # Add POA middleware for Polygon
        self.w3.middleware_onion.inject(ExtraDataToPOAMiddleware, layer=0)
        
        if not self.w3.is_connected():
            raise ConnectionError("Failed to connect to Polygon Amoy network")
        
        # Load contract ABI and initialize contract
        self.contract = None
        self._load_contract()
    
    def _load_contract(self):
        """Load the contract ABI and initialize contract instance"""
        try:
            abi_path = self.contract_config['abi_path']
            if os.path.exists(abi_path):
                with open(abi_path, 'r') as f:
                    contract_json = json.load(f)
                    abi = contract_json.get('abi', contract_json)
                
                contract_address = self.contract_config['address']
                if contract_address and self.w3.is_address(contract_address):
                    self.contract = self.w3.eth.contract(
                        address=self.w3.to_checksum_address(contract_address),
                        abi=abi
                    )
                    logger.info(f"Contract loaded successfully: {contract_address}")
                else:
                    logger.warning("Contract address not set or invalid")
            else:
                logger.warning(f"Contract ABI file not found: {abi_path}")
        except Exception as e:
            logger.error(f"Failed to load contract: {e}")
    
    def is_ready(self) -> bool:
        """Check if the contract is ready for use"""
        return self.contract is not None
    
    def has_trader_minted(self, trader_address: str) -> bool:
        """Check if a trader has already minted their NFT"""
        if not self.is_ready():
            return False
        
        try:
            trader_address = self.w3.to_checksum_address(trader_address)
            return self.contract.functions.hasTraderMinted(trader_address).call()
        except Exception as e:
            logger.error(f"Error checking if trader has minted: {e}")
            return False
    
    def get_trader_token_id(self, trader_address: str) -> Optional[int]:
        """Get the token ID for a specific trader"""
        if not self.is_ready():
            return None
        
        try:
            trader_address = self.w3.to_checksum_address(trader_address)
            if self.has_trader_minted(trader_address):
                return self.contract.functions.getTraderTokenId(trader_address).call()
            return None
        except Exception as e:
            logger.error(f"Error getting trader token ID: {e}")
            return None
    
    def get_token_trader(self, token_id: int) -> Optional[str]:
        """Get the trader address for a specific token ID"""
        if not self.is_ready():
            return None
        
        try:
            return self.contract.functions.getTokenTrader(token_id).call()
        except Exception as e:
            logger.error(f"Error getting token trader: {e}")
            return None
    
    def get_total_supply(self) -> int:
        """Get the total number of minted tokens"""
        if not self.is_ready():
            return 0
        
        try:
            return self.contract.functions.totalSupply().call()
        except Exception as e:
            logger.error(f"Error getting total supply: {e}")
            return 0
    
    def get_token_uri(self, token_id: int) -> Optional[str]:
        """Get the token URI for a specific token ID"""
        if not self.is_ready():
            return None
        
        try:
            return self.contract.functions.tokenURI(token_id).call()
        except Exception as e:
            logger.error(f"Error getting token URI: {e}")
            return None
    
    def estimate_mint_gas(self, trader_address: str) -> Optional[int]:
        """Estimate gas cost for minting"""
        if not self.is_ready():
            return None
        
        try:
            trader_address = self.w3.to_checksum_address(trader_address)
            
            # Try to estimate gas without requiring actual funds
            try:
                gas_estimate = self.contract.functions.mintMandala().estimate_gas({'from': trader_address})
                return int(gas_estimate * WEB3_CONFIG['gas_price_multiplier'])
            except Exception:
                # Fallback to default gas limit if estimation fails
                return WEB3_CONFIG['gas_limit']
            
        except Exception as e:
            logger.error(f"Error estimating mint gas: {e}")
            return WEB3_CONFIG['gas_limit']
    
    def get_mint_transaction_data(self, trader_address: str) -> Optional[Dict[str, Any]]:
        """Get transaction data for minting (for frontend to execute)"""
        if not self.is_ready():
            return None
        
        try:
            trader_address = self.w3.to_checksum_address(trader_address)
            
            # Check if already minted
            if self.has_trader_minted(trader_address):
                raise ValueError("Trader has already minted their mandala")
            
            # Get current gas price
            gas_price = self.w3.eth.gas_price
            
            # Estimate gas
            gas_estimate = self.estimate_mint_gas(trader_address)
            if not gas_estimate:
                gas_estimate = WEB3_CONFIG['gas_limit']
            
            # Prepare transaction data
            transaction_data = {
                'to': self.contract.address,
                'data': self.contract.functions.mintMandala().build_transaction({'from': trader_address})['data'],
                'gas': hex(gas_estimate),
                'gasPrice': hex(gas_price),
                'value': '0x0',  # No ETH/MATIC value needed
                'chainId': hex(self.network_config['chain_id'])
            }
            
            return transaction_data
            
        except Exception as e:
            logger.error(f"Error getting mint transaction data: {e}")
            return None
    
    def verify_transaction(self, tx_hash: str) -> Dict[str, Any]:
        """Verify a transaction and get its status"""
        try:
            tx_hash = self.w3.to_hex(tx_hash)
            
            # Get transaction receipt
            receipt = self.w3.eth.get_transaction_receipt(tx_hash)
            
            # Check if transaction was successful
            success = receipt['status'] == 1
            
            # Parse logs if successful
            token_id = None
            if success and self.contract:
                # Look for MandalaCreated event
                mandala_created_logs = self.contract.events.MandalaCreated().process_receipt(receipt)
                if mandala_created_logs:
                    token_id = mandala_created_logs[0]['args']['tokenId']
            
            return {
                'success': success,
                'block_number': receipt['blockNumber'],
                'gas_used': receipt['gasUsed'],
                'token_id': token_id,
                'transaction_hash': tx_hash,
                'explorer_url': f"{self.network_config['block_explorer']}/tx/{tx_hash}"
            }
            
        except TransactionNotFound:
            return {'success': False, 'error': 'Transaction not found'}
        except Exception as e:
            logger.error(f"Error verifying transaction: {e}")
            return {'success': False, 'error': str(e)}
    
    def get_contract_info(self) -> Dict[str, Any]:
        """Get basic contract information"""
        if not self.is_ready():
            return {'ready': False}
        
        try:
            return {
                'ready': True,
                'address': self.contract.address,
                'name': self.contract_config['name'],
                'symbol': self.contract_config['symbol'],
                'total_supply': self.get_total_supply(),
                'network': self.network_config['network_name'],
                'chain_id': self.network_config['chain_id'],
                'explorer_url': f"{self.network_config['block_explorer']}/address/{self.contract.address}"
            }
        except Exception as e:
            logger.error(f"Error getting contract info: {e}")
            return {'ready': False, 'error': str(e)}