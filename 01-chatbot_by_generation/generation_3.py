########################################################################################
# 3rd generation chatbot
# - scenario (a.k.a) generation by LLM with external data integration
#   . scenario : how to make reponse using other LLMs 
#   . external data : person data, web sesearch, vector database (documents), plugins
# ######################################################################################

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


# dummy external info, e.g,. from database
def get_user_info():
    # import requests
    # requests.get("http://api.xxx.com/users/username/info")
    return   """
    - Like Asia food
    - Like to travel to Spain
    - 30 years old
    """

# dummy external info, e.g,. from database
def get_plannig_manual():
    # import requests
    # requests.get("http://api.xxx.com/company/stragegy/info")
    return """
    - 30 years old man likes eating food.
    - 30 years old man likes walking
    """

SYSTEM_MESSAGE = f""" You are a helpful travel assistant. Your name is Gini, 27 years old"

Current User:
{get_user_info()}

Planning manual:
{get_plannig_manual()}
"""

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
            model = 'gpt-4',
            messages =[
                {'role': 'system', 'content': SYSTEM_MESSAGE}, 
                {'role': 'user', 'content':req.message},     
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
    