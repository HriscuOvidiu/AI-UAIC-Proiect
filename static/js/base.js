const baseUrl = 'http://localhost:5000';
const contentType = 'application/json';
const renderEvent = new Event("render", {bubbles: true, cancelable: false});

function render(html) {
    document.body.innerHTML = html;
    document.dispatchEvent(renderEvent);
};

function request(path, method, data) {
    return $.ajax({
        type: method,
        contentType: "application/json; charset=utf-8",
        url: path,
        data: JSON.stringify(data)
    });
}