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
        stage('SonarQube Analysis') {
            steps {
                script {
                    echo "SonarQube Analysis..."
                    def scannerHome = tool 'SonarQube'
                    withSonarQubeEnv('SonarQube') {
                        sh """
                            ${scannerHome}/bin/sonar-scanner \
                            -Dsonar.projectKey=mini-rag-main \
                            -Dsonar.projectName=${TARGET_DIRECTORY} \
                            -Dsonar.python.version=3.9 \
                            -Dsonar.scm.provider=git
                        """
                    }
                }
            }
        }

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
