import os
from dotenv import load_dotenv
from langchain.llms import AzureOpenAI
from langchain.chat_models import AzureChatOpenAI
from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.sql_database import SQLDatabase
from langchain.schema import SystemMessage
import openai

def main():
    # Configure openai api
    openai.api_type = os.getenv('OPENAI_API_TYPE')
    openai.api_version = os.getenv('OPENAI_API_VERSION')
    openai.api_base = os.getenv('OPENAI_API_BASE')
    openai.api_key = os.getenv("OPENAI_API_KEY")

    # Configure database
    database_username = os.getenv("SQL_SERVER_USERNAME")
    database_password = os.getenv("SQL_SERVER_PASSWORD")
    database_server = os.getenv("SQL_SERVER_NAME")
    database_db = os.getenv("SQL_SERVER_DATABASE_NAME")
    
    # Create connection string
    connection_string = (
        f"mssql+pyodbc://{database_username}:{database_password}@"
        f"{database_server}.database.windows.net:1433/"
        f"{database_db}?driver=ODBC+Driver+18+for+SQL+Server"
    )

    # Connect to the database
    db = SQLDatabase.from_uri(connection_string, schema="SalesLT")

    # # Use a completion model deployment
    # llm = AzureOpenAI(
    #     deployment_name="text-davinci-003",
    #     model_name="text-davinci-003"
    # )

    # Use a chat model deployment
    llm = AzureChatOpenAI(
        deployment_name="gpt-35-turbo-16k",
        model="gpt-35-turbo-16k",
        temperature=0.5
    )

    # Use sql database toolkit
    toolkit = SQLDatabaseToolkit(db=db, llm=llm, reduce_k_below_max_tokens=True)

    # Create the sql agent
    agent_executor = create_sql_agent(
        llm=llm,
        toolkit=toolkit,
        verbose=True,
        agent_executor_kwargs={
            "system_message": SystemMessage(content="You are an expert SQL data analyst.")
        }
    )

    try:
        result = agent_executor.run("Return the customer with the highest sales order total (TotalDue) as well as the purchase order number and aggregate amount (rounded to the nearest whole number) in the format '<customer_name> had the highest sales order total at <dollar_amount> as part of purchase order <purchase_order_number>.'")
        return result
    except Exception as e:
        return None

if __name__ == "__main__":
    result = main()
    print(result)
