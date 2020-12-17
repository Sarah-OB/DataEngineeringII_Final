def groovyfile

pipeline {
    agent any

    stages {
        stage('Build script') {
            steps {
                script {
                    def filename = 'jenkins.' + env.BRANCH_NAME + '.groovy'
                    groovyfile = load filename
                }
            }
        }

        stage('Build python app') {
            steps {
                sh 'docker run -d -p 5000:5000 --name python:latest'
            }
        }

        stage('Testing') {
            steps {
                script {
                    withPythonEnv("HOME=${env.WORKSPACE}"){
                        groovyfile.test_app()
                    }
                }
            }
        }

        stage('Down image'){
            steps {
                script {
                    groovyfile.down_image()
                }
            }
        }

        stage('Ready app'){
            steps {
                script {
                    groovyfile.develop_app()
                }
            }
        }
    }
}
