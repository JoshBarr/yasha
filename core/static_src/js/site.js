'use strict';

class Site {
    constructor() {

    }
}

if ('addEventListener' in window\
    && 'querySelectorAll' in document\
    && 'XMLHttpRequest' in window) {
    var site = new Site();
}
