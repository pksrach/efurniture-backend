# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Copy .env file into the container
COPY .env .

# Copy Alembic configuration files into the container
COPY alembic.ini .
COPY alembic alembic

# Copy the Alembic runner script into the container
COPY run_alembic.sh .

# Make the script executable
RUN chmod +x run_alembic.sh

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Set the ENTRYPOINT to run the Alembic migrations
#ENTRYPOINT ["./run_alembic.sh"]

# Run the FastAPI server
CMD ["uvicorn", "app.main:app", "--port", "8000", "--reload"]