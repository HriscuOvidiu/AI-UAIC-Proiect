from flask import Flask, render_template, request
from flask_cors import CORS
from chess import main
import json

app = Flask(__name__)
CORS(app)

config = None
chess_game = None

is_first_moving = True


def get_game_state(chess_game):
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

    return state, logs

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

    (state, logs) = get_game_state(chess_game)

    return render_template('game.html', initial_state=state, logs=logs, is_first_moving=is_first_moving)

##
# API
##


@app.route('/api/availableMoves', methods=['GET', 'POST'])
def availableMoves():
    global chess_game

    request_row = request.get_json()['row']
    request_column = request.get_json()['column']
    rows, columns = main.positions_to_frontend(
        chess_game, int(request_row), int(request_column))
    moves = {"rows": rows, "columns": columns}
    return json.dumps(moves)


@app.route('/api/sendConfiguration', methods=['GET', 'POST'])
def sendConfiguration():
    global config
    config = request.get_json()
    return ""


@app.route('/api/move', methods=['POST'])
def move():
    global chess_game
    global is_first_moving

    body = request.get_json()
    print(body)
    chess_game.move(int(body['initialRow']), int(body['initialColumn']), int(
        body['targetRow']), int(body['targetColumn']))

    print(is_first_moving)
    (state, logs) = get_game_state(chess_game)
    # is_first_moving = not is_first_moving
    # print(is_first_moving)
    return render_template('game.html', initial_state=state, logs=logs, is_first_moving=is_first_moving)


@app.after_request
def set_response_headers(response):
    response.headers['Cache-Control'] = 'no-cache'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response


if __name__ == "__main__":
    app.run(host='127.0.0.1', debug=True)
