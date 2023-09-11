import os
from dotenv import load_dotenv

# from langchain.llms import AzureOpenAI
from langchain.chat_models import AzureChatOpenAI
from langchain.llms.loading import load_llm
from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.sql_database import SQLDatabase
from langchain.schema import SystemMessage

# from langchain.memory import ChatMessageHistory
import openai
from langchain.agents import tool


@tool
def get_word_length(word: str) -> int:
    """Returns the length of a word."""
    return len(word)


tools = [get_word_length]


def main():
    # Configure openai api
    openai.api_type = os.getenv("OPENAI_API_TYPE")
    openai.api_version = os.getenv("OPENAI_API_VERSION")
    openai.api_base = os.getenv("OPENAI_API_BASE")
    openai.api_key = os.getenv("OPENAI_API_KEY")

    # Use a chat model deployment
    llm = load_llm("./llms/azure/chat.json")

    # # Configure database
    # database_username = os.getenv("SQL_SERVER_USERNAME")
    # database_password = os.getenv("SQL_SERVER_PASSWORD")
    # database_server = os.getenv("SQL_SERVER_NAME")
    # database_db = os.getenv("SQL_SERVER_DATABASE_NAME")

    # # Create connection string
    # connection_string = (
    #     f"mssql+pyodbc://{database_username}:{database_password}@"
    #     f"{database_server}.database.windows.net:1433/"
    #     f"{database_db}?driver=ODBC+Driver+18+for+SQL+Server"
    # )

    # # Connect to the database
    # db = SQLDatabase.from_uri(connection_string, schema="SalesLT")


#     # Use sql database toolkit
#     toolkit = SQLDatabaseToolkit(db=db, llm=llm, reduce_k_below_max_tokens=True)

#     # Create the sql agent
#     agent_executor = create_sql_agent(
#         llm=llm,
#         toolkit=toolkit,
#         verbose=True,
#         agent_executor_kwargs={
#             "system_message": SystemMessage(
#                 content="You are an expert MS SQL data query writer.  You only write valid MS SQL queries."
#             )
#         },
#     )

#     try:
#         result = agent_executor.run(
#             "Show me all customers who have spent more than $1000."
#         )
#         return result
#     except Exception as e:
#         return e


# if __name__ == "__main__":
#     result = main()
#     print(result)
