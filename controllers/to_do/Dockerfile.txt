# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /usr/src/app

# Copy the requirements.txt file to the working directory
COPY requirements.txt .

# Install any dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to the container
COPY . .

# Expose port 5000 to the outside world (Flask default port)
EXPOSE 5000

# Command to run the application
CMD ["python", "app.py"]
