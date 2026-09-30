pipeline {

    agent any

    environment {
        IMAGE_NAME = "customer-portal"
        CONTAINER_NAME = "customer-portal-${BUILD_NUMBER}"
    }

    stages {

        stage('Checkout') {
            steps {
                echo 'Checking out source code from Git...'

                git(
                    credentialsId: 'github-credentials',
                    url: 'https://github.com/YOUR_USERNAME/customer-portal.git',
                    branch: 'main'
                )
            }
        }

        stage('Build') {
            steps {
                echo 'Building application...'

                bat '''
                    python -m pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Test') {
            steps {
                echo 'Running automated tests...'

                bat '''
                    pytest -v
                '''
            }
        }

        stage('Docker Build') {
            steps {
                echo 'Building Docker image...'

                bat '''
                    docker build -t %IMAGE_NAME%:build-%BUILD_NUMBER% .
                '''
            }
        }

        stage('Container Verification') {
            steps {
                echo 'Starting temporary Docker container...'

                bat '''
                    docker run -d --name %CONTAINER_NAME% -p 8080:5000 %IMAGE_NAME%:build-%BUILD_NUMBER%
                '''

                bat '''
                    timeout /t 5 /nobreak

                    curl --fail http://localhost:8080/health
                '''
            }
        }

        stage('Cleanup') {
            steps {
                echo 'Stopping and removing temporary container...'

                bat '''
                    docker stop %CONTAINER_NAME% || exit /b 0
                    docker rm %CONTAINER_NAME% || exit /b 0
                '''
            }
        }
    }

    post {

        always {
            echo 'Pipeline completed.'
        }

        failure {
            echo 'Pipeline failed.'
        }

        success {
            echo 'Pipeline completed successfully.'
            echo "Docker image: customer-portal:build-${BUILD_NUMBER}"
        }
    }
}