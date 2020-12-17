def test_app(){
    sh 'pip install flask nltk gensim unidecode pandas'
    sh 'python test_app_norequests.py'
}

def down_image(){
    sh 'docker rm -f python'
}

def develop_app(){
  echo 'Branch into develop'
}

return this
