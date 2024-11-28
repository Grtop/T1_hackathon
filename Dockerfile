# Use an official Python runtime as a parent image
FROM python:3.10-slim
RUN pip install --upgrade pip

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable
# Create necessary directories
RUN mkdir -p /app/good_files /app/uploads

# Run the FastAPI application using uvicorn
# Copy and set permissions for start script
COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh

# Run start script
CMD ["/app/start.sh"]