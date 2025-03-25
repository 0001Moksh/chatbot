import markdown2
import re
from bs4 import BeautifulSoup
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
# from dotenv import dotenv_values
import os
# Initialize Flask app
app = Flask(__name__)

# Load environment variables
# config = dotenv_values(".env")
# gemini_api = config.get('gemini_api')


# Load the environment variable
app.config['GEMINI_API'] = os.getenv('GEMINI_API', 'default_api_key')

# Configure Gemini API
genai.configure(api_key=app.config['GEMINI_API'])
# genai.configure(api_key="AIzaSyDBiMuUtYvPI2WuDqF1NqdOgd8EtRr72So")


def clean_response(text):
    # Remove HTML first
    soup = BeautifulSoup(text, "html.parser")
    clean_text = soup.get_text(separator="\n")

    # Convert markdown to plain text
    clean_text = markdown2.markdown(clean_text)
    clean_text = re.sub(r'<[^>]+>', '', clean_text)  # Remove remaining HTML tags

    return clean_text.strip()



# Global variable to store chat history
chat_history = []

@app.route('/')
def home():
    return render_template('ui.html')

@app.route('/chat', methods=['POST'])
def chat():
    global chat_history

    # Get user message from the request
    user_message = request.json['message']

    # Initialize the model
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction="You are my assistant. Your name is Deva. Try to behave as a chatbot with concise responses. Moksh Bhardwaj built you and portfolio is https://mokshbhardwaj.netlify.app/, so call him 'sir'."
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

#         # Return the model's response
#         test_responses = ['''
# ### *Test Script for Cleaning Response*  
# python
# from bs4 import BeautifulSoup

# def clean_response(text):
#     soup = BeautifulSoup(text, "html.parser")
#     return soup.get_text(separator="\n")  # Keeps proper formatting

# # Example test cases
# test_responses = [
#     "<b>Our new product</b> is launching soon.",
#     "<strong>The deadline is Friday.</strong>",
#     "<i>This is italic text.</i> Avoid overusing <b>bold</b>.",
#     "Plain text without HTML."
# ]

# ''']
#         model_response = test_responses[0]
        model_response = clean_response(model_response)

        return jsonify({"message": model_response})
    else:
        return jsonify({"message": "Please enter a valid message."})




















if __name__ == '__main__':
    app.run(debug=True)