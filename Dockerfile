# Use the official Python base image with Python 3.10
FROM python:3.10

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file and install the dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the entire web service code to the container
COPY . .

# Expose the port on which the web service will run (change the port if necessary)
EXPOSE 8000

# Run the command to start the web service
CMD [ "python", "app.py" ]
