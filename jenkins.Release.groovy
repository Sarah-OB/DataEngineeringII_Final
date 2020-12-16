def build_app(){
  sh 'docker-compose up -d'
}

def e2e_test(){
  echo 'release-specific testing here'
}
def user_acceptance(){
  input "Proceed with deployment to production ?"
}

def test_app(){
  e2e_test()
  user_acceptance()
}

def down_app(){
  sh 'docker-compose down'
}

def production_app(){
  echo 'Merging with main'
}

return this
