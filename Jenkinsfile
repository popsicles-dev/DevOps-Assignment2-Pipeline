pipeline {
    // We use agent any to allow sh steps on the Jenkins host
    agent any
    
    environment {
        // Target site for the Selenium tests
        BASE_URL = 'http://16.171.224.162'
        // Repository containing the Java/Maven test code and Dockerfile.tests-java
        TEST_REPO_URL = 'https://github.com/popsicles-dev/DevOps-Selenium-Tests.git' 
        // Local directory name for the test repository checkout
        TEST_REPO_DIR = 'test-repo'
        // Directory inside the test repo containing the Java source/pom.xml
        TEST_FOLDER = 'java-tests'
        // Tag for the custom Docker image built in the pipeline
        TEST_IMAGE_TAG = 'selenium-tests:latest'

        // Placeholder for email extraction (will be overwritten by script block)
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
                    // Extract commit information for email
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
                    // Note: Ensure your TEST_REPO_URL points to the correct GitHub repo
                    git branch: 'main', url: "${TEST_REPO_URL}"
                }
            }
        }
        
        stage('Build and Deploy App') {
            steps {
                echo "--- Building Flask App ---"
                // This builds the application image and deploys the Part II stack
                sh 'docker compose up -d --build'
                sh 'sleep 30' // Wait for DB and app to stabilize
            }
        }
        
        stage('Build Test Image') {
            steps {
                echo "--- Building Test Docker Image with Chrome (using Dockerfile.tests-java) ---"
                dir(TEST_REPO_DIR) {
                    // Assuming Dockerfile.tests-java is located in the test-repo directory
                    sh "docker build -t ${TEST_IMAGE_TAG} -f Dockerfile.tests-java ."
                }
            }
        }
        
        stage('Run Tests') {
            steps {
                echo "--- Running Maven Tests in Container with Chrome ---"
                // Running the custom built image, mounting the source code, and executing Maven
                sh """
                    docker run --rm \
                    --network host \
                    --shm-size=2g \
                    -e BASE_URL=${BASE_URL} \
                    -v "\$(pwd)/${TEST_REPO_DIR}/${TEST_FOLDER}":/app \
                    -v "\$(pwd)/${TEST_REPO_DIR}/${TEST_FOLDER}/target":/app/target \
                    ${TEST_IMAGE_TAG} \
                    /bin/bash -c "mvn clean test"
                """
            }
            post {
                always {
                    // Publish the test results using the Surefire report generated in the target directory
                    junit "${TEST_REPO_DIR}/${TEST_FOLDER}/target/surefire-reports/*.xml"
                }
            }
        }
        
        stage('Cleanup') {
            steps {
                echo "--- Final Cleanup (App and Image) ---"
                sh 'docker compose down --rmi all'
                sh "docker rmi ${TEST_IMAGE_TAG} 2>/dev/null || true"
            }
        }
    }
    
    post {
        always {
            echo "Pipeline finished. Check test report."
            
            script {
                // Get email from git (fallback to your email if extraction fails)
                def recipientEmail = env.GIT_COMMITTER_EMAIL
                
                // CRITICAL: Ensure the grading email is always included
                if (!recipientEmail || recipientEmail == '') {
                    recipientEmail = 'qasimalik@gmail.com'
                } else if (!recipientEmail.contains('qasimalik@gmail.com')) {
                    // If git email is valid, include the grading email as well
                    recipientEmail = "${recipientEmail},qasimalik@gmail.com"
                } else {
                    // Fallback in case of extraction error
                    recipientEmail = 'qasimalik@gmail.com'
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

View Build: ${env.BUILD_URL}
Test Report: ${env.BUILD_URL}testReport/

---
Automated notification from Jenkins CI/CD Pipeline
                         """
                    
                    echo "✓ Email requested successfully to: ${recipientEmail}"
                } catch (Exception e) {
                    echo "✗ Failed to send email (Check Jenkins System Config): ${e.getMessage()}"
                }
            }
        }
        success {
            echo '✓ Tests passed! Preparing success email.'
        }
        failure {
            echo '✗ Tests failed! Preparing failure email.'
        }
    }
}
