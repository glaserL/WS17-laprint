DROP TABLE IF EXISTS fingerprints;
CREATE TABLE fingerprints (
	id INTEGER PRIMARY KEY autoincrement,
	useragent TEXT NOT NULL,
	accept TEXT NOT NULL,
	accept_language TEXT NOT NULL,
	accept_encoding TEXT NOT NULL,
	guessphrase TEXT
);

DROP TABLE IF EXISTS guesses;
CREATE TABLE guesses (
	id INTEGER PRIMARY KEY autoincrement,
	visit TEXT NOT NULL,
	guess TEXT NOT NULL
);