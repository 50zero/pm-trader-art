"""
Serverless API endpoint for Polymarket data fetching
Serves as a CORS proxy and data processor
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../'))

from flask import Flask, jsonify
import requests
import json
import traceback

app = Flask(__name__)

def fetch_trader_data(address):
    """
    Fetch and process Polymarket data for a trader address
    Acts as a CORS proxy and data processor
    """
    try:
        # Import the existing data fetcher logic
        try:
            from data_fetcher import fetch_polymarket_data, process_trader_data
        except ImportError:
            # Fallback implementation if imports fail in serverless environment
            return fetch_polymarket_data_fallback(address)
        
        # Use existing logic
        raw_data = fetch_polymarket_data(address)
        processed_data = process_trader_data(raw_data, address)
        
        return {
            'success': True,
            'data': processed_data
        }
        
    except Exception as e:
        print(f"Error fetching trader data: {e}")
        print(traceback.format_exc())
        return {
            'success': False,
            'error': str(e)
        }

def fetch_polymarket_data_fallback(address):
    """
    Fallback implementation for Polymarket data fetching
    """
    try:
        # Example Polymarket API calls (you'll need to implement based on their actual API)
        headers = {
            'User-Agent': 'Portfolio-Mandala-Educational-Project/1.0',
            'Accept': 'application/json'
        }
        
        # This is a placeholder - replace with actual Polymarket API endpoints
        api_urls = [
            f'https://gamma-api.polymarket.com/events?active=true&limit=100',
            # Add more endpoints as needed
        ]
        
        all_data = []
        for url in api_urls:
            try:
                response = requests.get(url, headers=headers, timeout=10)
                if response.status_code == 200:
                    all_data.extend(response.json())
            except requests.RequestException as e:
                print(f"Error fetching from {url}: {e}")
                continue
        
        # Process and filter data for the specific address
        trader_data = process_data_for_address(all_data, address)
        
        return {
            'success': True,
            'data': trader_data
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': f'Fallback fetch failed: {str(e)}'
        }

def process_data_for_address(raw_data, address):
    """
    Process raw Polymarket data for a specific trader address
    """
    # This is a simplified example - implement based on actual data structure
    trader_events = []
    total_volume = 0
    categories = {}
    
    for event in raw_data:
        # Filter events where this address participated
        # This logic depends on the actual API response structure
        if 'participants' in event and address.lower() in [p.get('address', '').lower() for p in event.get('participants', [])]:
            trader_events.append(event)
            
            # Calculate volume and categories
            volume = event.get('volume', 0)
            category = event.get('category', 'other')
            
            total_volume += volume
            categories[category] = categories.get(category, 0) + volume
    
    # Calculate percentages
    category_percentages = {}
    if total_volume > 0:
        for category, volume in categories.items():
            category_percentages[category] = (volume / total_volume) * 100
    
    return {
        'trader_address': address,
        'total_volume': total_volume,
        'trade_count': len(trader_events),
        'categories': categories,
        'category_percentages': category_percentages,
        'events': trader_events[:10]  # Limit to recent events
    }

def handler(request):
    """
    Vercel serverless function handler for Polymarket data
    Expects URL pattern: /api/polymarket/{address}
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
        
        # Fetch trader data
        result = fetch_trader_data(address)
        
        return jsonify(result)
        
    except Exception as e:
        print(f"Error in polymarket API: {e}")
        print(traceback.format_exc())
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        }), 500

# For local testing
if __name__ == '__main__':
    from flask import request
    app.add_url_rule('/api/polymarket/<address>', 'polymarket', 
                     lambda address: handler(type('obj', (object,), {'path': f'/api/polymarket/{address}'})()))
    app.run(debug=True, port=3002)