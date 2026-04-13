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

        stage('Run Docker Compose') {
            steps {
                bat 'docker-compose down'
                bat 'docker-compose up -d'
            }
        }

        stage('Verify Deployment') {
            steps {
                bat 'docker ps'
            }
        }
    }

    post {
        success {
            echo 'Pipeline SUCCESS'
        }
        failure {
            echo 'Pipeline FAILED'
        }
    }
}
