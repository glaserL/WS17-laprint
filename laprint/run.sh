export FLASK_APP="laprint.factory:create_app()"
export FLASK_DEBUG=true
flask initdb
flask run
