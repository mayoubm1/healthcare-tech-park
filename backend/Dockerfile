# Use the official Python image as the base image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8080 available to the world outside this container
EXPOSE 8080

# Run gunicorn to serve the Flask application
# The format is 'module:app_instance_name'
# wsgi.py contains 'app = create_app(...)'
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "wsgi:app"]
