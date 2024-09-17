FROM python:slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

CMD ["gunicorn", "-b", "0.0.0.0:5000", "bot:bot", "--timeout", "200", "--worker-class", "gevent"]
