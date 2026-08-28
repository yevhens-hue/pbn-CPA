# Use the official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.9-slim

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True

WORKDIR /app

# Copy local code to the container image.
COPY requirements.txt ./

# Install dependencies.
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install playwright pytest beautifulsoup4
RUN playwright install chromium --with-deps

# Copy the rest of the application
COPY . ./

# Run the web service on container startup. 
# Here we use run.sh or schedule a specific python script like publish_post.py
CMD ["python3", "dashboard.py"]
