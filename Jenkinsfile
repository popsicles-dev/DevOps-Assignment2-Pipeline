pipeline {
    // CRITICAL: Use a Docker agent that contains Java and Maven
    // This removes the need to install Maven/JDK directly on the EC2 host.
    agent {
        docker {
            image 'maven:3.9.5-amazoncorretto-17' 
            // We mount the local workspace into the container so Maven can find the test code
            args '-v $HOME/.m2:/root/.m2' 
        }
    }
    
    environment {
        // CRITICAL: This environment variable passes the target URL to your Java tests
        BASE_URL = 'http://16.171.224.162' 
        TEST_REPO_URL = 'https://github.com/popsicles-dev/DevOps-Selenium-Tests.git' 
        TEST_FOLDER = 'java-selenium-tests' // We will put the Java repo in a new folder
        
        // Email configuration (CRITICAL for marks)
        RECIPIENT_EMAIL = 'qasimalik@gmail.com'
    }

    stages {
        stage('Checkout Source Codes') {
            steps {
                echo "--- 1. Checkout Application Code (Jenkinsfile source) ---"
                // This checks out the repo containing the Jenkinsfile
                git branch: 'main', url: 'https://github.com/popsicles-dev/DevOps-Assignment2-Pipeline.git'
                
                echo "--- 2. Checkout Java Test Code ---"
                dir(TEST_FOLDER) {
                    // Clones the separate Java test repository locally
                    git branch: 'main', url: TEST_REPO_URL
                }
            }
        }
        
        // Deployment stage remains the same (assumes docker-compose is in the root)
        stage('Build and Deploy App') {
            steps {
                echo "--- Building and Deploying Python App (Part II) ---"
                // Builds the Python image and deploys the stack
                sh 'docker compose up -d --build'
                sh 'sleep 30' // Wait for DB and app to stabilize
            }
        }
        
        stage('Test Execution (Maven)') {
            steps {
                echo "--- Running Maven Tests (JDK 17) ---"
                // CRITICAL: Maven commands run inside the Docker agent
                dir(TEST_FOLDER) {
                    // 'clean install' compiles the code, runs the tests, and generates the report
                    // The BASE_URL is passed automatically via the 'environment' section
                    sh 'mvn clean install'
                }
            }
            post {
                // Publish the Surefire XML results for Jenkins reporting
                always {
                    // Assuming Surefire generated test reports here
                    junit "${TEST_FOLDER}/target/surefire-reports/*.xml"
                }
            }
        }
        
        stage('Cleanup Deployment') {
            steps {
                echo "--- Tearing down deployment after tests ---"
                sh 'docker compose down --rmi all'
            }
        }
    }
    
    post {
        always {
            echo "Pipeline finished. Check test report for status."
        }
}
