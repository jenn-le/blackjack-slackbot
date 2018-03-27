FROM python:3

RUN mkdir -p /usr/casinobot/src
WORKDIR /usr/casinobot/

COPY . /usr/casinobot

RUN pip install -r requirements.txt

CMD ["python", "./src/casinobot.py"]
