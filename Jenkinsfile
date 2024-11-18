@Library("myLibrary") _

pipeline {
    agent any

    // Disable automatic SCM checkout
    options {
        skipDefaultCheckout()
    }

    environment {
        CREDENTIALS_ID = "mahmoudanwer_github_token"
        GITHUB_USERNAME = "mahmoud-anwer"
        REPO_OWNER = "mahmoud-anwer"
        REPO_NAME = "mini-rag"
        TARGET_DIRECTORY = "mini-rag"
        BASE_BRANCH = "main"
    }
    
    stages {
        stage('Cleanup the workspace') {
            steps {
                script{
                    echo "Cleanup the workspace..."
                    cleanWs()
                }
            }
        }

        stage('Cloning the Repository') {
            steps {
                script {
                    echo "Cloning..."
                    def cloneRepo_params = [
                        github_username: env.GITHUB_USERNAME,
                        credentials_id: env.CREDENTIALS_ID,
                        repo_owner: env.REPO_OWNER,
                        repo_name: env.REPO_NAME,
                        target_dir: env.TARGET_DIRECTORY
                    ]
                    cloneRepo(cloneRepo_params)
                }
            }
        }

        stage('SonarQube Analysis') {
            steps {
                script {
                    echo "SonarQube Analysis..."
                    def scannerHome = tool 'SonarQube'
                    withSonarQubeEnv('SonarQube') {
                        sh """
                            ${scannerHome}/bin/sonar-scanner \
                            -Dsonar.projectKey=mini-rag-main \
                            -Dsonar.projectName='mini-rag' \
                            -Dsonar.projectBaseDir=${TARGET_DIRECTORY} \
                            -Dsonar.python.version=3.9 \
                            -Dsonar.scm.provider=git
                        """
                    }
                }
            }
        }

        stage('Building Docker image') {
            steps {
                script{
                     echo "Buld Docker image..."
                    sh """
                        ssh ubuntu@10.0.0.154 "cd /home/ubuntu/mini-rag/docker &&\
                        docker-compose build api"
                    """
                }
            }
        }

        stage('Deploy the new Docker image') {
            steps {
                script {
                    echo "Deploy Docker image..."
                    sh """
                        ssh ubuntu@10.0.0.154 "cd /home/ubuntu/mini-rag/docker &&\
                        docker-compose up -d api"
                    """
                }
            }
        }

        stage('Update Docker image tag and redeploy') {
            steps {
                script {
                    echo "Update Docker image tag..."
                    sh """
                        ssh ubuntu@10.0.0.154 "cd /home/ubuntu/mini-rag/docker &&\
                        sed -i "s/IMAGE_TAG=.*/IMAGE_TAG=${BUILD_NUMBER}/" .env && \
                        docker-compose up -d api"
                    """
                }
            }
        }
        
    }
}
