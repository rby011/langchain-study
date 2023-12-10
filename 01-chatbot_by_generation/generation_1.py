########################################################################################
# 1st generation chatbot
#
# 사용자의 메시지를 LLM 에 그데로 전달하고 응답을 받아 전달하는 방식
########################################################################################

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

# route configuration - client interaction
@app.post('/chat')
def chat(req:ChatRequest): # pythantic formatted request
    response = openai.ChatCompletion.create(
        model = 'gpt-3.5-turbo',
        messages =[
            {'role': 'system', 'content': SYSTEM_MESSAGE}, 
            {'role': 'user', 'content':req.message}, # parsing by pydantic     
        ],
        temperature = req.temperature,
    )
    return {'message': response.choices[0].message.content}

# backend run
if __name__ == '__main__':
    import uvicorn
    
    uvicorn.run(app, host="0.0.0.0" , port=8000)
    