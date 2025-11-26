#Importamos librerias 
from dotenv import load_dotenv
import os
import yaml

from langchain_openai import ChatOpenAI
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent, SQLDatabaseToolkit
from langchain_community.agent_toolkits.sql.base import (
   create_sql_agent as create_sql_agent,)
from langchain.agents import create_agent


#cargar las env
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PG_HOST = os.getenv("PG_HOST")
PG_DATABASE = os.getenv("PG_DATABASE")
PG_USER = os.getenv("PG_USER")
PG_PASSWORD = os.getenv("PG_PASSWORD")
PG_PORT = os.getenv("PG_PORT")
DATABASE_URL = f"postgresql://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DATABASE}"

with open('system_agent.yaml', 'r',encoding='utf-8') as f:
    config = yaml.safe_load(f)

print(config['agent']['system_prompt'])
#Cargar el prompt para el agente
system_prompt = config['agent']['system_prompt']
model_name = config['agent']['model']

#Crear el LLM
llm = ChatOpenAI(
    model_name = model_name,
    temperature=0
)


db = SQLDatabase.from_uri(DATABASE_URL)

toolkit = SQLDatabaseToolkit(db=db, llm=llm)

#Crear el agente

#agent1 = create_agent(
#    llm=llm,
#    tools=tools,
#    agent_type = "tool-calling",
#    verbose = True,
#    system_message = system_prompt
#)

agent = create_sql_agent(
    llm=llm,
    toolkit=toolkit,
    agent_type="tool-calling",  # también puedes probar "openai-tools" o quitarlo
    verbose=True,
    prefix = system_prompt #implementacion del YAML
)   

#Consulta
query = "¿Ultima compra de la tabla factura dame valor?"
response = agent.run(query)
print(response)


#GENERAR UN PROMPT PERSONALIZADO 

#  DARLE CONTEXTO CON QUERIES 
    