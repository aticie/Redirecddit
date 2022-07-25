FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt /app

RUN pip install -r requirements.txt

COPY main.py /app

ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "3000"]
