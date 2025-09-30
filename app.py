from flask import Flask, jsonify
import os
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        'status': 'success',
        'message': 'Project Prometheus Backend is running!',
        'timestamp': datetime.utcnow().isoformat(),
        'version': '1.0.0'
    })

@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy',
        'service': 'ppfdbe'
    }), 200

@app.route('/api/test')
def test():
    return jsonify({
        'status': 'success',
        'data': {
            'message': 'CI/CD test endpoint',
            'environment': os.getenv('ENV', 'production'),
            'region': 'asia-northeast3'
        }
    })

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8080))
    app.run(host='0.0.0.0', port=port)