import os
import google.generativeai as palm

from google.cloud import bigquery
from sqlalchemy import *
from sqlalchemy.engine import create_engine
from sqlalchemy.schema import *

from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.agents import AgentExecutor
from langchain.sql_database import SQLDatabase
from langchain.embeddings import GooglePalmEmbeddings
from langchain.llms import GooglePalm


service_account_file = "your_sa_account_key_file.json"
os.environ['GOOGLE_API_KEY'] = 'your_palm_api_key'
palm.configure(api_key='GOOGLE_API_KEY')
project = "your_project_id"
dataset = "your_dataset"
table = "you_table"
sqlalchemy_url = f'bigquery://{project}/{dataset}?credentials_path={service_account_file}'

llm = GooglePalm()
llm.temperature = 0.1

db = SQLDatabase.from_uri(sqlalchemy_url)
toolkit = SQLDatabaseToolkit(db=db, llm=llm)

agent_executor = create_sql_agent(
llm=llm,
toolkit=toolkit,
verbose=True,
top_k=1000,
)

agent_executor.run("Who are the top 3 buyers?")