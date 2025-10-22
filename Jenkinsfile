pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/DanilBykov01/card-game.git'
            }
        }
        stage('Build Docker Image') {
            steps {
                sh 'docker build -t card-game:latest .'
            }
        }
        stage('Run Smoke Test') {
            steps {
                sh '''
                  CID=$(docker run -d -p 18000:8000 card-game:latest)
                  sleep 3
                  curl -f http://localhost:18000/ || (docker logs $CID && exit 1)
                  docker rm -f $CID
                '''
            }
        }
    }
}

