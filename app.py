from flask import Flask, render_template, request, url_for, redirect
from flask_cors import CORS
from chess import main
from time import sleep
import json

app = Flask(__name__)
CORS(app)

config = None
chess_game = None

is_first_human = False
is_second_human = False
is_first_moving = True


def get_game_state(chess_game):
    state = chess_game.render()

    for row in state:
        for index, cell in enumerate(row):
            if cell != "":
                row[index] = f'assets/{cell}.png'
            else:
                row[index] = 'assets/blank.png'
    logs = chess_game.logs

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
    global is_first_moving

    chess_game = main.get_chess_game(config)
    is_first_moving = chess_game.is_current_player_white()

    (state, logs) = get_game_state(chess_game)
    return render_template('game.html', initial_state=state, logs=logs, is_first_moving=is_first_moving, is_first_human=is_first_human, is_second_human=is_second_human)


@app.route('/over')
def game_over():
    return render_template('game-over.html', winning_player='Player', winning_color='Black')

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
    global is_first_human
    global is_second_human

    config = request.get_json()

    print(config)
    if config['game-type'] == 0:
        is_first_human = False
        is_second_human = False
    elif config['game-type'] == 1:
        is_first_human = True
        is_second_human = False
    elif config['game-type'] == 2:
        is_first_human = True
        is_second_human = True
    return ""


@app.route('/api/move', methods=['POST'])
def move():
    global chess_game
    global is_first_moving

    body = request.get_json()
    if is_first_moving and not is_first_human or not is_first_moving and not is_second_human:
        chess_game.minimax_root(depth=2)
    else:
        chess_game.move(int(body['initialRow']), int(body['initialColumn']), int(
            body['targetRow']), int(body['targetColumn']))

    is_first_moving = chess_game.is_current_player_white()
    (state, logs) = get_game_state(chess_game)
    is_finished = chess_game.has_finished()

    if is_finished != 2:
        return render_template('game.html', initial_state=state, logs=logs, is_first_moving=is_first_moving, is_first_human=is_first_human, is_second_human=is_second_human)
    else:
        sleep(2)
        return render_template('game-over.html', winning_player="Player", winning_color="Black")


@app.after_request
def set_response_headers(response):
    response.headers['Cache-Control'] = 'no-cache'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response


if __name__ == "__main__":
    app.run(host='127.0.0.1', debug=True)
