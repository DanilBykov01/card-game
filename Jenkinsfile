pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/DanilBykov01/card-game.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                  set -e
                  docker build -t card-game:latest -t card-game:$BUILD_NUMBER .
                '''
            }
        }

        stage('Run Smoke Test') {
            steps {
                sh '''
                  set -e
                  PORT=$((18000 + BUILD_NUMBER))
                  echo "Using port: $PORT"
                  CID=$(docker run -d -p $PORT:8000 --name cg_test_$BUILD_NUMBER card-game:latest)
                  sleep 10
                  curl -f "http://localhost:$PORT/" | tee /tmp/smoke_output.txt
                '''
            }
        }
    }

    post {
        always {
            sh '''
              docker rm -f cg_test_$BUILD_NUMBER >/dev/null 2>&1 || true
            '''
        }
    }
}

