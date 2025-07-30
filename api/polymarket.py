from http.server import BaseHTTPRequestHandler
import json
import traceback
from urllib.parse import urlparse

class handler(BaseHTTPRequestHandler):
    def _set_cors_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        
    def do_OPTIONS(self):
        self.send_response(200)
        self._set_cors_headers()
        self.end_headers()
        
    def do_GET(self):
        try:
            # Parse the request URL
            parsed_url = urlparse(self.path)
            path_parts = parsed_url.path.strip('/').split('/')
            
            # Simple response for testing
            response_data = {
                'success': True,
                'message': 'Polymarket API is working!',
                'path': self.path,
                'method': 'GET',
                'endpoints': [
                    'GET /api/polymarket/{address} - Get trading data for address'
                ]
            }
            
            # If an address is provided in the path, acknowledge it
            if len(path_parts) > 2 and path_parts[2]:
                address = path_parts[2]
                response_data['address'] = address
                response_data['message'] = f'Polymarket API ready for address {address}'
                # In a real implementation, you would fetch actual trading data here
                response_data['mock_data'] = {
                    'total_volume': 1000,
                    'trade_count': 25,
                    'categories': {'politics': 60, 'sports': 40}
                }
            
            # Send response
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self._set_cors_headers()
            self.end_headers()
            
            self.wfile.write(json.dumps(response_data).encode())
            
        except Exception as e:
            print(f"Error in Polymarket API: {e}")
            print(traceback.format_exc())
            
            # Send error response
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self._set_cors_headers()
            self.end_headers()
            
            error_data = {
                'success': False,
                'error': f'Server error: {str(e)}'
            }
            self.wfile.write(json.dumps(error_data).encode())