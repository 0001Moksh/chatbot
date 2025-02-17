import google.generativeai as genai
from dotenv import dotenv_values

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


a = chat_ai('hi bro')
print(a)