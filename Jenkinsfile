// This Jenkinsfile defines the CI/CD pipeline for the build phase.
pipeline {
    agent any

    stages {
        stage('Checkout Source Code from GitHub') {
            steps {
                // REQUIRED: Fetches the code from the repository. 
                // ***IMPORTANT: Update URL with your repository's HTTPS URL***
                git branch: 'main', url: 'https://github.com/popsicles-dev/DevOps-Assignment2-Pipeline.git'
            }
        }
        
        stage('Containerized Build and Deployment') {
            steps {
                // Runs the Docker Compose file, forces a rebuild, and launches the application
                sh 'docker compose up -d --build'
                
                sh 'echo "Deployment to host port 8081 is complete."'
            }
        }
    }
    
    post {
        always {
            // Check container status after the build
            sh "docker ps -a"
        }
    }
}