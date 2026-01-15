"""
Application entry point for development.

Run with: python run.py
"""
import os
from app import create_app

# Get configuration from environment variable
config_name = os.environ.get('FLASK_CONFIG', 'development')
app = create_app(config_name)


if __name__ == '__main__':
    # Get host and port from environment
    host = os.environ.get('FLASK_HOST', '0.0.0.0')
    port = int(os.environ.get('FLASK_PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║        Therapy Session Management - Development Server       ║
╠══════════════════════════════════════════════════════════════╣
║  URL:    http://{host}:{port}                              
║  Config: {config_name}                                       
║  Debug:  {debug}                                             
╚══════════════════════════════════════════════════════════════╝
    """)
    
    app.run(host=host, port=port, debug=debug)
