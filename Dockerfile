FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

# Install ffmpeg
RUN apt-get update && apt-get install -y ffmpeg

# Run server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

#coy code to container
COPY . /code/