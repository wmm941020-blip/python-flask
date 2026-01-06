FROM python:3.13-slim

WORKDIR /app

# Install system dependencies if needed (e.g. for mysqlclient or cryptography)
# RUN apt-get update && apt-get install -y default-libmysqlclient-dev build-essential && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

# Environment variables
ENV FLASK_APP=run.py

# Run the application
CMD ["python", "run.py"]
