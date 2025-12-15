pipeline {
    agent any
    
    environment {
        BASE_URL = 'http://16.171.224.162' 
        TEST_REPO_URL = 'https://github.com/popsicles-dev/DevOps-Selenium-Tests.git' 
        TEST_FOLDER = 'java-tests'
    }

    stages {
        stage('Cleanup Old Containers') {
            steps {
                echo "--- Cleaning up old containers ---"
                sh '''
                    docker compose down --remove-orphans 2>/dev/null || true
                    docker rm -f mysql_db_container_part2 flask_web_container_part2 2>/dev/null || true
                '''
            }
        }
        
        stage('Checkout Application Code') {
            steps {
                echo "--- Checkout Application Code ---"
                checkout scm
            }
        }
        
        stage('Checkout Test Code') {
            steps {
                echo "--- Checkout Test Code ---"
                dir('test-repo') {
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
                dir('test-repo') {
                    sh 'docker build -t selenium-tests:latest -f Dockerfile.tests-java .'
                }
            }
        }
        
        stage('Run Tests') {
            steps {
                echo "--- Running Maven Tests in Container with Chrome ---"
                sh """
                    docker run --rm \
                    --network host \
                    -e BASE_URL=${BASE_URL} \
                    -v \$(pwd)/test-repo/${TEST_FOLDER}/target:/app/target \
                    selenium-tests:latest
                """
            }
            post {
                always {
                    junit "test-repo/${TEST_FOLDER}/target/surefire-reports/*.xml"
                }
            }
        }
        
        stage('Cleanup') {
            steps {
                echo "--- Final Cleanup ---"
                sh 'docker compose down --rmi all'
                sh 'docker rmi selenium-tests:latest 2>/dev/null || true'
            }
        }
    }
    
    post {
        always {
            echo "Pipeline finished. Check test report."
        }
    }
}
