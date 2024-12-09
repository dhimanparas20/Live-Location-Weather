# Use an official Python runtime as a base image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose internal port 5000
EXPOSE  5000

# Run Flask application with Gunicorn, binding to port 5000 internally
# Externally, this can be mapped to port 80
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]