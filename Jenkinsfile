pipeline {
    agent any

    environment {
        IMAGE_NAME = "docker-jenkins-app"
        CONTAINER_NAME = "docker-jenkins-app"
        HOST_PORT = "8081"
        CONTAINER_PORT = "5000"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build') {
            steps {
                sh '''
                    echo "Build stage started"
                    python3 --version
                    pip3 --version
                    pip3 install -r requirements.txt
                '''
            }
        }

        stage('Test') {
            steps {
                sh '''
                    echo "Running tests..."
                    python3 -m pytest -v
                '''
            }
        }

        stage('Docker Build') {
            steps {
                sh '''
                    echo "Building Docker image..."
                    docker build -t ${IMAGE_NAME}:latest .
                '''
            }
        }

        stage('Docker Run') {
            steps {
                sh '''
                    echo "Stopping old container if it exists..."
                    docker rm -f ${CONTAINER_NAME} 2>/dev/null || true

                    echo "Starting new container..."
                    docker run -d \
                      --name ${CONTAINER_NAME} \
                      -p ${HOST_PORT}:${CONTAINER_PORT} \
                      ${IMAGE_NAME}:latest

                    sleep 5

                    docker ps
                '''
            }
        }

        stage('Health Check') {
            steps {
                sh '''
                    echo "Checking application health..."

                    for i in 1 2 3 4 5
                    do
                        if curl -f http://localhost:${HOST_PORT}/health
                        then
                            echo
                            echo "Application is HEALTHY"
                            exit 0
                        fi

                        echo "Health check failed - retrying..."
                        sleep 3
                    done

                    echo "Application is DOWN"
                    docker logs ${CONTAINER_NAME}
                    exit 1
                '''
            }
        }
    }

    post {
        success {
            echo 'CI pipeline completed successfully. Application is healthy.'
        }

        failure {
            echo 'CI pipeline failed. Check the stage logs.'
        }
    }
}
