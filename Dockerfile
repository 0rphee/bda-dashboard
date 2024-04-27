# Use official Python 3.11 image as base
FROM python:3.11

RUN apt-get update

# Install Node.js and npm
RUN curl -sL https://deb.nodesource.com/setup_16.x | bash -
RUN apt-get install -y nodejs

# Set working directory in the container
WORKDIR /app

# Copy requirements.txt to the container
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY proy-bda-frontend/package-lock.json .
COPY proy-bda-frontend/package.json .

# Navigate to the frontend directory and run npm build
WORKDIR /app/proy-bda-frontend
RUN npm install


# Copy the rest of the application code to the container
COPY ./proy-bda-frontend .

RUN npm run build

# copy the rest (python related)
COPY . ../.

WORKDIR /app

EXPOSE 8000

ENV FLASK_RUN_PORT=8000 FLASK_RUN_HOST=0.0.0.0

# Command to run the application
CMD [ "flask", "run", "--debug" ]
