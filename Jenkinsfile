def groovyfile

pipeline {
    agent {
        docker {
            image 'python:3.6'
        }
    }

    stages {
        stage('Build script') {
            steps {
                script {
                    def filename = 'jenkins.' + env.BRANCH_NAME + '.groovy'
                    groovyfile = load filename
                }
            }
        }

        stage('Testing') {
            steps {
                script {
                    groovyfile.test_app()
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
