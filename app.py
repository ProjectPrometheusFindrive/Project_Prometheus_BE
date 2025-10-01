from flask import Flask, jsonify
import os
from datetime import datetime
from database import db_instance

app = Flask(__name__)

# MongoDB 연결 초기화
@app.before_request
@app.before_request
def before_first_request():
    if not db_instance.is_connected():
        db_instance.connect()

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
    db_status = 'connected' if db_instance.is_connected() else 'disconnected'
    status_code = 200 if db_status == 'connected' else 503

    return jsonify({
        'status': 'healthy' if db_status == 'connected' else 'degraded',
        'service': 'ppfdbe',
        'database': db_status
    }), status_code

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

@app.route('/api/db-test')
def db_test():
    try:
        if not db_instance.is_connected():
            if not db_instance.connect():
                return jsonify({'status': 'error', 'message': 'database connection failed'}), 503
        db = db_instance.get_db()
        if db is None:
            return jsonify({'status': 'error', 'message': 'database handle unavailable'}), 500
        col = db['test_items']
        now = datetime.utcnow()
        doc = {'status': 'created', 'note': 'db connectivity test', 'createdAt': now}
        inserted_id = col.insert_one(doc).inserted_id
        col.update_one({'_id': inserted_id}, {'$set': {'status': 'updated'}})
        saved = col.find_one({'_id': inserted_id})
        payload = {
            '_id': str(saved.get('_id')) if saved else None,
            'status': saved.get('status') if saved else None,
            'createdAt': saved.get('createdAt').isoformat() if saved and saved.get('createdAt') else None
        }
        return jsonify({'status': 'success', 'collection': 'test_items', 'document': payload}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
