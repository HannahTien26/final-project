FROM python:3.9-slim
RUN apt-get update && apt-get install -y chromium chromium-driver
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["gunicorn", "app:app"]