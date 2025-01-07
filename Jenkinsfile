pipeline {
    agent any

    environment {
        REMOTE_HOST = '10.0.0.154'
        REMOTE_USER = 'ubuntu'
        REMOTE_DIR = '/home/ubuntu/mini-rag'
    }

    parameters {
        string(name: 'BRANCH', defaultValue: 'main', description: 'Branch to deploy')
        string(name: 'SERVICE', defaultValue: 'api', description: 'Service to deploy')
    }

    stages {
        stage('Retrieving the latest changes') {
            steps {
                echo "Retrieving the latest changes..."
                sshagent(['projects-server2']) {
                    sh """
                        ssh ${REMOTE_USER}@${REMOTE_HOST} "cd ${REMOTE_DIR} && \
                        git pull origin ${BRANCH}"
                    """
                }
            }
        }

        stage('Building the Docker image') {
            steps {
                echo "Building the Docker image..."
                sshagent(['projects-server2']) {
                    sh """
                        ssh ${REMOTE_USER}@${REMOTE_HOST} "cd ${REMOTE_DIR}/docker && \
                        docker-compose build ${SERVICE}"
                    """
                }
            }
        }

        stage('Deploying the Docker image') {
            steps {
                echo "Deploying the Docker image..."
                sshagent(['projects-server2']) {
                    sh """
                        ssh ${REMOTE_USER}@${REMOTE_HOST} "cd ${REMOTE_DIR}/docker &&\
                        docker-compose up -d ${SERVICE}"
                    """
                }
            }
        }
    }
}
