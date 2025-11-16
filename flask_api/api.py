"""
Flask API for Hotel Booking Chatbot
Provides REST endpoints to interact with the Rasa chatbot from any frontend
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import requests
import uuid
import logging
import os
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get the absolute path to the flask_api directory
basedir = os.path.abspath(os.path.dirname(__file__))
parent_dir = os.path.dirname(basedir)

app = Flask(__name__, 
            static_folder='static',
            static_url_path='/static')
CORS(app)  # Enable CORS for frontend integration

# Rasa server configuration
RASA_API_URL = "http://localhost:5005"
RASA_WEBHOOKS_URL = f"{RASA_API_URL}/webhooks/rest/webhook"

# Store active sessions (in production, use Redis or a database)
active_sessions = {}


@app.route('/')
def index():
    """Serve the frontend chat interface"""
    return send_from_directory('static', 'index.html')


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    try:
        response = requests.get(f"{RASA_API_URL}/status", timeout=5)
        rasa_status = "running" if response.status_code == 200 else "down"
    except:
        rasa_status = "down"
    
    return jsonify({
        "status": "ok",
        "timestamp": datetime.now().isoformat(),
        "rasa_status": rasa_status
    }), 200


@app.route('/chat', methods=['POST'])
def chat():
    """
    Send a message to the chatbot and get a response
    
    Request JSON:
    {
        "message": "Hello",
        "sender": "user123"  # Optional: If not provided, a new session is created
    }
    
    Response JSON:
    {
        "sender": "user123",
        "responses": [
            {"text": "Hello! I can help you book a hotel room. What's your name?"}
        ],
        "timestamp": "2024-11-16T13:45:00"
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify({
                "error": "Missing 'message' in request body"
            }), 400
        
        user_message = data['message']
        sender_id = data.get('sender', str(uuid.uuid4()))
        
        # Log the conversation
        logger.info(f"User [{sender_id}]: {user_message}")
        
        # Send message to Rasa
        rasa_payload = {
            "sender": sender_id,
            "message": user_message
        }
        
        response = requests.post(
            RASA_WEBHOOKS_URL,
            json=rasa_payload,
            timeout=10
        )
        
        if response.status_code != 200:
            logger.error(f"Rasa error: {response.text}")
            return jsonify({
                "error": "Failed to get response from chatbot",
                "details": response.text
            }), 500
        
        bot_responses = response.json()
        
        # Log bot responses
        for resp in bot_responses:
            logger.info(f"Bot [{sender_id}]: {resp.get('text', '')}")
        
        # Update session
        active_sessions[sender_id] = {
            "last_message": user_message,
            "timestamp": datetime.now().isoformat()
        }
        
        return jsonify({
            "sender": sender_id,
            "responses": bot_responses,
            "timestamp": datetime.now().isoformat()
        }), 200
        
    except requests.exceptions.Timeout:
        logger.error("Rasa request timeout")
        return jsonify({
            "error": "Request timeout - chatbot is taking too long to respond"
        }), 504
    
    except requests.exceptions.ConnectionError:
        logger.error("Cannot connect to Rasa server")
        return jsonify({
            "error": "Cannot connect to chatbot server. Please ensure Rasa is running."
        }), 503
    
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return jsonify({
            "error": "Internal server error",
            "details": str(e)
        }), 500


@app.route('/session/new', methods=['POST'])
def new_session():
    """
    Create a new conversation session
    
    Response JSON:
    {
        "sender": "uuid-here",
        "message": "New session created"
    }
    """
    sender_id = str(uuid.uuid4())
    active_sessions[sender_id] = {
        "created_at": datetime.now().isoformat()
    }
    
    logger.info(f"New session created: {sender_id}")
    
    return jsonify({
        "sender": sender_id,
        "message": "New session created successfully"
    }), 201


@app.route('/session/reset', methods=['POST'])
def reset_session():
    """
    Reset a conversation session
    
    Request JSON:
    {
        "sender": "user123"
    }
    
    Response JSON:
    {
        "sender": "user123",
        "message": "Session reset successfully"
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'sender' not in data:
            return jsonify({
                "error": "Missing 'sender' in request body"
            }), 400
        
        sender_id = data['sender']
        
        # Tell Rasa to reset the conversation
        response = requests.post(
            f"{RASA_API_URL}/conversations/{sender_id}/tracker/events",
            json={"event": "restart"},
            timeout=5
        )
        
        if response.status_code == 200:
            # Remove from active sessions
            if sender_id in active_sessions:
                del active_sessions[sender_id]
            
            logger.info(f"Session reset: {sender_id}")
            
            return jsonify({
                "sender": sender_id,
                "message": "Session reset successfully"
            }), 200
        else:
            return jsonify({
                "error": "Failed to reset session",
                "details": response.text
            }), 500
            
    except Exception as e:
        logger.error(f"Error resetting session: {str(e)}")
        return jsonify({
            "error": "Failed to reset session",
            "details": str(e)
        }), 500


@app.route('/session/active', methods=['GET'])
def active_sessions_list():
    """
    Get list of active sessions
    
    Response JSON:
    {
        "active_sessions": 5,
        "sessions": {...}
    }
    """
    return jsonify({
        "active_sessions": len(active_sessions),
        "sessions": active_sessions
    }), 200


@app.route('/bookings', methods=['GET'])
def get_bookings():
    """
    Get all bookings from the bookings.txt file
    
    Response JSON:
    {
        "bookings": [...],
        "total": 10
    }
    """
    try:
        bookings_file = os.path.join(parent_dir, 'bookings.txt')
        with open(bookings_file, 'r') as f:
            content = f.read()
        
        # Parse bookings (simple parsing, split by separator)
        bookings_raw = content.split('============================================================')
        bookings = []
        
        for booking in bookings_raw:
            if booking.strip() and 'BOOKING CONFIRMATION' in booking:
                bookings.append(booking.strip())
        
        return jsonify({
            "bookings": bookings,
            "total": len(bookings)
        }), 200
        
    except FileNotFoundError:
        return jsonify({
            "bookings": [],
            "total": 0,
            "message": "No bookings found"
        }), 200
    except Exception as e:
        logger.error(f"Error reading bookings: {str(e)}")
        return jsonify({
            "error": "Failed to read bookings",
            "details": str(e)
        }), 500


@app.route('/docs', methods=['GET'])
def api_docs():
    """
    API Documentation
    """
    docs = {
        "title": "Hotel Booking Chatbot API",
        "version": "1.0.0",
        "description": "REST API for interacting with the hotel booking chatbot",
        "endpoints": [
            {
                "path": "/health",
                "method": "GET",
                "description": "Check API and Rasa server health"
            },
            {
                "path": "/chat",
                "method": "POST",
                "description": "Send a message to the chatbot",
                "body": {
                    "message": "string (required)",
                    "sender": "string (optional)"
                }
            },
            {
                "path": "/session/new",
                "method": "POST",
                "description": "Create a new conversation session"
            },
            {
                "path": "/session/reset",
                "method": "POST",
                "description": "Reset an existing conversation",
                "body": {
                    "sender": "string (required)"
                }
            },
            {
                "path": "/session/active",
                "method": "GET",
                "description": "Get list of active sessions"
            },
            {
                "path": "/bookings",
                "method": "GET",
                "description": "Get all bookings from the system"
            },
            {
                "path": "/docs",
                "method": "GET",
                "description": "This documentation"
            }
        ],
        "examples": {
            "chat": {
                "request": {
                    "message": "I want to book a room",
                    "sender": "user123"
                },
                "response": {
                    "sender": "user123",
                    "responses": [
                        {"text": "Great! What's your name?"}
                    ],
                    "timestamp": "2024-11-16T13:45:00"
                }
            }
        }
    }
    
    return jsonify(docs), 200


if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 Hotel Booking Chatbot API Starting...")
    print("="*60)
    print(f"🌐 Frontend: http://localhost:5001")
    print(f"📡 API Server: http://localhost:5001")
    print(f"🤖 Rasa Server: {RASA_API_URL}")
    print(f"📚 Documentation: http://localhost:5001/docs")
    print(f"💚 Health Check: http://localhost:5001/health")
    print("="*60 + "\n")
    print("💡 Open http://localhost:5001 in your browser to chat!")
    print("\n")
    
    app.run(host='0.0.0.0', port=5001, debug=True)

