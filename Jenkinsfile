pipeline{
    agent any
    stages{
        stage("Deploy"){
            steps{
                sh "docker compose down"
                sh "docker compose up -d --build"
            }
            
        }

        stage("Health checks"){
            steps{
                sh "sleep 5"
                curl http://host.docker.internal:8005/health
            }
        }
    }
}
