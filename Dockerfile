# Use a lightweight Python image as the base
FROM python:3.9-slim

# Install system dependencies, including zbar for barcode scanning
RUN apt-get update && apt-get install -y \
    libzbar0 \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy the requirements file to the working directory and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code to the working directory
COPY . .
EXPOSE 8501

# Set environment variables if needed (e.g., for Google Cloud credentials)
# ENV GOOGLE_APPLICATION_CREDENTIALS="/app/credentials.json"

# Run the application (replace `app.py` with your actual script)
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.enableCORS=false"]
