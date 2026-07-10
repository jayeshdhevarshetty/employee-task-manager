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
                sh "curl http://employee-task-manager:8005"
            }
        }
    }
}
