# Use Python 3.9 image as the base
FROM python:3.13.0

# Set the working directory inside the container
WORKDIR /app

# Copy all files from the current directory to the container
COPY . /app

RUN apt-get update && \
    apt-get install -y poppler-utils && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies from requirements.txt
RUN pip install -r requirements.txt

# Expose ports for the application (HTTP and HTTPS)
EXPOSE 80
EXPOSE 443

# Command to run the application
CMD ["python", "app.py"]
