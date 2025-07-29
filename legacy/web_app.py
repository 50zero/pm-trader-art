from flask import Flask, render_template, request, jsonify
import asyncio
import os
import json
import logging
from mandala_app import PolymarketMandalaApp
from nft_integration import PortfolioMandalaContract, NFTMetadataGenerator

# Configure logging
logging.basicConfig(level=logging.INFO)

app = Flask(__name__, 
            template_folder='web/templates',
            static_folder='web/static')

# Initialize the mandala app and web3 components
mandala_app = PolymarketMandalaApp()
try:
    nft_contract = PortfolioMandalaContract()
    metadata_generator = NFTMetadataGenerator()
except Exception as e:
    logging.warning(f"Failed to initialize Web3 components: {e}")
    nft_contract = None
    metadata_generator = None

@app.route('/')
def index():
    """Main page with address input"""
    return render_template('index.html')

@app.route('/api/mandala/<trader_address>')
def get_mandala(trader_address):
    """API endpoint to generate mandala for a trader address"""
    try:
        # Run the async function
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        svg, portfolio = loop.run_until_complete(
            mandala_app.generate_mandala_for_address(trader_address)
        )
        loop.close()
        
        # Serialize top_markets properly
        top_markets_data = []
        if portfolio.top_markets:
            for market in portfolio.top_markets:
                top_markets_data.append({
                    'question': market.question,
                    'slug': market.slug,
                    'volume': market.volume,
                    'trade_count': market.trade_count
                })
        
        return jsonify({
            'success': True,
            'svg': svg,
            'portfolio': {
                'trader_address': portfolio.trader_address,
                'total_volume': portfolio.total_volume,
                'trade_count': portfolio.trade_count,
                'category_percentages': portfolio.category_percentages,
                'top_markets': top_markets_data
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/mandala/<trader_address>')
def view_mandala(trader_address):
    """Direct mandala view page"""
    return render_template('mandala.html', trader_address=trader_address)

# NFT-related endpoints
@app.route('/api/nft/contract-info')
def get_contract_info():
    """Get contract information for frontend"""
    if not nft_contract:
        return jsonify({
            'success': False,
            'message': 'Contract not initialized'
        })
    
    try:
        contract_info = nft_contract.get_contract_info()
        
        # Load ABI if available
        abi = None
        abi_path = 'contracts/artifacts/PortfolioMandala.sol/PortfolioMandala.json'
        if os.path.exists(abi_path):
            try:
                with open(abi_path, 'r') as f:
                    contract_json = json.load(f)
                    abi = contract_json.get('abi', [])
            except Exception as e:
                logging.error(f"Error loading ABI: {e}")
        
        return jsonify({
            'success': True,
            'contract': {
                **contract_info,
                'abi': abi
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/nft/mint-status/<trader_address>')
def get_mint_status(trader_address):
    """Check if a trader has already minted their NFT"""
    if not nft_contract:
        return jsonify({
            'success': False,
            'error': 'Contract not available'
        }), 503
    
    try:
        has_minted = nft_contract.has_trader_minted(trader_address)
        token_id = None
        
        if has_minted:
            token_id = nft_contract.get_trader_token_id(trader_address)
        
        # Estimate gas cost for minting
        estimated_gas = None
        estimated_cost = None
        if not has_minted:
            gas_estimate = nft_contract.estimate_mint_gas(trader_address)
            if gas_estimate:
                # Rough cost estimation (gas * gas_price * MATIC_price)
                estimated_cost = f"~{gas_estimate * 20 * 0.0000000001:.6f} MATIC"
        
        return jsonify({
            'success': True,
            'has_minted': has_minted,
            'token_id': token_id,
            'estimated_cost': estimated_cost,
            'can_mint': not has_minted
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/nft/prepare-mint', methods=['POST'])
def prepare_mint():
    """Prepare minting transaction data"""
    if not nft_contract:
        return jsonify({
            'success': False,
            'error': 'Contract not available'
        }), 503
    
    try:
        data = request.get_json()
        trader_address = data.get('trader_address')
        
        if not trader_address:
            return jsonify({
                'success': False,
                'error': 'Trader address required'
            }), 400
        
        # Check if already minted
        if nft_contract.has_trader_minted(trader_address):
            return jsonify({
                'success': False,
                'error': 'Trader has already minted their NFT'
            }), 400
        
        # Get transaction data
        transaction_data = nft_contract.get_mint_transaction_data(trader_address)
        if not transaction_data:
            return jsonify({
                'success': False,
                'error': 'Failed to prepare transaction'
            }), 500
        
        # Estimate gas cost
        gas_estimate = nft_contract.estimate_mint_gas(trader_address)
        gas_info = None
        if gas_estimate:
            gas_info = {
                'gas_limit': gas_estimate,
                'formatted': f"{gas_estimate:,} gas units",
                'usd_cost': f"{gas_estimate * 20 * 0.0000000001 * 0.5:.4f}"  # Rough USD estimate
            }
        
        return jsonify({
            'success': True,
            'transaction': transaction_data,
            'gas_estimate': gas_info
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/nft/transaction-status', methods=['POST'])
def check_transaction_status():
    """Check the status of a minting transaction"""
    if not nft_contract:
        return jsonify({
            'success': False,
            'error': 'Contract not available'
        }), 503
    
    try:
        data = request.get_json()
        tx_hash = data.get('tx_hash')
        trader_address = data.get('trader_address')
        
        if not tx_hash:
            return jsonify({
                'success': False,
                'error': 'Transaction hash required'
            }), 400
        
        # Verify transaction
        tx_status = nft_contract.verify_transaction(tx_hash)
        
        if tx_status['success']:
            return jsonify({
                'status': 'confirmed',
                'token_id': tx_status.get('token_id'),
                'transaction_hash': tx_hash,
                'explorer_url': tx_status.get('explorer_url'),
                'block_number': tx_status.get('block_number')
            })
        else:
            # Check if transaction is still pending
            if 'Transaction not found' in tx_status.get('error', ''):
                return jsonify({
                    'status': 'pending',
                    'message': 'Transaction still pending'
                })
            else:
                return jsonify({
                    'status': 'failed',
                    'error': tx_status.get('error', 'Transaction failed')
                })
                
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/nft/metadata/<int:token_id>')
def get_nft_metadata(token_id):
    """Get NFT metadata for OpenSea compatibility"""
    if not nft_contract or not metadata_generator:
        return jsonify({
            'error': 'NFT services not available'
        }), 503
    
    try:
        # Get trader address from token ID
        trader_address = nft_contract.get_token_trader(token_id)
        if not trader_address:
            return jsonify({
                'error': 'Token not found'
            }), 404
        
        # Generate portfolio data
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        svg, portfolio = loop.run_until_complete(
            mandala_app.generate_mandala_for_address(trader_address)
        )
        loop.close()
        
        # Generate metadata
        metadata = metadata_generator.generate_metadata(token_id, portfolio, trader_address)
        
        return jsonify(metadata)
        
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500

@app.route('/api/nft/contract-metadata')
def get_contract_metadata():
    """Get contract-level metadata for OpenSea"""
    if not metadata_generator:
        return jsonify({
            'error': 'Metadata service not available'
        }), 503
    
    try:
        contract_metadata = metadata_generator.generate_contract_metadata()
        return jsonify(contract_metadata)
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)