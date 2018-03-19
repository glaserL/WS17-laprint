import os

from flask import Flask, g
from werkzeug.utils import find_modules, import_string
from laprint.blueprints.laprint import init_db
# Boring Setup stuff

def create_app(config=None):
	app = Flask('laprint') # flask object
	# app.config.from_object(__name__) #load configs from here, could be another config file
	app.config.update(dict(
		DATABASE = os.path.join(app.root_path, 'laprint.db'),
		SECRET_KEY = 'verysecretkeydontleaveunset',
		USERNAME='admin',
		PASSWORT='admin',
		DEBUG=True
	))
	app.config.update(config or {})
	app.config.from_envvar('LAPRINT_SETTINGS', silent=True)

	register_blueprints(app)
	register_cli(app)
	register_teardowns(app)

	return app

def register_blueprints(app):
	"""collects all blueprints and adds them to the app object"""
	for name in find_modules('laprint.blueprints'):
		mod = import_string(name)
		if hasattr(mod, 'bp'):
			app.register_blueprint(mod.bp)
	return None

def register_cli(app):
	@app.cli.command('initdb')
	def initdb_command():
		"""Initializes the database, used on command line as 'flask initdb'"""
		init_db()
		print("Initialized the database.")

def register_teardowns(app):
	@app.teardown_appcontext
	def close_db(error):
		"""closes the db connection either safely or when an error occurred"""
		if hasattr(g, 'sqlite_db'):
			g.sqlite_db.close()

app = create_app()