class Popup {
    constructor(selector) {
        this.selector = selector;
    }

    toggle() {
        $(this.selector).fadeToggle();
    }
}