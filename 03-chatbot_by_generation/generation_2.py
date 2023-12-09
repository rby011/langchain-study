########################################################################################
# 2nd generation chatbot
#
# 사용자의 메시지에서 의도를 파악하는 LLM 과 파악된 의도에 맞는 LLM 이 이를 처리하는 구조
# - intention 파악은 gpt4 에게
# - intention 에 따라 대응하는 것은 gpt 3.5 에게
# ########################################################################################

import os
import openai 
from dotenv import load_dotenv

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# key management
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# backend configuration - rest api
app = FastAPI(debug=True)
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods = ['*'],
    allow_headers=['*']
)

# user request formatting
class ChatRequest(BaseModel):
    message:str
    temperature: float =1

# persona setting
SYSTEM_MESSAGE = "You are a helpful travel assistant. Your name is Gini, 27 years old"

def classify_intent(msg):
    prompt  = f""" Your job is to classify intent.
    
    Choose one of the following intents:
    - travel_plan
    - customer_support
    - revervation
    
    User : {msg}
    Intent : 
    """
    response = openai.ChatCompletion.create(
        model = 'gpt-4',
        messages =[
           {'role' : 'user', 'content' : prompt} 
        ] ,
    )
    
    print(response)
    
    return response.choices[0].message.content.strip()

# route configuration - client interaction
@app.post('/chat')
def chat(req:ChatRequest): 
    
    intent = classify_intent(req.message)
    
    if intent == 'travel_plan':
        response = openai.ChatCompletion.create(
            model = 'gpt-3.5-turbo',
            messages =[
                {'role': 'system', 'content': SYSTEM_MESSAGE}, 
                {'role': 'user', 'content':req.message}, # parsing by pydantic     
            ],
            temperature = req.temperature,
        )
        return {'message': response.choices[0].message.content}
    
    elif intent == 'customer_support':
        return {'message': 'here is customer support : 2132'}
    
    elif intent == 'reservation':
        return {'message': 'here is revseratio number : 123'}

# backend run
if __name__ == '__main__':
    import uvicorn
    
    uvicorn.run(app, host="0.0.0.0" , port=8000)
    