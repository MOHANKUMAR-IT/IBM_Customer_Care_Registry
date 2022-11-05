FROM python:3.10.7


WORKDIR /usr/src/app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

RUN Scripts/activate
CMD [ "python3", "app.py"]

