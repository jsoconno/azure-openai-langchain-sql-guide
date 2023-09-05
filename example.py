import os
from langchain.llms import AzureOpenAI
import openai
from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.sql_database import SQLDatabase
from dotenv import load_dotenv

load_dotenv()

# Configure OpenAI API
openai.api_type = os.getenv('OPENAI_API_TYPE')
openai.api_version = os.getenv('OPENAI_API_VERSION')
openai.api_base = os.getenv('OPENAI_API_BASE')
openai.api_key = os.getenv("OPENAI_API_KEY")

llm = AzureOpenAI(deployment_name="gpt-35-turbo-16k", model_name="gpt-35-turbo-16k")

database_username = os.getenv("TF_VAR_sql_server_username")
database_password = os.getenv("TF_VAR_sql_server_password")
database_server = os.getenv("TF_VAR_sql_server_name")
database_db = os.getenv("TF_VAR_sql_server_database_name")

# connection_string = f"mssql+pymssql://{database_user}:{database_password}@{database_server}.database.windows.net:1433/{database_db}"
connection_string = (
    f"mssql+pyodbc://{database_username}:{database_password}@{database_server}.database.windows.net:1433/"
    "{database_db}?driver=ODBC+Driver+18+for+SQL+Server"
)

db = SQLDatabase.from_uri(connection_string)
toolkit = SQLDatabaseToolkit(db=db, llm=llm, reduce_k_below_max_tokens=True)

agent_executor = create_sql_agent(
    llm=llm,
    toolkit=toolkit,
    verbose=True
)

toolkit = SQLDatabaseToolkit(db=db)

agent_executor = create_sql_agent(
    llm=llm,
    toolkit=toolkit,
    verbose=True
)

agent_executor.run("Find the 5 most expensive records!")