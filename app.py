from flask import Flask, render_template, request
from flask_cors import CORS
from chess import main

app = Flask(__name__)
CORS(app)

##
# Front-end routes
##

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/game', methods=['GET', 'POST'])
def game():
    state = main.get_board()
    print(state)
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
    return "<h1>Hello</h1>"

@app.route('/api/sendConfiguration', methods=['GET', 'POST'])
def sendConfiguration():
    print(request.get_json())
    return ""

@app.route('/api/move', methods=['POST'])
def move():
    pass

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
