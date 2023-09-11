# Use an official Python runtime as a parent image
FROM ubuntu:latest

# Set environment variables to non-interactive (this prevents some prompts)
ENV DEBIAN_FRONTEND=non-interactive

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app/

# Update package list and install essentials
RUN apt-get update -y && \
    apt-get install -y unzip wget vim curl lsb-release apt-transport-https python3-pip

# Install Python
RUN pip3 install --upgrade pip && \
    python3 -V && \
    pip --version

# Copy the requirements.txt into the container at /app
COPY requirements.txt /app

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Install Terraform
RUN wget https://releases.hashicorp.com/terraform/1.4.6/terraform_1.4.6_linux_amd64.zip && \
    unzip -o terraform_1.4.6_linux_amd64.zip && \
    mv terraform /usr/local/bin/ && \
    terraform --version

# Install Azure CLI
RUN curl -sL https://aka.ms/InstallAzureCLIDeb | bash && \
    az --version

# Install Microsoft ODBC driver for SQL Server
RUN curl -fsSL https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
    curl -fsSL https://packages.microsoft.com/config/ubuntu/20.04/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && \
    ACCEPT_EULA=Y apt-get install -y msodbcsql18 && \
    ACCEPT_EULA=Y apt-get install -y mssql-tools18 && \
    apt-get install -y unixodbc-dev

# Set environment variables for Microsoft ODBC driver for SQL Server
ENV PATH "$PATH:/opt/mssql-tools18/bin"

# Make port 80 available to the world outside this container
EXPOSE 80
