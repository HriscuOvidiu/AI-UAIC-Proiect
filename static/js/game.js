function showAvailableMoves(position) {
    request('/api/availableMoves', 'POST', { position: position })
        .done((data) => {
            render(data);
        });
};

var validMovesShowing = false;
var currentlyAvailableCells = []
var currentlySelectedPiece;

function getValidMoves(row, column) {
    return [[0, 3], [5, 5]];
}

function getPlayerColor() {
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


function userPressed(row, column) {
    if (validMovesShowing == false) {
        if (doesOwnPiece(row, column)) {
            validMoves = getValidMoves(row, column);
            currentlySelectedPiece = `#cell${row}${column}`;
            validMoves.push([row, column])
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

    }
    else {
        var moving = false;
        currentlyAvailableCells.forEach((value, index, array) => {
            if (`#cell${row}${column}` == value) {
                moving = true
            }
        })

        if (moving == true) {
            //TO-DO: implement dynamically moving a piece
            console.log('Moving');
        }

        else {
            currentlyAvailableCells.forEach((value, index, array) => {
                makeCellUnavailable(value);
            })
            currentlyAvailableCells = []
            $(currentlySelectedPiece).removeClass("available-cell").addClass("cell");
            currentlySelectedPiece = "";
            validMovesShowing = false;
        }
    }

}

$(document).ready(() => {
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
});