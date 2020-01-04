function addInitialState(tag) {
    const elements = $(`.choice.${tag}`);
    elements.first().addClass('selected');
    elements.click(function(e){
        e.preventDefault();
        
        elements.removeClass('selected');       
        $(this).addClass('selected');

        const text = $(this).text();
        info[tag] = text;
        console.log(info);
    });
};

function runGame(){
    window.location.href='/game';
};

const info = {};
const tags = ['rule', 'game-type', 'ai-type'];

$(document).ready(() => {
    tags.forEach((t) => {
        addInitialState(t);
    });
});