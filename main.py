from flask import Flask, render_template, request, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'ihateanime'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///games.db'
db = SQLAlchemy(app)

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(10), nullable=False)
    players = db.relationship('Player', backref='game', lazy=True)

    def __repr__(self):
        return f"Game(id={self.id}, name='{self.name}', status='{self.status}')"

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    room = db.Column(db.String(255), nullable=False)
    deck = db.Column(db.String(255))
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'), nullable=False)

    def __repr__(self):
        return f"Player(id={self.id}, name='{self.name}', room='{self.room}', deck='{self.deck}', game_id={self.game_id})"


@app.route('/')
def index():
    if 'name' in session:
        return redirect(url_for('rooms'))
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    name = request.form['name']
    if len(name) > 0 and len(name) < 20 and ',' not in name:
        session['name'] = request.form['name']
        return redirect(url_for('rooms'))
    else:
        return redirect(url_for('index'))

@app.route('/rooms')
def rooms():
    return render_template('rooms.html', nickname=session['name'])

@app.route('/create_room', methods=['POST'])
def create_room():
    if 'name' not in session:
        return redirect(url_for('index'))
    
    room_name = request.form['room_name']
    game = Game(name=room_name, status="active")
    db.session.add(game)
    db.session.commit()

    return redirect(url_for('game'))

@app.route('/join_room', methods=['POST'])
def join_room():
    if 'name' not in session:
        return redirect(url_for('index'))
    
    room_id = request.form['room_id']
    game = Game.query.get(room_id)

    if game:
        return redirect(url_for('game'))
    else:
        return redirect(url_for('rooms'))

@app.route('/game')
def game():
    if 'name' not in session:
        return redirect(url_for('index'))

    

    return render_template('game.html')

if __name__ == '__main__':
    app.run(debug=True)