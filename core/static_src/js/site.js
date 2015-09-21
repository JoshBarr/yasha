const cut     = 'addEventListener' in window;
const the     = 'querySelectorAll' in document;
const mustard = 'XMLHttpRequest'   in window;

class Site {
    constructor() {

    }
}


if (cut && the && mustard) {
    const site = new Site();
}
