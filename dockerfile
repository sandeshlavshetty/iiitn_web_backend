# Use an official lightweight Python image
FROM python:3.11

# Set the working directory
WORKDIR /app

# Install system dependencies (including Graphviz for pygraphviz)
RUN apt-get update && apt-get install -y \
    graphviz \
    graphviz-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy project files into container
COPY . .

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose port for Flask
EXPOSE 5000

# Run the application with Gunicorn
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
