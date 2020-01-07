var validMovesShowing = false;
var currentlyAvailableCells = []
var currentlySelectedPiece;
const sound = 'chess_piece_sound.wav';

const chessPieceSound = new Audio('static/assets/' + sound);
async function getValidMoves(row, column) {
    var rows, columns;
    var cells = []

    data = await request('/api/availableMoves', 'POST', { 'row': row, 'column': column });
    jdata = JSON.parse(data);
    rows = jdata.rows;
    columns = jdata.columns;

    rows.forEach((value, index) => {
        cells.push([value, columns[index]]);
    })
    return cells;
}

function sendMoveRequest(initialRow, initialColumn, targetRow, targetColumn) {
    request('/api/move', 'POST', { 'initialRow': initialRow, 'initialColumn': initialColumn, 'targetRow': targetRow, 'targetColumn': targetColumn })
        .done((view) => {
            render(view);
            chessPieceSound.play();
        });
}

function getPlayerColor() {
    // $('player-one-display')
    return $('.player-color').first().html().toLowerCase().slice(0, -1);
}

function getCellImageName(row, column) {
    let cellIndex = `#cell${row}${column}`;
    let imageFullPath = $(cellIndex).children().first().attr('src');
    let tokens = imageFullPath.split('/')
    let imageNameAndExtension = tokens[tokens.length - 1]
    return imageNameAndExtension.split('.')[0]
}

function doesOwnPiece(row, column) {
    let playerColor = getPlayerColor()
    let imageName = getCellImageName(row, column)
    let imageColor = imageName.split('-')[1];
    if (imageColor == playerColor) {
        return true;
    }
    return false;
}


function makeCellAvailable(id) {
    $(id).removeClass("cell").addClass("available-cell");
    currentlyAvailableCells.push(id);
}

function makeCellUnavailable(id) {
    $(id).removeClass("available-cell").addClass("cell");
}

function isPlayerTurn() {
    if (!$('.player-one-display').first().hasClass('player-one-moves')) {
        return false;
    }

    if ($('.player-text').first().html() != 'Player') {
        return false;
    }

    return true;
}

async function userPressed(row, column) {
    if (validMovesShowing == false) {
        if (doesOwnPiece(row, column)) {
            validMoves = await getValidMoves(row, column);
            currentlySelectedPiece = `#cell${row}${column}`;
            validMoves.push([row, column]);
            validMoves.forEach(element => {
                let row = element[0];
                let column = element[1];
                let id = `#cell${row}${column}`;
                makeCellAvailable(id);
            });
            // console.log(currentlyAvailableCells)
            currentlyAvailableCells.pop();
            validMoves.pop();
            validMovesShowing = true;
        }
    } else {
        var moving = false;
        var targetID;

        currentlyAvailableCells.forEach((value) => {
            if (`#cell${row}${column}` == value) {
                targetID = value
                moving = true
            }
        });

        if (moving == true) {
            //TO-DO: implement dynamically moving a piece
            sendMoveRequest(currentlySelectedPiece[5], currentlySelectedPiece[6], targetID[5], targetID[6])
        } else {
            currentlyAvailableCells.forEach((value) => {
                makeCellUnavailable(value);
            });
            currentlyAvailableCells = [];
            $(currentlySelectedPiece).removeClass("available-cell").addClass("cell");
            currentlySelectedPiece = "";
            validMovesShowing = false;
        }
        currentlyAvailableCells = []
    }

}

$(document).on('render', () => {
    if (isPlayerTurn()) {
        $('.cell').each(function () {
            $(this).click(() => {
                var cellId = $(this).attr('id');
                cellNumber = cellId.substr(cellId.length - 1);
                cellId = cellId.slice(0, -1);
                rowNumber = cellId.substr(cellId.length - 1);
                userPressed(rowNumber, cellNumber);
            })
        });
    }

    validMovesShowing = false;
});

$(document).ready(() => {
    document.dispatchEvent(renderEvent);
});