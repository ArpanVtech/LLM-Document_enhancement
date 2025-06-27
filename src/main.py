import os
import sys

# Ensure the parent directory is in the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.demo_app import app

if __name__ == '__main__':
    # Print current working directory for debugging
    print(f"Current working directory: {os.getcwd()}")
    
    # Run the app
    app.run(host='0.0.0.0', port=3000, debug=True)