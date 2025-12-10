pipeline {
    agent any
    
    // Define environment variables
    environment {
        // CRITICAL: Replace with the actual running IP of your Assignment 2, Part I EC2 deployment (Port 80)
        TARGET_APP_URL = 'http://<Part_I_EC2_Public_IP>' 
        // Replace with your actual Test Repository URL
        TEST_REPO_URL = 'https://github.com/popsicles-dev/DevOps-Selenium-Tests.git' 
        // Container Name defined in your docker-compose.yml
        TEST_CONTAINER = 'flask_web_container_part2'
        
        // Email configuration (CRITICAL for marks)
        RECIPIENT_EMAIL = 'qasimalik@gmail.com'
    }

    stages {
        stage('Checkout Source Codes') {
            steps {
                echo "--- 1. Checkout Application Code ---"
                // Checks out this repository (the one containing the Jenkinsfile)
                git branch: 'main', url: 'https://github.com/popsicles-dev/DevOps-Assignment2-Pipeline.git'
                
                echo "--- 2. Checkout Test Code ---"
                dir('test-code') {
                    // Clones the separate test repository locally into 'test-code' folder
                    git branch: 'main', url: TEST_REPO_URL
                }
            }
        }
        
        stage('Build and Deploy') {
            steps {
                echo "--- Building new image with Chrome/Chromedriver and Deploying ---"
                // The '--build' flag forces Jenkins to use the NEW Dockerfile with Chrome installed
                sh 'docker compose up -d --build'
                sh 'sleep 30' // Wait for DB and app to stabilize
            }
        }
        
        stage('Test Execution') {
            steps {
                script {
                    echo "--- Running Selenium Tests ---"
                    
                    // 1. Copy test files into the running web container
                    sh "docker cp test-code/. ${TEST_CONTAINER}:/usr/src/app/tests"
                    
                    // 2. Install test dependencies (Selenium, Pytest) inside the running container
                    // This is necessary because the application environment only installs app requirements
                    sh "docker exec ${TEST_CONTAINER} pip install --no-cache-dir -r /usr/src/app/tests/requirements.txt"
                    
                    // 3. Execute Pytest, using the TARGET_APP_URL for the tests
                    // The '--junitxml' option generates a report Jenkins can read
                    sh "docker exec ${TEST_CONTAINER} pytest /usr/src/app/tests/test_app.py --junitxml=test-results.xml"
                }
            }
            post {
                // Publish the JUnit XML results for Jenkins reporting
                always {
                    junit 'test-results.xml'
                }
            }
        }
        
        stage('Cleanup Deployment') {
            steps {
                echo "--- Tearing down deployment after tests ---"
                // Tear down the Part II environment immediately after tests
                sh 'docker compose down --rmi all'
            }
        }
    }
    
    post {
        // --- CRITICAL: EMAIL NOTIFICATION (4 Marks Component) ---
        // This relies on the Mailer Plugin and correct SMTP setup in Jenkins
        success {
            mail to: RECIPIENT_EMAIL,
                 subject: "SUCCESS: ${JOB_NAME} Build ${BUILD_NUMBER} Tests Passed",
                 body: "Build and test for ${JOB_NAME} succeeded. View results: ${BUILD_URL}testReport/"
        }
        failure {
            mail to: RECIPIENT_EMAIL,
                 subject: "FAILURE: ${JOB_NAME} Build ${BUILD_NUMBER} Tests Failed",
                 body: "Build and test for ${JOB_NAME} FAILED. Review console output here: ${BUILD_URL}console"
        }
        // Ensure the email is also sent if the collaborator (the pusher) has an email associated with their GitHub push
        // This is handled by the Mailer Plugin if properly configured in Jenkins System settings.
    }
}
