# Natural Language SQL Queries with Azure OpenAI

## Introduction

This guide walks you through how to use [LangChain](https://www.langchain.com/) with [Azure OpenAI Service](https://learn.microsoft.com/en-us/azure/ai-services/openai/overview) to query your data using natural language.

## Prerequisites

The following are required to follow along with this repository:

- Python 3.6+
- An Azure account with OpenAI enabled
- Terraform 1.3+ (optional)
- Docker (if using the Docker setup)

## Getting Started (Standard)

### Setting Up Your Development Environment

Set up a Python virtual environment to isolate your project dependencies. Follow these steps to create and activate a new virtual environment:

```bash
export VIRTUAL_ENV=".venv"
python3 -m venv $VIRTUAL_ENV
source .venv/bin/activate
```

### Installing Required Dependencies

Install essential software, including the Microsoft ODBC driver for SQL Server on macOS.  Without this, installation of `pyodbc` will likely fail.

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
brew tap microsoft/mssql-release https://github.com/Microsoft/homebrew-mssql-release
brew update
HOMEBREW_ACCEPT_EULA=Y brew install msodbcsql18 mssql-tools18
```

For more information, see the Microsoft docs on how to [Install the Microsoft ODBC driver for SQL Server macOS](https://learn.microsoft.com/en-us/sql/connect/odbc/linux-mac/install-microsoft-odbc-driver-sql-server-macos?view=sql-server-ver16).

Next, install your Python dependencies:

```bash
pip install --upgrade pip
python3 -m pip install --upgrade setuptools
pip install -r requirements.txt
```

You can find all required dependencies in the `requirements.txt` file at the root of this project.

### Setting OpenAI Environment Variables

Set up environment variables for both OpenAI and Azure OpenAI services:

```bash
export OPENAI_API_TYPE=azure
export OPENAI_API_VERSION=2023-07-01-preview
export OPENAI_API_BASE=https://your-resource-name.openai.azure.com
export OPENAI_API_KEY="..."
```

Be sure to exclude the trailing `/` from the `OPENAI_API_BASE` if you copy it from the Azure portal.

Next, set your database connection details as environment variables:

```bash
export SQL_SERVER_NAME="sample-server-12345678"
export SQL_SERVER_DATABASE_NAME="sample-database"
export SQL_SERVER_USERNAME="4dm1n157r470r"
export SQL_SERVER_PASSWORD="4-v3ry-53cr37-p455w0rd"
```

You can make these values anything you want them to be provided they meet character, uniqueness, and complexity requirements.

### Creating Infrastructure as Code with Terraform (Optional)

Automate the creation of your Azure SQL Server and database using Terraform. This is an optional but recommended step, as the example Python script relies on data in this database.

First, log into Azure:

```bash
az login
```

Next, set the Terraform inputs as environment variables using the ones previously defined:

```bash
export TF_VAR_sql_server_name=$SQL_SERVER_NAME
export TF_VAR_sql_server_database_name=$SQL_SERVER_DATABASE_NAME
export TF_VAR_sql_server_username=$SQL_SERVER_USERNAME
export TF_VAR_sql_server_password=$SQL_SERVER_PASSWORD
```

Finally, run Terraform:

```bash
terraform init
terraform plan -out out.tfplan
terraform apply out.tfplan
```

If you don't have Terraform installed, it is recommended to do so with [tfenv](https://github.com/tfutils/tfenv).

### Running the Python Script

Run the example script to see Langchain and Azure OpenAI in action:

```bash
python run.py
```

## Getting Started (Docker)

If you are using a newer MacBook with an M1 or M2 chip, you will likely have issues getting `pyodbc` or `pymssql` to install with Python due to some system architecture issues.  To resolve this, there is a Dockerfile you can use.

### Creating a .env file

Create a `.env` file at the root.  This file is included in the `.gitignore` file and will not be committed to your repository.  The values in this file will be used during execution with Docker.

```bash
SQL_SERVER_NAME=...
SQL_SERVER_DATABASE_NAME=...
SQL_SERVER_USERNAME=...
SQL_SERVER_PASSWORD=...

OPENAI_API_TYPE=...
OPENAI_API_VERSION=...
OPENAI_API_BASE=...
OPENAI_API_KEY=...
```

### Building the Docker image

You now need to build the Docker image so you can use it to run the Python scripts.

```bash
docker build -t azure-openai-langchain .
```

### Running Docker

Now you can run Docker using the built image and passing the environment variables set above.

```bash
docker run --env-file .env -it azure-openai-langchain /bin/bash
```

### Running the Python Script

Run the example script to see Langchain and Azure OpenAI in action:

```bash
python3 run.py
```

## Testing other prompts

Here are some prompts you can try using the AdventureWorks dataset (if deployed your SQL database with Terraform).

### Product data

- What are the top-selling products?
- What is the most expensive product?
- Show me all products in the 'Bike' category.
- What are the products with a discount?

### Order data

- Show me all orders placed by Customer Keith Harris.
- What is the name of the customer has placed the most orders?
- How many pending orders are there?

### Customer data

- What are the names of the top 5 customers by revenue?
- What is the average age of our customers?
- Show me all customers who have spent more than $1000.

## Additional References

For more information about how this was set up, you can review the:

- [Azure OpenAI LangChain Documentation](https://python.langchain.com/docs/integrations/llms/azure_openai)

Tip: If you are having trouble knowing what attributes or methods are available for a given class, you can inspect them in the script by holding down the command (`⌘`) key and selecting the class, method, or attribute.
