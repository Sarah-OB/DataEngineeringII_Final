def test_app(){
    //sh 'pip install flask nltk gensim unidecode pandas'
    //sh 'python -m unittest test_app_nodocker.py'
    sh 'virtualenv venv && . venv/bin/activate && pip install flask nltk gensim unidecode pandas && python -m unittest test_app_nodocker.py'
}


def develop_app(){
  echo 'Branch into develop'
}

return this
