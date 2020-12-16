def groovyfile
pipeline {
  agent any

  stages {
    stage('Build Script') {
        steps {
            script {
                def filename = 'jenkins.' + env.BRANCH_NAME + '.groovy'
                groovyfile = load filename
            }
        }
    }

    stage('Build Tweets app') {
        steps{
            script{
                groovyfile.build_app()
            }
        }
    }
	  
  
      stage('Build Flask Docker Image'){
	sh 'docker build -t myflaskapp .' 
      }
      stage('Run Docker Image') {
	steps {
	  echo 'Running Flask app'
	  sh 'docker run -p 5000:5000 -d --name  myflaskapp  myflaskapp'
	}
      }
  

    stage('Testing') {
        steps {
            script {
                groovyfile.test_app()
            }
        }
    }

    stage('Docker images down') {
        steps {
            script {
                groovyfile.down_app()
            }
        }
	}
      stage('Create release branch') {
        steps {
            script {
                groovyfile.release_app()
            }
        }
      }
    }
}
