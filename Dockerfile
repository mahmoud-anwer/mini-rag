FROM python:3.9-alpine3.20
WORKDIR /app
COPY ./src/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY ./src .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]
