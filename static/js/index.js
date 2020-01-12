function addInitialState(tag) {
    const elements = $(`.choice.${tag}`);
    const firstEl = elements.first();
    firstEl.addClass('selected');
    info[tag] = firstEl.attr('id');

    elements.click(function (e) {
        e.preventDefault();

        elements.removeClass('selected');
        $(this).addClass('selected');

        const text = $(this).attr('id');
        info[tag] = text;
        console.log(info);
    });
};

function runGame() {
    const postObj = {};

    Object.keys(info).forEach((key) => {
        postObj[key] = idMapping[info[key]];
    });
    postObj['ai-type2'] = -1;

    request('/api/sendConfiguration', 'POST', postObj)
        .done(() => {
            window.location.href='/game';
        });
};

const idMapping = {
    'classic': 0,
    'weak': 1,
    'endgame': 2,

    'cvc': 0,
    'pvc': 1,
    'pvp': 2,

    'minimax': 0,
    'reinforcement': 1
};

const info = {};
const tags = ['rule', 'game-type', 'ai-type'];

$(document).ready(() => {
    tags.forEach((t) => {
        addInitialState(t);
    });
});