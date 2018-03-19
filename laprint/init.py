from laprint import factory

app = factory.create_app() # flask object

if __name__ == "__main__":
	app.run(host='0.0.0.0')