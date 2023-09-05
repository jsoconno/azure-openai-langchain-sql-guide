# learn-langchain

## setup

### create a virtual environment

```bash
export VIRTUAL_ENV=".venv"
python3 -m venv $VIRTUAL_ENV
source .venv/bin/activate
```

### install dependencies

```bash
pip install --upgrade pip
python3 -m pip install --upgrade setuptools
pip install -r requirements.txt
```

### set environment variables

#### openai api

```bash
export OPENAI_API_KEY="..."
```

#### azure openai api

```bash
export OPENAI_API_TYPE=azure
export OPENAI_API_VERSION=2023-05-15
export OPENAI_API_BASE=https://your-resource-name.openai.azure.com
export OPENAI_API_KEY="..."
```

### setup python script

#### openai api

```python
from langchain.llms import OpenAI

llm = OpenAI()

llm.predict('Say "hi!".)
```

#### azure openai api

```python
from langchain.llms import AzureOpenAI

# Create an instance of Azure OpenAI
# Replace the deployment name with your own
llm = AzureOpenAI(
    deployment_name="td2",
    model_name="text-davinci-002",
)

llm('Say "hi!".')
```

## create sample data with terraform (optional)

### authenticate to azure

```bash
az login
```

### create the infrastructure

This will create a new instance of Azure SQL Server and a database pre-loaded with sample data.

```bash
export TF_VAR_sql_server_name="sample-server-12345678"
export TF_VAR_sql_server_database_name="sample-database"
export TF_VAR_sql_server_username="4dm1n157r470r"
export TF_VAR_sql_server_password="4-v3ry-53cr37-p455w0rd"
```

```bash
terraform init
terraform plan -out out.tfplan
terraform apply out.tfplan
```

### query and return natural lanugage responses from the database

```python
python example.py
```
