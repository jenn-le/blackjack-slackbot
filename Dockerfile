FROM python:3

RUN mkdir -p /usr/casinobot/src
WORKDIR /usr/casinobot/

COPY . /usr/casinobot

RUN pip install -r requirements.txt
RUN python set_slack_info.py

CMD ["python", "./src/casinobot.py"]
