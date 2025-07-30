from http.server import BaseHTTPRequestHandler
import json
import traceback
from urllib.parse import urlparse, parse_qs

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # Parse the request URL
            parsed_url = urlparse(self.path)
            path_parts = parsed_url.path.strip('/').split('/')
            
            # Simple response for testing
            response_data = {
                'success': True,
                'message': 'Mandala API is working!',
                'path': self.path,
                'method': 'GET',
                'timestamp': '2025-07-30T15:25:00Z'
            }
            
            # Send response
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            self.wfile.write(json.dumps(response_data).encode())
            
        except Exception as e:
            print(f"Error in mandala API: {e}")
            print(traceback.format_exc())
            
            # Send error response
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            
            error_data = {
                'success': False,
                'error': f'Server error: {str(e)}'
            }
            self.wfile.write(json.dumps(error_data).encode())