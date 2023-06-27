# Use the official Python base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the Python script to the container
COPY main.py .

# Set the entry point command for the container
ENTRYPOINT ["python", "main.py"]

# Default command for the container (empty in this case)
CMD []
