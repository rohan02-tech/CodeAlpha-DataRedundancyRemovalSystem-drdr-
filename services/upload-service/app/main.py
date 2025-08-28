import logging
import hashlib
from flask import Flask, request, jsonify
from google.cloud import firestore, pubsub_v1
from .chunker import ContentDefinedChunker

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Initialize clients
try;
    firestore_client = firestore.Client(project=project_id)
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, 'chunk-processing-topic')
except Exception as e:
    logger.error(f"Failed to initialize clients: {e}")
    raise

class UploadService:
    def __init__(self):
        self.chunker = ContentDefinedChunker()

    def process_upload(self, file_stream, filename, user_id):
        """Process file upload and return chunk manifest"""
        chunk_hashes = []
        
        try:
            for chunk_data in self.chunker.chunk_stream(file_stream):
                chunk_hash = hashlib.sha256(chunk_data).hexdigest()
                chunk_hashes.append(chunk_hash)
                
                # Publish message to Pub/Sub for async processing
                message_data = {
                    'chunk_hash': chunk_hash,
                    'chunk_data': chunk_data.hex(),  # Serialize bytes
                    'user_id': user_id,
                    'filename': filename
                }
                future = publisher.publish(topic_path, data=message_data.encode('utf-8'))
                future.result()  # Wait for publish to complete
                
            return chunk_hashes
        except Exception as e:
            logger.error(f"Error processing upload: {e}")
            raise

upload_service = UploadService()

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'}), 200

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
        
    file = request.files['file']
    user_id = request.headers.get('X-User-ID', 'anonymous')
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
        
    try:
        chunk_hashes = upload_service.process_upload(
            file.stream, 
            file.filename, 
            user_id
        )
        
        # Store file manifest in Firestore
        doc_ref = firestore_client.collection('users').document(user_id)\
                    .collection('files').document(file.filename)
        doc_ref.set({
            'filename': file.filename,
            'chunk_hashes': chunk_hashes,
            'size': sum(len(chunk) for chunk in chunk_hashes),
            'uploaded_at': firestore.SERVER_TIMESTAMP
        })
        
        return jsonify({
            'message': 'File processed successfully',
            'chunks': len(chunk_hashes),
            'file_id': file.filename
        }), 200
        
    except Exception as e:
        logger.error(f"Upload failed: {e}")
        return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False)
