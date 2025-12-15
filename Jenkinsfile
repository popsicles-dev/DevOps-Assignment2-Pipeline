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
        stage('Cleanup Old Test Containers') {
            steps {
                echo "--- Cleaning up old test containers only ---"
                sh """
                    docker rm -f selenium-test-container 2>/dev/null || true
                    docker rmi ${TEST_IMAGE_TAG} 2>/dev/null || true
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
                echo "--- Building and Deploying Flask App ---"
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
        
        stage('Cleanup Test Resources') {
            steps {
                echo "--- Cleaning up test image only (keeping app containers running) ---"
                sh "docker rmi ${TEST_IMAGE_TAG} 2>/dev/null || true"
            }
        }
    }
    
    post {
        always {
            echo "Pipeline finished. Application containers are still running."
            echo "Access your app at: ${BASE_URL}"
            
            script {
                def committerEmail = env.GIT_COMMITTER_EMAIL ?: ''
                def testStatus = currentBuild.result ?: 'SUCCESS'
                
                // Only send email if we have a valid committer email
                if (committerEmail && committerEmail.contains('@')) {
                    try {
                        echo "Sending email to committer: ${committerEmail}"
                        
                        mail to: committerEmail,
                             subject: "Jenkins Build ${testStatus}: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                             body: """
Build Status: ${testStatus}

Job: ${env.JOB_NAME}
Build Number: #${env.BUILD_NUMBER}
Commit: ${env.GIT_COMMIT_MSG}
Author: ${env.GIT_COMMITTER}

Application URL: ${BASE_URL}
View Build: ${env.BUILD_URL}
Test Report: ${env.BUILD_URL}testReport/

---
Automated notification from Jenkins CI/CD Pipeline

Note: Your application containers are still running at ${BASE_URL}
                             """
                        
                        echo "✓ Email sent successfully to: ${committerEmail}"
                    } catch (Exception e) {
                        echo "✗ Failed to send email: ${e.getMessage()}"
                    }
                } else {
                    echo "⚠ No valid committer email found. Skipping email notification."
                    echo "Extracted email was: '${committerEmail}'"
                }
            }
        }
        success {
            echo '✓ All tests passed! Application is running.'
        }
        failure {
            echo '✗ Tests failed! Check logs above for details.'
            echo 'Note: Application containers are still running for debugging.'
        }
    }
}
