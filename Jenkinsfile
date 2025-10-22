pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                // Код всё равно чекаутится Jenkins'ом до старта pipeline,
                // но оставим явный шаг, чтобы было наглядно.
                git branch: 'main', url: 'https://github.com/DanilBykov01/card-game.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                  set -e
                  docker build -t card-game:latest .
                '''
            }
        }

        stage('Run Smoke Test') {
            steps {
                sh '''
                  set -e
                  # Запускаем контейнер
                  CID=$(docker run -d -p 18000:8000 --name cg_test_$BUILD_NUMBER card-game:latest)

                  # Даём приложению подняться
                  sleep 3

                  # Берём IP адрес контейнера (внутри docker-сети)
                  IP=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' $CID)
                  echo "Container ID: $CID"
                  echo "Container IP: $IP"

                  # Обращаемся прямо к контейнеру по его IP и внутреннему порту 8000
                  curl -f "http://$IP:8000/" | tee /tmp/smoke_output.txt

                  # Если дошли сюда — всё ок. Чистим контейнер.
                  docker rm -f $CID
                '''
            }
        }
    }

    post {
        always {
            // На всякий случай прибьём тестовый контейнер, если он вдруг остался
            sh 'docker rm -f cg_test_$BUILD_NUMBER >/dev/null 2>&1 || true'
        }
    }
}

