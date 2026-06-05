pipeline {
    agent any

    environment {
        PATH = "/home/ubuntu/.local/bin:${env.PATH}"
    }

    stages {
        stage('Get Code') {
            steps {
                checkout([
                    $class: 'GitSCM', 
                    branches: [[name: '*/develop']], 
                    extensions: [], 
                    userRemoteConfigs: [[url: 'https://github.com/jmunozhe1/todo-list-aws.git']]
                ])
            }
        }

        stage('Static Test') {
            steps {
                sh 'pip install --user flake8 bandit'
                sh 'flake8 src/ > flake8-report.txt || true'
                sh 'bandit -r src/ -f txt -o bandit-report.txt || true'
                archiveArtifacts artifacts: 'flake8-report.txt, bandit-report.txt', allowEmptyArchive: false
            }
        }

        stage('Deploy') {
            steps {
                sh 'sam build'
                sh 'sam deploy --config-env staging --no-confirm-changeset'
            }
        }

        stage('Rest Test') {
            steps {
                sh 'pip install --user pytest requests'
                script {
                    def apiUrl = sh(
                        script: "aws cloudformation describe-stacks --stack-name staging-todo-list-aws --query \"Stacks[0].Outputs[?OutputKey=='BaseUrlApi'].OutputValue\" --output text",
                        returnStdout: true
                    ).trim()
                    
                    withEnv(["BASE_URL=${apiUrl}"]) {
                        sh 'pytest test/integration/todoApiTest.py'
                    }
                }
            }
        }

        stage('Promote') {
            steps {
                sh '''
                    git checkout master
                    git merge origin/develop --no-edit
                    git push origin master
                '''
            }
        }
    }
}