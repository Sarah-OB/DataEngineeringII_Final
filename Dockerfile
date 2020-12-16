FROM python:3.6

WORKDIR /app

ENV TWEETS_ANALYZER_APP=app.py

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
