@Library("myLibrary") _

pipeline {
    agent any

    // Disable automatic SCM checkout
    // options {
    //     skipDefaultCheckout()
    // }

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
        stage('Cleanup the workspace') {
            steps {
                script{
                    echo "Cleanup the workspace..."
                    // cleanWs()
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
                    def scannerHome = tool 'SonarQube Scanner'
                    withSonarQubeEnv('SonarQube') {
                        sh "${scannerHome}/bin/sonar-scanner"
                    }
                }
            }
        }

        stage('Building Docker image') {
            steps {
                script{
                     echo "Building..."
                    sh """
                        docker build -t anwer95/${DOCKER_REPO_NAME}:${env.BUILD_ID} ./${TARGET_DIRECTORY}
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
                        docker push ${DOCKERHUB_USERNAME}/${DOCKER_REPO_NAME}:${env.BUILD_ID}
                    """
                }
            }
        }
        
    }
}
