from flask import Flask, session, url_for, redirect, request, render_template, abort, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import bcrypt
import os


app = Flask(__name__)
app.secret_key = "debug-attivo"
UPLOAD_FOLDER = './upload-area'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
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
    bio = db.Column(db.String, nullable=False)

    def __init__(self, nome, cognome, titolo, ruolo, email, password, bio):
        self.nome = nome
        self.cognome = cognome
        self.titolo = titolo
        self.ruolo = ruolo
        self.email = email
        self.bio = bio
        p = bytes(password, encoding="utf-8")
        self.password = bcrypt.hashpw(p, bcrypt.gensalt())

    def __repr__(self):
        return "{}-{}".format(self.uid, self.email)


class Prodotto(db.Model):
    pid = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String, nullable=False)
    descrizione = db.Column(db.String, nullable=False)
    descrizione_breve = db.Column(db.String, nullable=False)
    downlink = db.Column(db.String, nullable=False)
    showcase = db.Column(db.Boolean, nullable=False)
    image = db.Column(db.String, nullable=False)

    def __init__(self, nome, descrizione, descrizione_breve, downlink, image):
        self.nome = nome
        self.descrizione = descrizione
        self.descrizione_breve = descrizione_breve
        self.downlink = downlink
        self.showcase = False
        self.image = image

    def __repr__(self):
        return "{}-{}".format(self.pid, self.nome)


def login(email, password):
    user = User.query.filter_by(email=email).first()
    try:
        return bcrypt.checkpw(bytes(password, encoding="utf-8"), user.password)
    except AttributeError:
        # Se non esiste l'Utente
        return False


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


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
    css = url_for("static", filename="style.css")
    user = find_user('username')
    return render_template("main.htm", user=user, css=css)


@app.route('/products')
def page_products():
    css = url_for("static", filename="style.css")
    products = Prodotto.query.all()
    return render_template("products.htm", css=css)


@app.route('/members')
def page_members():
    css = url_for("static", filename="style.css")
    users = User.query.all()
    return render_template("members.htm", users=users, css=css)


@app.route('/amministrazione', methods=["POST", "GET"])
def page_amministrazione():
    if request.method == 'GET' and 'username' in session:
        utente = find_user(session['username'])
        css = url_for("static", filename="style.css")
        return render_template("Amministrazione/amministrazione.htm", css=css, utente=utente)
    else:
        if login(request.form['username'], request.form['password']):
            session['username'] = request.form['username']
            return redirect(url_for('page_amministrazione'))
        else:
            abort(403)


@app.route('/product_add', methods=["POST", "GET"])
def page_product_add():
    if 'username' not in session:
        return abort(403)
    if request.method == 'GET':
        utente = find_user(session['username'])
        css = url_for("static", filename="style.css")
        return render_template("Amministrazione/Prodotti/product_add.htm", css=css, utente=utente)
    else:
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        prodotto = Prodotto(request.form['nome'], request.form['destesa'], request.form['dbreve'], request.form['download'], str(file.filename))
        db.session.add(prodotto)
        db.session.commit()
        return redirect(url_for('page_amministrazione'))


if __name__ == "__main__":
    # Se non esiste il database viene creato
    if not os.path.isfile("db.sqlite"):
        utente = User("Lorenzo", "Balugani", "Perito Informatico", "Programmatore", "lorenzo.balugani@gmail.com", "password", "Marmelle")
        db.create_all()
        db.session.add(utente)
        db.session.commit()
    app.run(debug=True)