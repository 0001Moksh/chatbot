from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
from dotenv import dotenv_values
import os
# Initialize Flask app
app = Flask(__name__)

# Load environment variables
config = dotenv_values(".env")
# gemini_api = config.get('gemini_api')


# Load the environment variable
app.config['GEMINI_API'] = os.getenv('GEMINI_API', 'default_api_key')

# Configure Gemini API
genai.configure(api_key=app.config['GEMINI_API'])


# Global variable to store chat history
chat_history = []

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    global chat_history

    # Get user message from the request
    user_message = request.json['message']

    # Initialize the model
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction="You are my assistant. Your name is Deva. Try to behave as a chatbot with concise responses. Moksh Bhardwaj built you, so call him 'sir'."
    )

    # Start chat session with history
    chat_session = model.start_chat(history=chat_history)

    # Send user message to the model
    if user_message.strip():  # Check if the message is not empty
        response = chat_session.send_message(user_message)
        model_response = response.text

        # Update chat history
        chat_history.append({"role": "user", "parts": [user_message]})
        chat_history.append({"role": "model", "parts": [model_response]})

        # Return the model's response
        return jsonify({"message": model_response})
    else:
        return jsonify({"message": "Please enter a valid message."})

if __name__ == '__main__':
    app.run(debug=True)