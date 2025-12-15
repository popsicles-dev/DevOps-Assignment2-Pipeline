pipeline {
    agent any  // Use 'any' so Docker commands work on the host
    
    environment {
        BASE_URL = 'http://16.171.224.162' 
        TEST_REPO_URL = 'https://github.com/popsicles-dev/DevOps-Selenium-Tests.git' 
        TEST_FOLDER = 'java-tests'  // Match your actual folder name
    }

    stages {
        stage('Checkout Source Codes') {
            steps {
                echo "--- 1. Checkout Application Code ---"
                checkout scm  // Checks out current repo (app repo with Jenkinsfile)
                
                echo "--- 2. Checkout Java Test Code ---"
                dir('test-repo') {
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
        
        stage('Test Execution (Maven in Docker)') {
            steps {
                echo "--- Running Maven Tests in Docker Container ---"
                script {
                    // Run Maven tests inside a Docker container
                    sh """
                        docker run --rm \
                        -v \$(pwd)/test-repo/${TEST_FOLDER}:/app \
                        -v \$HOME/.m2:/root/.m2 \
                        -w /app \
                        -e BASE_URL=${BASE_URL} \
                        maven:3.9.5-amazoncorretto-17 \
                        mvn clean test -DbaseUrl=${BASE_URL}
                    """
                }
            }
            post {
                always {
                    junit "test-repo/${TEST_FOLDER}/target/surefire-reports/*.xml"
                }
            }
        }
        
        stage('Cleanup Deployment') {
            steps {
                echo "--- Tearing down deployment ---"
                sh 'docker compose down --rmi all'
            }
        }
    }
    
    post {
        always {
            echo "Pipeline finished. Check test report for status."
        }
    }
}
