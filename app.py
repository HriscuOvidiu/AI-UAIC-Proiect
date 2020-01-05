from flask import Flask, render_template, request
from flask_cors import CORS
from chess import main
import json

app = Flask(__name__)
CORS(app)

config = None
chess_game = None

##
# Front-end routes
##


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/game', methods=['GET', 'POST'])
def game():
    global chess_game
    
    chess_game = main.get_chess_game(config)

    # TEST valid positions
    print(chess_game.get_valid_positions(0, 3))
    # TEST

    state = chess_game.render()
    
    for row in state:
        for index, cell in enumerate(row):
            if cell != "":
                row[index] = f'assets/{cell}.png'
            else:
                row[index] = 'assets/blank.png'
    logs = ["[23:58:11]: Player moves pawn from H2 to H3",
            "[23:58:14]: Computer moves horse from G8 to F6",
            "[23:58:11]: Player moves pawn from H2 to H3"]
    is_first_moving = True
    return render_template('game.html', initial_state=state, logs=logs, is_first_moving=is_first_moving)

##
# API
##

@app.route('/api/availableMoves', methods=['GET', 'POST'])
def availableMoves():
    print(request.get_json())
    rows = [2, 3, 4]
    columns = [2, 3, 4]
    moves = {"rows": rows, "columns": columns}
    return json.dumps(moves)

@app.route('/api/sendConfiguration', methods=['GET', 'POST'])
def sendConfiguration():
    global config
    config = request.get_json()
    return ""

@app.route('/api/move', methods=['POST'])
def move():
    pass

if __name__ == "__main__":
    app.run(host='127.0.0.1', debug=True)
