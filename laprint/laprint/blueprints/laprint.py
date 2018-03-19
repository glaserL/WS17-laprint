### Interacting with the sqlite3 database

import sqlite3
from flask import Blueprint, request, g, redirect, url_for, \
render_template, current_app

bp = Blueprint('laprint', __name__)

### DATABASE SERVICES ###
def connect_db():
	"""get database connection"""
	rv = sqlite3.connect(current_app.config['DATABASE'])
	rv.row_factory = sqlite3.Row
	return rv

def get_db():
	"""returns the db context or creates a new one if none exists"""
	if not hasattr(g, 'sqlite_db'):
		g.sqlite_db = connect_db()
	g.sqlite_db.row_factory = sqlite3.Row
	return g.sqlite_db

def init_db():
	"""initializes the database, use this for testing purposes"""
	db = get_db()
	with current_app.open_resource('schema.sql', mode = 'r') as init_file:
		db.cursor().executescript(init_file.read())
	db.commit()

def query_db(query, args=(), one=False):
    """interface for query db, enforces escaping"""
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def insert_db(table, fields=(), values=()):
    
    cur = get_db().cursor()
    query = 'INSERT INTO %s (%s) VALUES (%s)' % (
        table,
        ', '.join(fields),
        ', '.join(['?'] * len(values))
    )
    cur.execute(query, values)
    get_db().commit()
    id = cur.lastrowid
    cur.close()
    return id


### SITES OF SERVICE ###

@bp.route('/')
def main():
	guess = guess_User(request.headers)
	stats = query_db('SELECT count(id) AS c FROM fingerprints', one = True)
	return render_template('main.html', stats = stats)
	
@bp.route('/fingerprint')
def fingerprint():
	guess = guess_User(request.headers)
	if guess != None:
		print("Assuming \"%s\" as correct guessphrase.." % (guess))
		return render_template('fingerprint.html', guess = guess)
	else:
		return render_template('fingerprint.html')

@bp.route('/final')
def final():
	"""Good bye message"""
	return render_template('final.html')


@bp.route('/about')
def about():
	""" small about page with impressum and contact"""
	return render_template('about.html')


def save_guess(form):
	"""Recieves a filled out form and writes the quality relevant values to db"""
	print('Writing guess confirmation..')
	visited = form['visitedfb']
	guessfeedback = "N/A" if ('guessfb' not in form) else form['guessfb'] 
	confirm = insert_db("guesses", ('visit', 'guess'), (visited, guessfeedback))
	print("Success, already wrote "+str(confirm)+" guesses.")

def create_fingerprint(guessphrase, headers):
	useragent = request.headers.get('User-Agent', 'ERROR')
	accept = request.headers.get('Accept', 'ERROR')
	accept_language = request.headers.get('Accept-Language', 'ERROR')
	accept_encoding = request.headers.get('Accept-Encoding', 'ERROR')
	insert_db("fingerprints", 
		('useragent', 'accept', 'accept_language', 'accept_encoding', 'guessphrase'),
		(useragent, accept, accept_language, accept_encoding, guessphrase))
	print("""Added Fingerprint: 
	useragent:\t%s
	accept:\t%s
	accept_language:\t%s
	accept_encoding:\t%s""" % (useragent,accept,accept_language,accept_encoding))

# WRITE PAGES
@bp.route('/addNew', methods=['POST'])
def addNew():

	if request.method == 'POST':
		print("Received guessphrase: " + request.form['guessphrase'])
		save_guess(request.form)
		if(request.form['visitedfb'] == "no"): # we don't want doubled guessphrases
			create_fingerprint(request.form['guessphrase'],request.headers)
	return redirect(url_for('laprint.final'))


### SERVICE FUNCTION ###
def guess_User(headers):
	import random
	candidates = retrieve_guess(headers)
	if len(candidates)>1: # we saw this fingerprint more than once, but we try our luck
		return random.choice(candidates)
	elif len(candidates)==1:
		# we've seen this fingerprint once already
		return candidates[0]
	else:
		return None # we've not seen this fingerprint yet, so we assume she/he is new.

def retrieve_guess(headers):
	useragent = request.headers.get('User-Agent', 'ERROR')
	accept = request.headers.get('Accept', 'ERROR')
	accept_language = request.headers.get('Accept-Language', 'ERROR')
	accept_encoding = request.headers.get('Accept-Encoding', 'ERROR')
	result = query_db("""SELECT guessphrase FROM fingerprints WHERE useragent = ?
		AND accept = ? AND accept_language = ? AND accept_encoding = ?""",
		[useragent, accept, accept_language, accept_encoding])
	candidates = [row['guessphrase'] for row in result]
	print("Found %d potential fingerprint candidates.." % (len(candidates)))
	return candidates
