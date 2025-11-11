"""
Flask Web Application for Hotel Booking Chatbot UI
This is the frontend server that communicates with the Rasa backend
"""
from flask import Flask, render_template, request, jsonify
import requests
import uuid
import os

app = Flask(__name__)

# Rasa server configuration - can be changed via environment variables
RASA_API_URL = os.getenv('RASA_API_URL', 'http://localhost:5005/webhooks/rest/webhook')


@app.route('/')
def index():
    """Render the main chat interface"""
    return render_template('index.html')


@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat messages and communicate with Rasa"""
    try:
        user_message = request.json.get('message')
        session_id = request.json.get('session_id')
        
        if not user_message:
            return jsonify({'error': 'No message provided'}), 400
        
        # Generate session ID if not provided
        if not session_id:
            session_id = str(uuid.uuid4())
        
        # Send message to Rasa
        payload = {
            'sender': session_id,
            'message': user_message
        }
        
        response = requests.post(RASA_API_URL, json=payload, timeout=10)
        
        if response.status_code == 200:
            bot_responses = response.json()
            return jsonify({
                'session_id': session_id,
                'responses': [msg.get('text', '') for msg in bot_responses]
            })
        else:
            return jsonify({'error': 'Failed to get response from bot'}), 500
            
    except requests.exceptions.ConnectionError:
        return jsonify({'error': 'Cannot connect to chatbot server. Please ensure Rasa is running on port 5005.'}), 503
    except requests.exceptions.Timeout:
        return jsonify({'error': 'Request timed out. The chatbot server is not responding.'}), 504
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    try:
        # Check if Rasa server is reachable
        response = requests.get('http://localhost:5005/', timeout=2)
        return jsonify({
            'status': 'ok',
            'ui': 'running',
            'rasa_backend': 'reachable' if response.status_code < 500 else 'unreachable'
        })
    except:
        return jsonify({
            'status': 'ok',
            'ui': 'running',
            'rasa_backend': 'unreachable'
        }), 200


if __name__ == '__main__':
    print("\n" + "="*60)
    print("🏨 Hotel Booking Chatbot - Web Interface")
    print("="*60)
    print(f"Frontend Server: http://localhost:5001")
    print(f"Backend (Rasa):  {RASA_API_URL}")
    print("="*60)
    print("\n⚠️  Make sure Rasa server is running on port 5005!")
    print("   Run: rasa run --enable-api --cors \"*\"\n")
    
    app.run(debug=True, host='0.0.0.0', port=5001)

