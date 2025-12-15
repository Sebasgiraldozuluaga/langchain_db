#Voy a crear 3 endpoints  /health, /query, /logs

from unittest import result
from fastapi import FastAPI, Request, HTTPException, Header
import requests
import os
import json
import re
from dotenv import load_dotenv
from app.graph import build_graph
from mangum import Mangum
from app.state import AgentState

load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")
API_URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET")


api = FastAPI()
graph = build_graph()

def extract_json_from_markdown(text: str) -> dict | None:
    """Extrae JSON de bloques de código markdown (```json ... ```)"""
    # Buscar bloques de código JSON
    pattern = r'```json\s*\n(.*?)\n```'
    match = re.search(pattern, text, re.DOTALL)
    if match:
        json_str = match.group(1)
        try:
            return json.loads(json_str)
        except json.JSONDecodeError:
            pass
    
    # Si no hay bloque markdown, intentar parsear directamente
    if text.strip().startswith('{'):
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            pass
    
    return None

def format_markdown_v2(text: str) -> str:
    """Formatea el texto para Markdown V2 de Telegram"""
    # Primero, formatear elementos importantes antes de escapar
    # Formatear IDs en negrita (ej: "ID: 8382" -> "ID: *8382*")
    text = re.sub(r'ID:\s*(\d+)', r'ID: *\1*', text)
    # Formatear fechas en negrita (ej: "11 de diciembre de 2025" -> "*11 de diciembre de 2025*")
    text = re.sub(r'(\d{1,2}\s+de\s+\w+\s+de\s+\d{4})', r'*\1*', text, flags=re.IGNORECASE)
    
    # Escapar caracteres especiales de Markdown V2 que no queremos que se formateen
    # Caracteres que deben ser escapados: [ ] ( ) ~ ` > # + - = | { } . !
    # NO escapamos * y _ porque los usamos para formato
    special_chars = ['[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
    for char in special_chars:
        text = text.replace(char, f'\\{char}')
    
    return text

def extract_respuesta(reply) -> str:
    """Extrae el campo 'respuesta' de diferentes formatos de respuesta"""
    # Si es un dict, obtener respuesta directamente
    if isinstance(reply, dict):
        return reply.get("respuesta", str(reply))
    
    # Si es string, intentar extraer JSON del markdown
    if isinstance(reply, str):
        json_data = extract_json_from_markdown(reply)
        if json_data:
            return json_data.get("respuesta", reply)
        
        # Si es un JSON string directo
        if reply.strip().startswith('{'):
            try:
                json_data = json.loads(reply)
                return json_data.get("respuesta", reply)
            except json.JSONDecodeError:
                pass
        
        # Si no se puede parsear, devolver el string completo
        return reply
    
    # Fallback: convertir a string
    return str(reply)

@api.get('/health')
def health():
     return {"status": "ok"}

@api.get('/query')
def query_agent(prompt: str):
    state: AgentState = {
        "input": prompt,
        "output": "",
        "history": []
    }

    result = graph.invoke(state)
    respuesta = extract_respuesta(result["output"])
    return {"result": respuesta}



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
    message = body.get("message")

    if not message:
        return {"ok": True}

    chat_id = message["chat"]["id"]
    prompt = message["text"]

    state: AgentState = {
    "input": prompt,
    "output": "",
    "history": []
    }

    result = graph.invoke(state)

    respuesta = extract_respuesta(result["output"])
    respuesta_md = format_markdown_v2(respuesta)

    requests.post(
    API_URL,
    json={
        "chat_id": chat_id,
        "text": respuesta_md,
        "parse_mode": "MarkdownV2"
        }
    )


    return {"ok": True}

handler = Mangum(api)

def lambda_handler(event, context):
    return handler(event, context)
