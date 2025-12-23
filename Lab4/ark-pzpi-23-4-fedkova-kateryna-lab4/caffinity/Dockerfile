# Use an official Python runtime as a parent image
FROM python:3.11.4-slim-buster

# Set the working directory in the container to /app
WORKDIR /usr/src/app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . .

CMD ["gunicorn", "caffinity.wsgi:application", "--bind", "0.0.0.0:10000"]