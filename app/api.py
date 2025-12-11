#Voy a crear 3 endpoints  /health, /query, /logs

from fastapi import FastAPI, Request, HTTPException, Header
import requests
import os
from dotenv import load_dotenv
from app.main import run_agent, get_logs
from mangum import Mangum

load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")
API_URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET")


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


@api.post("/webhook")
async def telegram_webhook(
    request: Request,
):
    #x_telegram_bot_api_secret_token: str = Header(None) Dentro de los parametros
    # Validación del secret token
    #if x_telegram_bot_api_secret_token != WEBHOOK_SECRET:
     #   print("Webhook llamado sin secret_token válido")
      #  raise HTTPException(status_code=403, detail="Forbidden")

    #if WEBHOOK_SECRET and x_telegram_bot_api_secret_token != WEBHOOK_SECRET:
    #    print(" Secret token inválido o ausente (solo prueba local)")
  

    body = await request.json()
    print("Telegram update received:", body)
    print("API_URL:", API_URL)
    print("BOT_TOKEN:", TOKEN)


    message = body.get("message")
    if not message:
        return {"ok": True}

    chat_id = message["chat"]["id"]
    prompt = message["text"]

    # Ejecuta el agente
    #reply = run_agent(prompt)
    try:
        reply = run_agent(prompt)
    except Exception as e:
        print("Error en run_agent:", e)
        reply = "Hubo un error interno ejecutando la IA."

    # Respuesta a Telegram
    r = requests.post(
        API_URL,
        json={"chat_id": chat_id, "text": reply}
    )
    print("Respuesta Telegram:",r.status_code, r.text)

    return {"ok": True}

handler = Mangum(api)

def lambda_handler(event, context):
    return handler(event, context)
