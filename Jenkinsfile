pipeline {
    agent any

    stages {

        stage('Clone Repository') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                bat 'python -m pip install -r requirements.txt'
            }
        }

        stage('Validate DAG') {
            steps {
                bat 'python dags/exampledag.py'
            }
        }

        stage('CI/CD Success') {
            steps {
                echo 'ETL Pipeline Successfully Built!'
            }
        }
    }
}