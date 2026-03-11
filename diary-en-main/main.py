# Import
from flask import Flask, render_template,request, redirect
# Importing the database library
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
# Connecting SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///diary.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Creating a DB
db = SQLAlchemy(app )

#Assignment #1. Create a DB table
class Card(db.Model):
    title = db.Column(db.String(100), nullable=False)
    id = db.Column(db.Integer, primary_key=True)
    subtitle = db.Column(db.String(100), nullable=False)
    text = db.Column(db.String, nullable=False)
    
    def __repr__(self):
        return f'<Card {self.id}>'











# Running the page with content
@app.route('/')
def index():
    # Displaying the DB objects
    # Assignment #2. Display the objects from the DB in index.html
    cards = Card.query.order_by(Card.id).all()

    return render_template('index.html',
                           cards = cards

                           )

# Running the page with the card
@app.route('/card/<int:id>')
def card(id):
    # Assignment #2. Display the right card by its id
    

    return render_template('card.html', card=card)

# Running the page and creating the card
@app.route('/create')
def create():
    return render_template('create_card.html')

# The card form
@app.route('/form_create', methods=['GET','POST'])
def form_create():
    if request.method == 'POST':
        title =  request.form['title']
        subtitle =  request.form['subtitle']
        text =  request.form['text']

        # Assignment #2. Create a way to store data in the DB
        card = Card(title=title, subtitle=subtitle, text=text)
        db.session.add(card)
        db.session.commit()




        return redirect('/')
    else:
        return render_template('create_card.html')


if __name__ == "__main__":
    app.run(debug=True)