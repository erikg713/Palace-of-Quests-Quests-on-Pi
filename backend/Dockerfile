# Flask Dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ENV FLASK_APP=app.py
ENV FLASK_ENV=production

CMD ["flask", "run", "--host=0.0.0.0"]
