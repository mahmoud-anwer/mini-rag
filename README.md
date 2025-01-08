# mini-rag
This is a minimal implementation of the RAG model for question answering.

## Requirements
- Python 3.9

## Installation

### Create virtual environment for the application
```
virtualenv mini-rag
source mini-rag/bin/activate
```

### Setup the environment variables
```
cp .env.example .env
```
- Open `.env` file, and set the required environment variables.

### Install the required packages
```
pip install -r requirements.txt
```

### Run the FASTAPI server
```
uvicorn main:app --reload --host 0.0.0.0 --port 5000
```

## Setting up Docker
- Install `Docker` and `Docker Compose` on your local machine, and then execute the following commands from the repository root directory:
```
cd docker
cp .env.example .env
```
- Open `.env` file, and set the required environment variables.
- Execute the following command to get your containers up and running:
```
docker compose up -d
```

## Structure
- Entry point
    - Purpose: The entry point of the application.
    - File: `src/main.py`
- Assets
    - Purpose: Storing the application assets.
    - Directory: `src/assets`
- Controllers
    - Purpose: Handling the main functions of the application.
    - Directory: `src/controllers`
- Configuration
    - Purpose: Handling the application configuration.
    - Directory: `src/helpers`
    - Environment variables: `src/.env` file
    - Method: `pydantic_settings`
- Models
    - Purpose: Handling the data models like database schemes and enumerations.
    - Directory: `src/models`
- Routes
    - Purpose: Handling the different routes of the application such as upload, process and nlp routes.
    - Directory: `src/routes`
- Database operations
    - Purpose: Handling the implementation of database logic such as creating or deleteing data chunks.
    - Directory: `src/services`
- LLM operations
    - Purpose:
        - Creating `interface` for different LLM providers such as `OpenAi` and `Cohere` implementing setting the generation and embedding models, and other required methods.
        - Creating `interface` for Vector databases such as `Qdrant` implementing the different database operations.
    - Directory: `src/stores`
- Logging
    - Purpose: Handling the logging implementation across the application.
    - Directory: `src/utils`
- Dependencies
    - Purpose: Containing the packages required by the application.
    - Directory: `src/requirements.txt`
- Dockering the application
    - Purpose: Handling creating a `Dockerfile` for the application.
    - File: `src/Dockerfile`
- Docker Compose
    - Purpose: Handling create a `Docker Compose` file for the applicaion including the API, MongoDB, MongoExpress and Qdrant.
    - Directory: `docker`
- CI/CD pipeline
    - Purpose: Handling creating a CI/CD pipeline for the application.
    - Directory: `src/Jenkinsfile`
- VScode extensions
    - Purpose: Recommending using `pylint` extension.
    - Directory: `.vscode/extensions.json`
- VScode settings
    - Purpose: Handling adding some `pylint` and `vscode` settings.
    - Directory: `.vscode/settings.json`

## API endpoints
- Base
    - Purpose: Act as an informative endpoint that retrieves some information about the API.
    - route: `/api/v1`
- Upload file
    - Purpose: Upload a new file in a specific project, and retrieves the file ID.
    - route: `/api/v1/data/upload/{project_id}`
- Process one file
    - Purpose: Process a file in a specific project using its ID, and retrieves the number of inserted chunks.
    - route: `/api/v1/data/process/{project_id}`
- Process all files
    - Purpose: Process all files in a specific project, and retrieves the number of inserted chunks, and the number of processed files.
    - route: `/api/v1/data/processall/{project_id}`
- Insert chunks into Vector DB
    - Purpose: Insert the created chunks from a specific project into the Vector DB `Qdrant`, and retrieves the number of inserted items.
    - route: `/api/v1/nlp/index/push/{project_id}`
- Get the index information for a specific project
    - Purpose: retrieve the index information for a specific project from the Vector DB `Qdrant`.
    - route: `/api/v1/nlp/index/info/{project_id}`
- Search into the Vector DB
    - Purpose: Perform a semantic search in the vector DB `Qdrant` for a specific project, and retrieves the results with its score.
    - route: `/api/v1/nlp/index/search/{project_id}`
- Answers a question using the RAG approach
    - Purpose: Retrieves relevant documents for a specific project from the vector DB `Qdrant` collection and uses
        a language model to generate an answer based on the retrieved documents.
    - route: `/api/v1/nlp/index/answer/{project_id}`

## pre-commit checks using `TruffleHog`
- To scan for exposed sensitive data in each new commit.
- First, make sure that `Docker` servcice is up and running.
- After clonning the repository, run the following commands within your virtual environment and inside the root directory.
```
pip install pre-commit
pre-commit install
```
- To exclude any files or directories, add them to `exclude.txt` file.
- To test the configuration locally:
```
pre-commit run --all-files
```

## CI/CD Pipeline
This is a simple pipeline for linting, analysis using `SonarQube` and deploying the new source code.
- GitHub actions
    - Linting using `pylint`.
- Jenkinsfile-SQ `SonarQube`
    - SonarQube analysis.
- Jenkinsfile
    - Building the Docker image.
    - Deploying the new Docker image.

## Enhancements
- Add a CI/CD pipeline including static analysis.
- Refactoring the source code.
- Use MinIO for uploads (I think it would be better to use `NFS`).
- Use UUID to generate a unique file id.
- Use Qdrant container instead of using a regular directory.

## References
- [Mini-RAG - From notebooks to the production | Abu Bakr Soliman](https://www.youtube.com/playlist?list=PLvLvlVqNQGHCUR2p0b8a0QpVjDUg50wQj)
