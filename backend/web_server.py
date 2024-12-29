import os
import httpx
from fastapi import FastAPI
from dotenv import load_dotenv, set_key
from urllib.parse import urlencode

# Good practice to define env varialbes before the app starts and we can use pydantic to validate the env file
load_dotenv()
client_id = os.getenv('UPSTOX_API_KEY')
client_secret = os.getenv('UPSTOX_API_SECRET')
redirect_uri = 'http://127.0.0.1:8000/oauth/callback'

app = FastAPI()

@app.get('/')
def check():
    return {"status": "Healthy"}

@app.get('/login')
def login():
    base_url = "https://api.upstox.com/v2/login/authorization/dialog"
    query = {
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "response_type": "code"
    }
    query = urlencode(query)
    url = base_url+'?'+query
    return {"url":url}

@app.get("/oauth/callback")
async def oauth_callback(code: str, state: str | None = None):
    # Perform further actions like exchanging the code for an access token
    # return {
    #     "message": "Authorization successful",
    #     "code": code,
    #     "state": state
    # }
    base_url = 'https://api.upstox.com/v2/login/authorization/token'
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    data = {
        'code': code,
        'client_id': client_id,
        'client_secret': client_secret,
        'redirect_uri': redirect_uri,
        'grant_type': 'authorization_code'
    }
    async with httpx.AsyncClient() as client:
        res = await client.post(base_url, headers=headers, data=data)
        data = res.json()
        
    if res.status_code == 200:
        set_key('.env', 'UPSTOX_ACCESS_TOKEN', data['access_token'])
        return {'status': 'success', 'access_token': data['access_token']}
    return data