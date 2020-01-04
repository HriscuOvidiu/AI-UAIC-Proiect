const baseUrl = 'http://localhost:5000';
const contentType = 'application/json';

function render(html){
    document.body.innerHTML = html;
};

function request(path, method, data) {
    return $.ajax({
        type:method,
        contentType: "application/json; charset=utf-8",
        url:path,
        data: JSON.stringify(data)
    });
}