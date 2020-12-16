def build_app(){
  sh 'docker-compose up -d'
}

def down_app(){
  sh 'docker-compose down'
}

return this
