FROM python:slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir python-telegram-bot requests

CMD ["python", "bot.py"]
