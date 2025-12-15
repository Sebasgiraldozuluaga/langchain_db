#Importamos librerias 
from dotenv import load_dotenv
import os
import yaml

from langchain_openai import ChatOpenAI
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent, SQLDatabaseToolkit

#cargar las env
load_dotenv()

DATABASE_URL = (
    f"postgresql://{os.getenv('PG_USER')}:{os.getenv('PG_PASSWORD')}"
    f"@{os.getenv('PG_HOST')}:{os.getenv('PG_PORT')}/{os.getenv('PG_DATABASE')}"
)

with open("system_agent.yaml", "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)



llm = ChatOpenAI(model=config["agent"].get("model", "gpt-4o-mini"), temperature=0)
db = SQLDatabase.from_uri(DATABASE_URL)

agent = create_sql_agent(
    llm=llm,
    toolkit=SQLDatabaseToolkit(db=db, llm=llm),
    agent_type="tool-calling",
    verbose=True,
    prefix=config["agent"]["system_prompt"]
)

def run_agent(query: str) -> str:
    result = agent.invoke({"input": query})
    return result["output"]
    
    