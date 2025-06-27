
from flask import Flask, send_from_directory
from flask_cors import CORS
import os
import logging
from src.routes.Document import document_bp  # Import the blueprint

# Get the absolute path to the project root
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
static_folder = os.path.join(project_root, 'static')

app = Flask(__name__, static_folder=static_folder)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Print paths for debugging
logger.info(f"Project root: {project_root}")
logger.info(f"Static folder: {static_folder}")
logger.info(f"Index.html exists: {os.path.exists(os.path.join(static_folder, 'index.html'))}")

# Register the document blueprint with the main app
app.register_blueprint(document_bp, url_prefix='/api')

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory(app.static_folder, path)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)