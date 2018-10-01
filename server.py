from flask import Flask, session, url_for, redirect, request, render_template, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
import bcrypt
from datetime import datetime, date, timedelta

app = Flask(__name__)
app.secret_key = "debug-attivo"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.config.from_object(__name__)


class User(db.Model):
    uid = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.LargeBinary, nullable=False)
    nome = db.Column(db.String, nullable=False)
    cognome = db.Column(db.String, nullable=False)
    titolo = db.Column(db.String, nullable=False)
    ruolo = db.Column(db.String, nullable=False)

    def __init__(self, nome, cognome, titolo, ruolo, email, password):
        self.nome = nome
        self.cognome = cognome
        self.titolo = titolo
        self.ruolo = ruolo
        self.email = email
        p = bytes(password, encoding="utf-8")
        self.password = bcrypt.hashpw(p, bcrypt.gensalt())

    def __repr__(self):
        return "{}-{}".format(self.uid, self.email)


class Prodotto(db.Model):
    pid = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String, nullable=False)
    descrizione = db.Column(db.String, nullable=False)
    downlink = db.Column(db.String, nullable=False)

    def __init__(self, nome, descrizione, downlink):
        self.nome = nome
        self.descrizione = descrizione
        self.downlink = downlink

    def __repr__(self):
        return "{}-{}".format(self.pid, self.nome)


def login(email, password):
    user = User.query.filter_by(email=email).first()
    try:
        return bcrypt.checkpw(bytes(password, encoding="utf-8"), user.password)
    except AttributeError:
        # Se non esiste l'Utente
        return False


def find_user(email):
    return User.query.filter_by(email=email).first()


@app.route('/')
def page_home():
    if 'username' not in session:
        return redirect(url_for('page_main'))
    else:
        session.pop('username')
        return redirect(url_for('page_main'))


@app.route('/welcome')
def page_main():
    user = find_user('username')
    return render_template("main.htm", user=user)