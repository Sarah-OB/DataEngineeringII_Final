def test_app(){
  //sh 'python test_app.py '
  sh 'virtualenv venv && . venv/bin/activate && pip install requests && python test_app.py'
}


def develop_app(){
  echo 'Branch into develop'
}

return this
