# syntax=docker/dockerfile:1
FROM python:3.11-alpine

WORKDIR /web-app

ADD . /web-app

ENV MONGODB_CONNSTRING="mongodb+srv://root:pass@photobooth.pxudifq.mongodb.net/?retryWrites=true&w=majority"

ENV HOST='0.0.0.0'

ENV PORT=5001

RUN pip install --trusted-host pypi.python.org -r requirements.txt

EXPOSE 80

CMD ["python3", "./app.py"]