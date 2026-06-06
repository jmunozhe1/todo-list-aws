pipeline {
    agent any

    environment {
        PATH = "/var/lib/jenkins/.local/bin:${env.PATH}"
    }

    stages {
        stage('Get Code') {
            steps {
                echo 'Codigo fuente descargado correctamente desde la rama develop.'
            }
        }

        stage('Static Test') {
            steps {
                sh 'pip install --break-system-packages flake8 bandit'
                sh 'flake8 src/ > flake8-report.txt || true'
                sh 'bandit -r src/ -f txt -o bandit-report.txt || true'
                archiveArtifacts artifacts: 'flake8-report.txt, bandit-report.txt', allowEmptyArchive: false
            }
        }

        stage('Deploy') {
            steps {
                sh 'sam build'
                sh 'sam deploy --config-env staging --no-confirm-changeset --no-fail-on-empty-changeset --s3-bucket aws-sam-cli-managed-default-samclisourcebucket-7zzg7iedbe1i --no-resolve-s3'
            }
        }

        stage('Rest Test') {
            steps {
                sh 'pip install --break-system-packages pytest requests'
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
                withCredentials([usernamePassword(credentialsId: 'git-credentials', usernameVariable: 'GIT_USER', passwordVariable: 'GIT_TOKEN')]) {
                    sh '''
                        git config user.email "jenkins@ci.com"
                        git config user.name "Jenkins CI"
                        git checkout master
                        git merge origin/develop --no-edit
                        
                        git push https://${GIT_USER}:${GIT_TOKEN}@github.com/jmunozhe1/todo-list-aws.git master
                    '''
                }
            }
        }
    }
}