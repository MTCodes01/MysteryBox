FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements_utf8.txt .
RUN pip install --no-cache-dir -r requirements_utf8.txt

# Copy the application code
COPY . .

# Expose port 80 for web traffic
EXPOSE 80

# Command to run the application binding to all interfaces on port 80
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
