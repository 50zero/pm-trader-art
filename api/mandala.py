"""
Serverless API endpoint for mandala generation
Deployed on Vercel as /api/mandala/[address]
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../'))

from flask import Flask, jsonify
import json
import traceback

# Import the existing mandala generation logic
try:
    from mandala_app import generate_mandala_for_address
    from data_fetcher import fetch_polymarket_data
    from svg_generator import create_mandala_svg
    from models import PortfolioData
except ImportError as e:
    print(f"Import error: {e}")
    # Fallback imports for serverless environment
    pass

app = Flask(__name__)

def handler(request):
    """
    Vercel serverless function handler
    Expects URL pattern: /api/mandala/{address}
    """
    try:
        # Extract address from URL path
        path_parts = request.path.split('/')
        if len(path_parts) < 3:
            return jsonify({
                'success': False,
                'error': 'Address parameter required'
            }), 400
            
        address = path_parts[-1]  # Last part of path is the address
        
        # Validate address format
        if not address.startswith('0x') or len(address) != 42:
            return jsonify({
                'success': False,
                'error': 'Invalid Ethereum address format'
            }), 400
        
        # Generate mandala (this calls your existing Python logic)
        result = generate_mandala_for_address(address)
        
        if result['success']:
            return jsonify({
                'success': True,
                'svg': result['svg'],
                'portfolio': result['portfolio']
            })
        else:
            return jsonify({
                'success': False,
                'error': result.get('error', 'Failed to generate mandala')
            }), 500
            
    except Exception as e:
        print(f"Error in mandala API: {e}")
        print(traceback.format_exc())
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        }), 500

# For local testing
if __name__ == '__main__':
    from flask import request
    app.add_url_rule('/api/mandala/<address>', 'mandala', 
                     lambda address: handler(type('obj', (object,), {'path': f'/api/mandala/{address}'})()))
    app.run(debug=True, port=3000)