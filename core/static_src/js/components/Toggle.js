import { querySelectArray, whichAnimationEvent } from '../utils';


// This class describes the target of a toggle action
export class ToggleTarget {
    constructor(options) {
        this.el = options.el;
        this.name = this.el.getAttribute('data-toggle');
        this.animated = this.el.getAttribute('data-toggle-animated');
        this.bodyClose = this.el.getAttribute('data-toggle-body');
        this.store = options.store;
        this.handleToggle = this.handleToggle.bind(this);
        this.handleClick = this.handleClick.bind(this);
        this.handleBody = this.handleBody.bind(this);
        this.onAnimEnd = this.onAnimEnd.bind(this);
        this.onAnimIn = this.onAnimIn.bind(this);
        this.animEvent = whichAnimationEvent();
        this.store.on('toggle', this.handleToggle);
    }

    handleClick(e) {
        e.stopPropagation();
    }

    handleBody(e) {
        this.store.toggle(this.name);
        this.removeListeners();
    }

    removeListeners() {
        if (this.bodyClose) {
            document.body.removeEventListener('click', this.handleBody, false);
            this.el.removeEventListener('click', this.handleClick, false);
        }
    }

    addListeners() {
        if (this.bodyClose) {
            this.el.addEventListener('click', this.handleClick, false);
            document.body.addEventListener('click', this.handleBody, false);
        }
    }


    onAnimIn(e) {
        this.el.removeEventListener(this.animEvent, this.onAnimIn, false);
        this.el.classList.remove('u-hide');
    }

    handleToggle(data) {
        if (data.name !== this.name) {
            return;
        }

        if (data.open) {
            if (this.animated && this.animEvent) {
                this.el.addEventListener(this.animEvent, this.onAnimIn, false);
            }

            this.el.classList.remove('u-hide');
            this.el.classList.remove('-out');
            this.addListeners();

        } else {
            if (this.animated && this.animEvent) {
                this.el.addEventListener(this.animEvent, this.onAnimEnd, false);
                this.el.classList.add('-out');
            } else {
                this.el.classList.add('u-hide');
                this.removeListeners();
            }
        }
    }

    onAnimEnd(e) {
        if (e.srcElement !== this.el) {
            return;
        }

        this.removeListeners();
        this.el.removeEventListener(this.animEvent, this.onAnimEnd);
        this.el.classList.add('u-hide');
        this.el.classList.remove('-out');
    }
}

// This class is for the affordance that does the toggling. It just updates
// some state on the store object.
export class Toggle {
    constructor(options) {
        this.affordance = options.el;
        this.targetName = this.affordance.getAttribute('data-toggle-affordance');
        this.store = options.store;
        this.toggle = this.toggle.bind(this);
        this.affordance.addEventListener('click', this.toggle, false);
    }

    toggle(e) {
        e.preventDefault();
        e.stopPropagation();
        this.store.toggle(this.targetName);
    }
}
