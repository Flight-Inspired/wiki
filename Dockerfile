# Use the official Python image as the base image
FROM python:3.9

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy the Django application code to the container
COPY . /app/

# Copy the requirements file and install dependencies
RUN pip install -r requirements.txt

ENTRYPOINT [ "gunicorn", "core.wsgi" ]
