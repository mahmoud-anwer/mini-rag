pipeline {
    agent any

    environment {
        CREDENTIALS_ID = "mahmoudanwer_github_token"
        GITHUB_USERNAME = "mahmoud-anwer"
        REPO_OWNER = "mahmoud-anwer"
        REPO_NAME = "mini-rag"
        TARGET_DIRECTORY = "mini-rag"
        BASE_BRANCH = "main"
    }

    stages {
        stage('Building the Docker image') {
            steps {
                script{
                    echo "Building the Docker image..."
                    sh """
                        ssh ubuntu@10.0.0.154 "cd /home/ubuntu/mini-rag/docker &&\
                        docker-compose build api"
                    """
                }
            }
        }

        stage('Deploying the Docker image') {
            steps {
                script {
                    echo "Deploying the Docker image..."
                    sh """
                        ssh ubuntu@10.0.0.154 "cd /home/ubuntu/mini-rag/docker &&\
                        docker-compose up -d api"
                    """
                }
            }
        }

    }
}
