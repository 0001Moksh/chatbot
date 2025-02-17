from flask import Flask, request, render_template
import google.generativeai as genai
from dotenv import dotenv_values

app = Flask(__name__)
config = dotenv_values(".env")
gemini_api=config.get('gemini_api')

def chat_ai(user_input): 
    history = []
    genai.configure(api_key=gemini_api)
    model = genai.GenerativeModel(model_name="gemini-1.5-flash",system_instruction="You are a my assistant. Your name is Deva, call me sir")
    if user_input != "":
        chat_session = model.start_chat(history=history)
        response = chat_session.send_message(user_input)
        model_response =response.text
        history.append({"role":"user","parts":[user_input]})
        history.append({"role":"model","parts":[model_response]})
    return model_response


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/chat', methods=['POST','GET'])
def chat():
    if request.method == 'POST':
        query = request.form.get('text')
        response = chat_ai(query)
        if not response:  # Fixing the `.empty` issue
            response = "Chatbot is currently unavailable. Please try again later."
        return render_template('index.html', response=response)
    
    return render_template('index.html', response="Ask me anything!")


if __name__ == '__main__':
    app.run(debug=True)