#!/usr/bin/env python3
"""
Portfolio Mandala Web Server
Run this script to start the web interface for generating portfolio mandalas.
"""

import os
import sys
from web_app import app

def main():
    print("🎨 Portfolio Mandala Generator")
    print("=" * 40)
    print("Starting web server...")
    print("🌐 Open your browser and go to: http://localhost:5000")
    print("📱 Or access from your network: http://[your-ip]:5000")
    print("🛑 Press Ctrl+C to stop the server")
    print("=" * 40)
    
    try:
        app.run(
            debug=True,
            host='0.0.0.0',
            port=5000,
            use_reloader=False  # Disable reloader to prevent double startup messages
        )
    except KeyboardInterrupt:
        print("\n👋 Server stopped. Thanks for using Portfolio Mandala!")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()