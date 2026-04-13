pipeline {
    agent any

    environment {
        DOCKER_HOST = "tcp://localhost:2375"
    }

    stages {

        stage('Build Docker Image') {
            steps {
                bat 'docker build -t feedback-app .'
            }
        }

        stage('Deploy using Docker Compose') {
            steps {
                bat 'docker-compose down'
                bat 'docker-compose up -d'
            }
        }

        stage('Monitor Containers') {
            steps {
                bat 'docker ps'
                bat 'docker stats --no-stream'
            }
        }
    }

    post {
        success {
            echo 'Pipeline SUCCESS ✅'
        }
        failure {
            echo 'Pipeline FAILED ❌'
        }
    }
}
