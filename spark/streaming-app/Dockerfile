# Use official Apache Spark image as base
FROM apache/spark:3.5.0

# Become root for system-level changes
USER root

# Create airflow user inside container
RUN useradd -ms /bin/bash airflow

# Install Python and pip
RUN apt-get update && apt-get install -y python3-pip && apt-get clean

# Set working directory
WORKDIR /opt/spark-app

# Copy Python files and requirements into container
COPY requirements.txt .
COPY . .

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Switch to airflow user
USER airflow
