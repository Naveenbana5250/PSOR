# Start with a clean Ubuntu image
FROM ubuntu:22.04

# Avoid interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Install Python, pip, UFW, and the PyYAML library
RUN apt-get update && \
    apt-get install -y python3 python3-pip ufw && \
    pip3 install PyYAML

# Set the working directory inside the container
WORKDIR /app

# Copy your project code into the container
COPY . .

# (Remove this line) -> RUN ufw allow ssh && echo "y" | ufw enable

# Define the default command to run when the container starts
CMD ["python3", "engine.py"]
