FROM python:3.12-alpine

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8080

WORKDIR /app

COPY main.py /app/main.py
COPY src /app/src

EXPOSE 8080

CMD ["python", "main.py"]
