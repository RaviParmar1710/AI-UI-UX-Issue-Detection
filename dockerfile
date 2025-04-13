# Use official Python image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy all files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port for Fly
EXPOSE 8080

# Start the app using Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app"]
