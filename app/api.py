#Voy a crear 3 endpoints  /health, /query, /logs

from fastapi import FastAPI
from app.main import run_agent, get_logs
from mangum import Mangum


api = FastAPI()

@api.get('/health')
def health():
     return {"status": "ok"}

@api.get('/query')
def query_agent(prompt: str):
     response = run_agent(prompt)
     return {"Result": response}

@api.get('/logs')
def log_history():
     logs = get_logs()
     return {"logs": logs}

handler = Mangum(api)

def lambda_handler(event, context):
    return handler(event, context)