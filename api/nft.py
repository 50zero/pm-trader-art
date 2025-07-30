from http.server import BaseHTTPRequestHandler
import json
import traceback
from urllib.parse import urlparse

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            response_data = {
                'success': True,
                'message': 'NFT API is working!',
                'path': self.path,
                'method': 'GET',
                'endpoints': [
                    'GET /api/nft - Get NFT info',
                    'POST /api/nft - Mint NFT'
                ]
            }
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            self.wfile.write(json.dumps(response_data).encode())
            
        except Exception as e:
            print(f"Error in NFT API: {e}")
            print(traceback.format_exc())
            
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            
            error_data = {
                'success': False,
                'error': f'Server error: {str(e)}'
            }
            self.wfile.write(json.dumps(error_data).encode())