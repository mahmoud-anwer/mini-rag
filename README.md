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

## Structure
- Configuration
    - Directory: `helpers`
    - Method: `pydantic_settings`

- routes

    - `base` route: `/api/v1`
    - `data` route: `/api/v1/data/upload/{project_id}`


## Pipeline stages
- Scanning the source code by `pylint`
- Scanning the source code for secrets using `truffleHog`
- Building Docker image
- DockerHub login
- Pushing Docker image


## Setting up Docker
- Install Docker and Docker Compose on your local machine, and then execute the following commands from the repository root directory:
```bash
cd docker
cp .env.example .env
```
- Open `.env` file, and set the required variables.
- Get your containers up by executing the following command:
```bash
docker compose up -d
```

### TODO:
- add a container in the docker compose file for the application itself.