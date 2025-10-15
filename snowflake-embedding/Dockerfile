FROM python:3.11-slim

# Install build tools and other utilities
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    wget \
    git

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .
# Install any necessary packages specified in requirements.txt
RUN pip install -r requirements.txt

RUN python download_model.py

# Make port 8001 available to the world outside this container
EXPOSE 8080


# Run app.py when the container launches
CMD ["python", "app.py"]