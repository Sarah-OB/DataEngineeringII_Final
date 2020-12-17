def build_app(){
  sh 'docker-compose up -d'
  //sh 'docker build -t myflaskapp .'
  //sh 'docker run -p 5000:5000 -d --name  myflaskapp  myflaskapp'
}

def test_app(){
  sh 'python test_app.py'
}

def stress_test_app() {
    sh 'echo http://127.0.0.1:5000/?{1..1000} | xargs -n 1 -P 1000 curl -s'
    echo 'Stress test'
}

def down_app(){
  sh 'docker-compose down'
}

def release_app(){
  echo 'Branch into release'
}

return this
