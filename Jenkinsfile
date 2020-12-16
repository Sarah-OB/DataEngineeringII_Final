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

        stage('Build app') {
            steps {
                script {
                    groovyfile.build_app()
                }
            }
        }

        stage('Down app'){
            steps {
                script {
                    groovyfile.down_app()
                }
            }
        }
    }
}
