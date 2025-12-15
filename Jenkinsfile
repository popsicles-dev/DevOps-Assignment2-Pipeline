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
                    --shm-size=2g \
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
            
            emailext (
                subject: "Jenkins Build ${currentBuild.result}: ${env.JOB_NAME} - Build #${env.BUILD_NUMBER}",
                body: """
                    <h2>Build ${currentBuild.result}</h2>
                    <p><b>Job:</b> ${env.JOB_NAME}</p>
                    <p><b>Build Number:</b> ${env.BUILD_NUMBER}</p>
                    <p><b>Build Status:</b> ${currentBuild.result}</p>
                    <p><b>Build Duration:</b> ${currentBuild.durationString}</p>
                    <p><b>Build URL:</b> <a href="${env.BUILD_URL}">${env.BUILD_URL}</a></p>
                    <p><b>Test Report:</b> <a href="${env.BUILD_URL}testReport/">${env.BUILD_URL}testReport/</a></p>
                    <hr>
                    <p><b>Console Output:</b> <a href="${env.BUILD_URL}console">${env.BUILD_URL}console</a></p>
                """,
                to: 'hifsashafique8@gmail.com',
                mimeType: 'text/html'
            )
        }
        success {
            echo '✓ Tests passed! Email sent.'
        }
        failure {
            echo '✗ Tests failed! Email sent.'
        }
    }
}
