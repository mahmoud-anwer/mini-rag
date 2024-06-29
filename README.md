# mini-rag
This is a minimal implementation of the RAG model for question answering.

## Requirements
- Python 3.8 or later

## Installation

### Create virtual environment for the application
```bash
$ virtualenv mini-rag
$ source mini-rag/bin/activate
```

### Install the required packages

```bash
$ pip install -r requirements.txt
```

### Setup the environment variables

```bash
$ cp .env.example .env
```

Set your environment variables in the .env file like OPENAI_API_KEY value.

### Run the FASTAPI server

```bash
uvicorn main:app
uvicorn main:app --reload
uvicorn main:app --reload --host 0.0.0.0 --port 5000
```
