# Importación
from flask import Flask, render_template, request, redirect, session
# Conexión de la biblioteca de bases de datos
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
# Establecer la clave secreta para la sesión.
app.secret_key = 'my_top_secret_123'
# Connecting SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///diary.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Creando la DB
db = SQLAlchemy(app)
# Creando la tabla


class User(db.Model):
    # Estableciendo los campos de enrada
    # id
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # correo electrónico
    email = db.Column(db.String(100), nullable=False)
    # contraseña
    password = db.Column(db.String(100), nullable=False)

    # Objeto de salida y su ID
    def __repr__(self):
        return f'<User {self.id}>'

class Card(db.Model):
    # Estableciendo los campos de enrada
    # id
    id = db.Column(db.Integer, primary_key=True)
    # título
    title = db.Column(db.String(100), nullable=False)
    # Descripción
    subtitle = db.Column(db.String(300), nullable=False)
    # Texto
    text = db.Column(db.Text, nullable=False)
    # El correo electrónico del propietario de la tarjeta.
    user_email = db.Column(db.String(100), nullable=False)

    # Objeto de salida y su ID
    def __repr__(self):
        return f'<Card {self.id}>'
 

    # Objeto de salida y su ID
    def __repr__(self):
        return f'<Card {self.id}>'
    

# Tarea #1. Crear la tabla de usuarios


# Lanzamiento de la página de contenido
@app.route('/', methods=['GET','POST'])
def login():
    error = ''
    if request.method == 'POST':
        form_login = request.form['email']
        form_password = request.form['password']
        
        users_db = User.query.all()
        
        # Tarea #4. Implementar la verificación de usuario
        for user in users_db:
            if form_login == user.email and form_password == user.password:
                session['user_email'] = user.email
                return redirect('/index')
            else:
                error = 'Correo electrónico o contraseña incorrectos'
                return render_template('login.html', error=error)
     
    else:
        return render_template('login.html', error=error)



@app.route('/reg', methods=['GET','POST'])
def reg():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        # Tarea #3. Implementar grabación de usuarios
        user = User(email=email, password=password)
        db.session.add(user)
        db.session.commit()

        
        return redirect('/')
    
    else:    
        return render_template('registration.html')


# Iniciar página de contenido
@app.route('/index')
def index():
    # Tarea # 4. Asegúrese de que el usuario solo vea sus propias tarjetas
    email = session.get('user_email')
    
    cards = Card.query.filter_by(user_email=email).all()
    return render_template('index.html', cards=cards)

# Lanzando la página de la tarjeta
@app.route('/card/<int:id>')
def card(id):
    card = Card.query.get(id)

    return render_template('card.html', card=card)

# Iniciando la página de creación de tarjetas
@app.route('/create')
def create():
    return render_template('create_card.html')

# la forma de la tarjeta
@app.route('/form_create', methods=['GET','POST'])
def form_create():
    if request.method == 'POST':
        email = session['user_email']
        card = Card(
            title=request.form['title'], 
            subtitle=request.form['subtitle'], 
            text=request.form['text'], 
            user_email=email
        )

        db.session.add(card)
        db.session.commit()
        return redirect('/index')
    else:
        return render_template('create_card.html')

if __name__ == "__main__":
    app.run(debug=True)
