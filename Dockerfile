FROM ubuntu

RUN apt-get update && apt-get install -y python3 python3-pip
RUN pip install flask==2.1

COPY .

ENV FLASK_APP=app

EXPOSE 5000

