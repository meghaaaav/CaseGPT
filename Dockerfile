# Use an official Python runtime as a parent image
# Choose a version compatible with your project dependencies
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
# Copying requirements first leverages Docker's build cache
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
# --no-cache-dir keeps the image size down
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Make port 8501 available to the world outside this container
# Streamlit's default port is 8501
EXPOSE 8501

# Define the command to run the app when the container launches
# Replace 'your_app_script.py' with the actual filename of your Streamlit app script
CMD ["streamlit", "run", "app.py"]
