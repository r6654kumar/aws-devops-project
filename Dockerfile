# Use official Python image as base
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the application code
COPY app.py /app

# Install required Python packages
RUN pip install boto3 pymysql

# Command to run the application
CMD ["python", "app.py"]

