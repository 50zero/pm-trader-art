"""
Serverless API endpoints for NFT functionality
Handles contract info, metadata, and mint status
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../'))

from flask import Flask, jsonify
import json

app = Flask(__name__)

def get_contract_info():
    """Get contract ABI and configuration"""
    try:
        # Load ABI from compiled contract
        abi_path = os.path.join(os.path.dirname(__file__), '../contracts/artifacts/contracts/PortfolioMandala.sol/PortfolioMandala.json')
        
        if os.path.exists(abi_path):
            with open(abi_path, 'r') as f:
                contract_data = json.load(f)
                return {
                    'success': True,
                    'contract': {
                        'abi': contract_data['abi'],
                        'address': os.getenv('CONTRACT_ADDRESS', '0x98Ef066332b16d0f427ae936F0a3662c5ae68890')
                    }
                }
        else:
            return {
                'success': False,
                'message': 'Contract ABI not found'
            }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

def get_mint_status(address):
    """Check if address has already minted an NFT"""
    try:
        # In a real implementation, you'd check the blockchain
        # For now, return a placeholder response
        return {
            'success': True,
            'hasMinted': False,  # You would check the contract here
            'canMint': True
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

def get_nft_metadata(token_id):
    """Generate NFT metadata for a specific token ID"""
    try:
        # You would load the trader data associated with this token ID
        # and generate metadata according to OpenSea standards
        metadata = {
            "name": f"Portfolio Mandala #{token_id}",
            "description": "A unique portfolio mandala NFT representing trading patterns on Polymarket",
            "image": f"https://your-api-domain.vercel.app/api/mandala-image/{token_id}",
            "external_url": f"https://your-frontend-domain.github.io/mandala/{token_id}",
            "attributes": [
                {
                    "trait_type": "Token ID",
                    "value": token_id
                },
                {
                    "trait_type": "Collection",
                    "value": "Portfolio Mandala"
                }
            ]
        }
        return jsonify(metadata)
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500

def handler(request):
    """
    Main serverless handler for NFT endpoints
    Supports:
    - /api/nft/contract-info - Get contract ABI and address
    - /api/nft/mint-status/{address} - Check mint status for address  
    - /api/nft/metadata/{token_id} - Get NFT metadata
    """
    try:
        path_parts = request.path.split('/')
        
        if len(path_parts) < 3:
            return jsonify({'error': 'Invalid path'}), 400
            
        endpoint = path_parts[2]  # 'contract-info', 'mint-status', or 'metadata'
        
        if endpoint == 'contract-info':
            return jsonify(get_contract_info())
            
        elif endpoint == 'mint-status' and len(path_parts) > 3:
            address = path_parts[3]
            return jsonify(get_mint_status(address))
            
        elif endpoint == 'metadata' and len(path_parts) > 3:
            token_id = path_parts[3]
            return get_nft_metadata(token_id)
            
        else:
            return jsonify({'error': 'Unknown endpoint'}), 404
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# For local testing
if __name__ == '__main__':
    from flask import request
    
    # Add test routes
    @app.route('/api/nft/contract-info')
    def contract_info():
        return jsonify(get_contract_info())
    
    @app.route('/api/nft/mint-status/<address>')
    def mint_status(address):
        return jsonify(get_mint_status(address))
    
    @app.route('/api/nft/metadata/<token_id>')
    def metadata(token_id):
        return get_nft_metadata(token_id)
    
    app.run(debug=True, port=3001)