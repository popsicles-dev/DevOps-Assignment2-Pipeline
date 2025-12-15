pipeline {
    agent any
    
    environment {
        BASE_URL = 'http://16.171.224.162'
        TEST_REPO_URL = 'https://github.com/popsicles-dev/DevOps-Selenium-Tests.git' 
        TEST_REPO_DIR = 'test-repo'
        TEST_FOLDER = 'java-tests'
        TEST_IMAGE_TAG = 'selenium-tests:latest'
        GIT_COMMITTER_EMAIL = '' 
        GIT_COMMITTER = ''
        GIT_COMMIT_MSG = ''
    }

    stages {
        stage('Cleanup Old Containers') {
            steps {
                echo "--- Cleaning up old containers and images ---"
                sh """
                    docker compose down --remove-orphans 2>/dev/null || true
                    docker rm -f mysql_db_container_part2 flask_web_container_part2 2>/dev/null || true
                """
            }
        }
        
        stage('Checkout Application Code') {
            steps {
                echo "--- Checkout Application Code ---"
                checkout scm
                
                script {
                    env.GIT_COMMIT_MSG = sh(script: 'git log -1 --pretty=%B', returnStdout: true).trim()
                    env.GIT_COMMITTER = sh(script: 'git log -1 --pretty=%an', returnStdout: true).trim()
                    env.GIT_COMMITTER_EMAIL = sh(script: 'git log -1 --pretty=%ae', returnStdout: true).trim()
                    
                    echo "Commit: ${env.GIT_COMMIT_MSG}"
                    echo "Author: ${env.GIT_COMMITTER}"
                    echo "Email: ${env.GIT_COMMITTER_EMAIL}"
                }
            }
        }
        
        stage('Checkout Test Code') {
            steps {
                echo "--- Checkout Test Code ---"
                dir(TEST_REPO_DIR) {
                    git branch: 'main', url: "${TEST_REPO_URL}"
                }
            }
        }
        
        stage('Build and Deploy App') {
            steps {
                echo "--- Building Flask App ---"
                sh 'docker compose up -d --build'
                sh 'sleep 30'
            }
        }
        
        stage('Build Test Image') {
            steps {
                echo "--- Building Test Docker Image with Chrome ---"
                dir(TEST_REPO_DIR) {
                    sh "docker build -t ${TEST_IMAGE_TAG} -f Dockerfile.tests-java ."
                }
            }
        }
        
        stage('Run Tests') {
            steps {
                echo "--- Running Maven Tests in Container with Chrome ---"
                sh """
                    docker run --rm \
                    --network host \
                    --shm-size=2g \
                    -e BASE_URL=${BASE_URL} \
                    -v "\$(pwd)/${TEST_REPO_DIR}/${TEST_FOLDER}":/app \
                    ${TEST_IMAGE_TAG} \
                    /bin/bash -c "mvn clean test"
                """
            }
            post {
                always {
                    junit allowEmptyResults: true, testResults: "${TEST_REPO_DIR}/${TEST_FOLDER}/target/surefire-reports/*.xml"
                }
            }
        }
        
        stage('Cleanup') {
            steps {
                echo "--- Final Cleanup ---"
                sh 'docker compose down --rmi all'
                sh "docker rmi ${TEST_IMAGE_TAG} 2>/dev/null || true"
            }
        }
    }
    
    post {
        always {
            echo "Pipeline finished. Sending email notification."
            
            script {
                def committerEmail = env.GIT_COMMITTER_EMAIL ?: ''
                def recipientEmail = 'qasimalik@gmail.com'
                
                // Add committer email if valid and different from grading email
                if (committerEmail && committerEmail.contains('@') && committerEmail != 'qasimalik@gmail.com') {
                    recipientEmail = "${committerEmail},qasimalik@gmail.com"
                }
                
                def testStatus = currentBuild.result ?: 'SUCCESS'
                
                try {
                    echo "Sending email to: ${recipientEmail}"
                    
                    mail to: recipientEmail,
                         subject: "Jenkins Build ${testStatus}: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                         body: """
Build Status: ${testStatus}

Job: ${env.JOB_NAME}
Build Number: #${env.BUILD_NUMBER}
Commit: ${env.GIT_COMMIT_MSG}
Author: ${env.GIT_COMMITTER}
Committer Email: ${committerEmail}

View Build: ${env.BUILD_URL}
Test Report: ${env.BUILD_URL}testReport/

---
Automated notification from Jenkins CI/CD Pipeline
                         """
                    
                    echo "✓ Email sent successfully to: ${recipientEmail}"
                } catch (Exception e) {
                    echo "✗ Failed to send email: ${e.getMessage()}"
                    echo "Please verify:"
                    echo "1. Jenkins SMTP configuration (Manage Jenkins → System → E-mail Notification)"
                    echo "2. EC2 Security Group allows outbound port 587"
                    echo "3. Gmail App Password is correct"
                }
            }
        }
        success {
            echo '✓ All tests passed! Pipeline completed successfully.'
        }
        failure {
            echo '✗ Tests failed! Check logs above for details.'
        }
    }
}
