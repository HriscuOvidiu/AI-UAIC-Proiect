from flask import Flask, render_template, request
from flask_cors import CORS
from chess import chess

app = Flask(__name__)
CORS(app)

##
# Front-end routes
##


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/game')
def game():

    state = chess.get_board()
    print(state)
    for row in state:
        for index, cell in enumerate(row):
            if cell != "":
                row[index] = f'assets/{cell}.png'
            else:
                row[index] = 'assets/blank.png'

    print(state)

    return render_template('game.html', initial_state=state)

##
# API
##


@app.route('/api/availableMoves', methods=['GET', 'POST'])
def availableMoves():
    print(request.get_json())
    return "<h1>Hello</h1>"


@app.route('/api/move', methods=['POST'])
def move():
    pass


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
