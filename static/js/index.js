function cleanAiStrategies() {
    info['ai-type'] = -1;
    info['second-ai-type'] = -1;
};

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
    });

    if (tag === 'game-type') {
        $('.strategy').css('display', 'none');
        elements.click(function (e) {
            e.preventDefault();

            const strategies = $('.strategy');
            const ai = $(`.choice.ai-type`);

            strategies.css('display', 'none');
            cleanAiStrategies();

            if (info[tag] === 'pvc') {
                strategies.first().css('display', 'block');
                info['ai-type'] = ai.first().attr('id');
            } else if (info[tag] === 'cvc') {
                strategies.css('display', 'block');
                info['ai-type'] = ai.first().attr('id');
                info['second-ai-type'] = ai.first().attr('id');
            }
        });
    }
};

function runGame() {
    const postObj = {};

    Object.keys(info).forEach((key) => {
        if (info[key] !== -1) {
            postObj[key] = idMapping[info[key]];
        } else {
            postObj[key] = -1;
        }
    });

    request('/api/sendConfiguration', 'POST', postObj)
        .done(() => {
            window.location.href = '/game';
        });
};

const idMapping = {
    'classic': 0,
    'weak': 1,
    'endgame': 2,

    'pvp': 0,
    'pvc': 1,
    'cvc': 2,

    'minimax': 0,
    'reinforcement': 1,
    'alpha-beta': 2
};

const info = {};
const tags = ['rule', 'game-type', 'ai-type', 'second-ai-type'];

$(document).ready(() => {
    tags.forEach((t) => {
        addInitialState(t);
        cleanAiStrategies();
    });
});