# Use a base image with Python and dependencies installed
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create a directory for data
RUN mkdir data

# Copy the Python script and other necessary files
COPY test_bot.py ./
COPY conversation_history.db ./data/

# Expose port (if your bot listens on a specific port)
EXPOSE 8080

# Mount a volume for persistent storage of the SQLite database file
VOLUME /app/data

# Run the Python script when the container starts
CMD ["python", "test_bot.py"]
