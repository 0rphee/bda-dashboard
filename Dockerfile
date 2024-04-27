# Use official Python 3.11 image as base
FROM python:3.11-alpine

# Install necessary packages
RUN apk update && \
    apk add --no-cache nodejs npm

# Set working directory in the container
WORKDIR /app

# Copy requirements.txt to the container
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy Node.js dependencies
COPY proy-bda-frontend/package-lock.json .
COPY proy-bda-frontend/package.json .

# Navigate to the frontend directory and install npm dependencies
WORKDIR /app/proy-bda-frontend
RUN npm install

# Copy the rest of the application code to the container
COPY ./proy-bda-frontend .

# Build the frontend
RUN npm run build

# Go back to the app directory
WORKDIR /app

# Copy the rest of the application code
COPY . .

EXPOSE 8000

# Set Flask environment variables
ENV FLASK_RUN_PORT=8000 FLASK_RUN_HOST=0.0.0.0

# Command to run the application
CMD ["flask", "run", "--debug"]
