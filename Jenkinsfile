@Library("myLibrary") _

pipeline {
    agent any

    environment {
        CREDENTIALS_ID = "mahmoudanwer_github_token"
        GITHUB_USERNAME = "mahmoud-anwer"
        REPO_OWNER = "mahmoud-anwer"
        REPO_NAME = "mini-rag"
        TARGET_DIRECTORY = "mini-rag"
        SERVICE_NAME = "api"
        BASE_BRANCH = "main"
        DOCKERHUB_CREDENTIALS_ID = "mahmoudanwer_dockerhub_token"
        DOCKERHUB_USERNAME = "anwer95"
    }
    stages {
        stage('Cloning repository') {
            steps {
                script {
                    echo "Cloning ..."
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
        stage('Building Docker image') {
            steps {
                script{
                     echo "Editing..."
                    sh '''
                        ls
                        cd ${TARGET_DIRECTORY}
                    '''
                }
            }
        }
        
    }
}
