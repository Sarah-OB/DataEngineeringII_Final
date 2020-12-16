def requirements_app() {
    sh 'pip install Flask requests'
}

def test_app(){
  sh 'python test_app.py '
}


def develop_app(){
  echo 'Branch into develop'
}

return this
