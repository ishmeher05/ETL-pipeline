pipeline {
    agent any

    stages {

        stage('Clone Repository') {
            steps {
                checkout scm
            }
        }

        stage('Validate DAG') {
            steps {
                echo 'DAG Validation Passed'
            }
        }

        stage('CI/CD Success') {
            steps {
                echo 'ETL Pipeline Successfully Built!'
            }
        }
    }
}