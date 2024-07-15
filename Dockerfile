FROM python:3.9.19-slim
WORKDIR /app
COPY ./src/requirements.txt .
RUN pip install -r requirements.txt
COPY ./src .
RUN useradd app
RUN chown -R app:app /app
USER app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]
