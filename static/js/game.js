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
    if ($('.player-one-display').first().hasClass('player-one-moves')) {
        console.log("x")
        return $('.player-one-color').first().html().toLowerCase().slice(0, -1);
    }
    else {
        return $('.player-two-color').first().html().toLowerCase().slice(0, -1);
    }

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
    console.log(playerColor, imageColor)
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
    $('.cell').each(function () {
        $(this).click(() => {
            var cellId = $(this).attr('id');
            cellNumber = cellId.substr(cellId.length - 1);
            cellId = cellId.slice(0, -1);
            rowNumber = cellId.substr(cellId.length - 1);
            userPressed(rowNumber, cellNumber);
        })
    });

    validMovesShowing = false;
});

$(document).ready(() => {
    document.dispatchEvent(renderEvent);
});