from flask import Blueprint, jsonify, request
from werkzeug.utils import secure_filename
import os
import tempfile
import logging
from ..text_extractors import extract_text_from_file
from ..crew.document_crew import DocumentCrewOrchestrator


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

document_bp = Blueprint('document', __name__)

ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
# file upload 
@document_bp.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload and text extraction"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'File type not supported. Please upload PDF, DOCX, or TXT files.'}), 400
        
        # Save file to a temporary location
        filename = secure_filename(file.filename)
        file_extension = filename.rsplit('.', 1)[1].lower()
        
        # Create a temporary directory instead of file
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_file_path = os.path.join(temp_dir, filename)
            file.save(temp_file_path)
            
            # Extract text
            extracted_text = extract_text_from_file(temp_file_path, file_extension)
        
        logger.info(f"File uploaded: {filename}, size: {len(extracted_text)} chars")
        return jsonify({
            'success': True,
            'filename': filename,
            'extracted_text': extracted_text,
            'text_length': len(extracted_text)
        })
    
    except Exception as e:
        logger.error(f"Upload error: {str(e)}")
        return jsonify({'error': str(e)}), 500


@document_bp.route('/process-text', methods=['POST'])
def process_text():
    """Process text input directly (without file upload)"""
    try:
        data = request.json
        if not data or 'text' not in data:
            return jsonify({'error': 'No text provided'}), 400
        
        text = data['text']
        if not text.strip():
            return jsonify({'error': 'Empty text provided'}), 400
        
        logger.info(f"Text processed directly, size: {len(text)} chars")
        return jsonify({
            'success': True,
            'text': text,
            'text_length': len(text)
        })
    
    except Exception as e:
        logger.error(f"Text processing error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@document_bp.route('/summarize', methods=['POST'])
def summarize_document():
    """Summarize the provided text"""
    try:
        data = request.json
        if not data or 'text' not in data:
            return jsonify({'error': 'No text provided'}), 400
        
        text = data['text']
        summary_type = data.get('summary_type', 'general')
        
        # Use CrewAI orchestrator
        orchestrator = DocumentCrewOrchestrator(text)
        summary = orchestrator.summarize(summary_type)
        if not isinstance(summary, str):
            summary = str(summary)
        
        return jsonify({
            'success': True,
            'summary': summary,
            'summary_type': summary_type
        })
    
    except Exception as e:
        logger.error(f"Summarization error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@document_bp.route('/improve', methods=['POST'])
def improve_document():
    """Improve the language and structure of the document"""
    try:
        data = request.json
        if not data or 'text' not in data:
            return jsonify({'error': 'No text provided'}), 400
        
        text = data['text']
        improvement_type = data.get('improvement_type', 'general')
        
        # Use CrewAI orchestrator
        orchestrator = DocumentCrewOrchestrator(text)
        improved_text = orchestrator.improve(improvement_type)
        
        return jsonify({
            'success': True,
            'improved_text': improved_text,
            'improvement_type': improvement_type
        })
    
    except Exception as e:
        logger.error(f"Improvement error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@document_bp.route('/generate-addons', methods=['POST'])
def generate_addons():
    """Generate helpful add-ons like follow-up emails, headlines, or slide content"""
    try:
        data = request.json
        if not data or 'text' not in data:
            return jsonify({'error': 'No text provided'}), 400
        
        text = data['text']
        addon_type = data.get('addon_type', 'headlines')
        
        # Use CrewAI orchestrator
        orchestrator = DocumentCrewOrchestrator(text)
        addon_content = orchestrator.generate_addons(addon_type)
        
        return jsonify({
            'success': True,
            'addon_content': addon_content,
            'addon_type': addon_type
        })
    
    except Exception as e:
        logger.error(f"Addon generation error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@document_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'service': 'document_enhancement_system'})