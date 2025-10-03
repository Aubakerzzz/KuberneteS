
pipeline {
    agent any

    environment {
        // Set environment variables if needed
        COMPOSE_PROJECT = "mlops_assignment_01"
        BRANCH_NAME = "${env.BRANCH_NAME ?: 'main'}"
        DOCKERHUB_CREDENTIALS = 'dockerhub-creds' // Replace with your Jenkins credentials ID
        GIT_CREDENTIALS = 'github-pat'           // Replace with your GitHub credentials ID
    }

    stages {

        stage('Checkout Code') {
            steps {
                echo "Checking out repository..."
                checkout([
                    $class: 'GitSCM',
                    branches: [[name: "*/${BRANCH_NAME}"]],
                    doGenerateSubmoduleConfigurations: false,
                    extensions: [],
                    userRemoteConfigs: [[
                        url: 'https://github.com/MLOPS-Fall-2025/ci-cd-with-jenkins-and-stock-prediction-Aubakerzzz.git',
                        credentialsId: "${GIT_CREDENTIALS}"
                    ]]
                ])
            }
        }

        stage('Clean Docker Environment') {
            steps {
                script {
                    echo "Stopping and removing old containers and networks..."
                    sh '''
                        docker-compose -f docker-compose.yml down --remove-orphans
                        docker container prune -f
                    '''
                }
            }
        }

        stage('Build Docker Images') {
            steps {
                script {
                    echo "Building Docker images for backend, frontend, db..."
                    sh 'docker-compose -f docker-compose.yml build'
                }
            }
        }

        stage('Run Backend Tests') {
            steps {
                script {
                    echo "Running backend tests inside Docker container..."
                    sh '''
                        docker-compose -f docker-compose.yml run --rm backend bash -c "pip install -r requirements.txt && pytest --maxfail=1 --disable-warnings -q"
                    '''
                }
            }
        }

        stage('Push Docker Images') {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: "${DOCKERHUB_CREDENTIALS}", usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                        sh '''
                            echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin

                            # Push backend, frontend, db images
                            for service in backend frontend db; do
                                LOCAL_IMAGE="${COMPOSE_PROJECT}-$service:latest"
                                REMOTE_IMAGE="$DOCKER_USER/$service:${BRANCH_NAME}"
                                echo "Tagging $LOCAL_IMAGE as $REMOTE_IMAGE"
                                docker tag $LOCAL_IMAGE $REMOTE_IMAGE
                                docker push $REMOTE_IMAGE
                            done

                            docker logout
                        '''
                    }
                }
            }
        }

        stage('Deploy Containers') {
            steps {
                script {
                    echo "Deploying containers..."
                    sh 'docker-compose -f docker-compose.yml up -d'
                }
            }
        }

    }

    post {
        always {
            echo "Cleaning workspace..."
            cleanWs()
        }
        success {
            echo "Pipeline completed successfully!"
        }
        failure {
            echo "Pipeline failed! Check logs."
        }
    }
}
