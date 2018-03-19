# Fingerprinting for Learning Analytics
Student fingerprinting service for Learning Analytics Seminar @ Goethe University Frankfurt WS17/18 

The seminar paper is located in `paper/`, while the whole service written mostly in python is located in `laprint/`.

## Installing

* I suggest using virtualenv for initial testing. 
* Written and tested with python 3.6.4, requires `flask` (version 0.12.2).

Recommended/Tested installation process:

* (opt.) Install virtualenv `pip install virtualenv`
* create a virtualenv in the root directory `virtualenv your-virtualenv-name`
* initiate it with `source your-virtualenv-name/bin/activate`
* Install requirements `pip install flask`


## Setup

* Go to `laprint` root.
* `export FLASK_APP="init"` (Linux/MacOS, on windows replace `export` with `SET`)
* (opt.) `export FLASK_DEBUG=true`
* `flask initdb` (will destroy the database you had before)
* `flask run`
* Go to `127.0.0.1:5000`.

Note that there is a bug where flask can't find the app object, try `python -m flask run/initdb` instead.

I used Nginx on Ubuntu to serve this Application, rather strictly following [this tutorial](https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-uwsgi-and-nginx-on-ubuntu-16-04). You can try as well, but you should check the web for other, maybe more suitable choices. If everything fails, feel free to message me! There will be an instance running online until mid April.