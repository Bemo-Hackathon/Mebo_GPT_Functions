from flask import Blueprint, request, jsonify
from .utils import identify_persona, greetings_persona, notification_offer, notify_customer_payment_status_with_gpt, call_openai_api
import requests
import os

api = Blueprint('api', __name__)

API_KEY = os.getenv('API_KEY')
BASE_URL = "https://api.openai.com/v1"
DEFAULT_MODEL = "gpt-3.5-turbo-0125"

@api.route('/persona', methods=['POST'])
def persona():
    customer_data = request.json
    try:
        persona = identify_persona(customer_data)
        return jsonify({"persona": persona}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api.route('/greeting', methods=['POST'])
def greeting():
    customer_data = request.json
    try:
        greeting_msg = greetings_persona(customer_data)
        return jsonify({"greeting": greeting_msg}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api.route('/offer', methods=['POST'])
def offer():
    customer_data = request.json
    try:
        offer_msg = notification_offer(customer_data)
        return jsonify({"offer": offer_msg}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api.route('/payment-status', methods=['POST'])
def payment_status():
    customer_data = request.json
    try:
        payment_msg = notify_customer_payment_status_with_gpt(customer_data)
        return jsonify({"payment_notification": payment_msg}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@api.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_input = data.get("user_input")
    customer_data = data.get("customer_data")

    if not user_input or not customer_data:
        return jsonify({"error": "user_input e customer_data são necessários."}), 400

    try:
        greeting = greetings_persona(customer_data)
        
        prompt = f"{greeting}\n{user_input}\n"

        assistant_response = call_openai_api(prompt)

        return jsonify({"response": assistant_response}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
