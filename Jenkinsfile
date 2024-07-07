@Library("myLibrary") _

pipeline {
    agent any

    environment {
        CREDENTIALS_ID = "mahmoudanwer_github_token"
        GITHUB_USERNAME = "mahmoud-anwer"
        REPO_OWNER = "mahmoud-anwer"
        REPO_NAME = "mini-rag"
        TARGET_DIRECTORY = "mini-rag"
        SERVICE_NAME = "mini-rag-api"
        BASE_BRANCH = "main"
        DOCKERHUB_CREDENTIALS_ID = "mahmoudanwer_dockerhub_token"
        DOCKERHUB_USERNAME = "anwer95"
        DOCKER_REPO_NAME = "mini-rag"
    }
    
    stages {
        stage('Scaning the source code') {
            steps {
                script{
                    cleanWs()
                    echo "Scaning the source code for secrets..."
                    sh """
                        . /testENV/bin/activate
                        trufflehog3 --format html --output report.html
                        deactivate
                    """
                }
            }
        }

        stage('Building Docker image') {
            steps {
                script{
                     echo "Building..."
                    sh """
                        docker build -t anwer95/${DOCKER_REPO_NAME}:${env.BUILD_ID} .
                    """
                }
            }
        }

        stage('DockerHub login') {
            steps {
                script {
                    echo "Logging Dockerhub..."
                    def dockerhub_params = [
                        dockerhub_credentials_id: env.DOCKERHUB_CREDENTIALS_ID,
                        dockerhub_username: env.DOCKERHUB_USERNAME
                    ]
                    loginCR.dockerhub(dockerhub_params)
                }
            }
        }

        stage('Pushing Docker image') {
            steps {
                script {
                    echo "Pushing Docker image..."
                    sh """
                        docker push anwer95/${DOCKER_REPO_NAME}:${env.BUILD_ID}
                    """
                }
            }
        }
        
    }
}
