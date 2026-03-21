pipeline {
    agent any

    triggers {
        pollSCM('H/5 * * * *')
        cron('H 0 * * *')
    }

    environment {
        PROJECT_NAME = 'Student-Feedback-Form'
        REPORT_DIR   = 'test-reports'
        VENV_DIR     = 'venv'
    }

    options {
        timeout(time: 20, unit: 'MINUTES')
        buildDiscarder(logRotator(numToKeepStr: '10'))
        timestamps()
    }

    stages {

        // ─────────────── Checkout ───────────────
        stage('Checkout') {
            steps {
                echo 'Checking out source code...'
                checkout scm
                bat 'echo Workspace: %WORKSPACE%'
                bat 'dir'
            }
        }

        // ─────────────── Setup Environment ───────────────
        stage('Setup Environment') {
            steps {
                echo 'Setting up Python environment...'
                bat '''
                python -m venv venv

                call venv\\Scripts\\activate

                python -m pip install --upgrade pip

                pip install selenium webdriver-manager pytest pytest-html
                '''
            }
        }

        // ─────────────── Lint ───────────────
        stage('Lint') {
            steps {
                echo 'Checking syntax...'
                bat '''
                call venv\\Scripts\\activate

                python -m py_compile test_feedback_form.py
                '''
            }
        }

        // ─────────────── Run Tests ───────────────
        stage('Run Selenium Tests') {
            steps {
                echo 'Running Selenium tests...'
                bat '''
                if not exist test-reports mkdir test-reports

                call venv\\Scripts\\activate

                python -m pytest test_feedback_form.py ^
                --verbose ^
                --tb=short ^
                --html=test-reports/test-report.html ^
                --self-contained-html ^
                --junitxml=test-reports/junit-results.xml
                '''
            }
        }

        // ─────────────── Publish Results ───────────────
        stage('Publish Results') {
            steps {
                echo 'Publishing results...'
            }
            post {
                always {
                    junit testResults: "test-reports/junit-results.xml",
                          allowEmptyResults: true

                    archiveArtifacts artifacts: "test-reports/**",
                                     allowEmptyArchive: true

                    publishHTML(target: [
                        allowMissing: false,
                        alwaysLinkToLastBuild: true,
                        keepAll: true,
                        reportDir: "test-reports",
                        reportFiles: 'test-report.html',
                        reportName: 'Selenium Test Report'
                    ])
                }
            }
        }
    }

    // ─────────────── Post Build ───────────────
    post {
        success {
            echo 'BUILD SUCCESS: All tests passed'
        }
        failure {
            echo 'BUILD FAILED: Check console output'
        }
        always {
            echo "Build finished: ${currentBuild.result}"
            cleanWs()
        }
    }
}