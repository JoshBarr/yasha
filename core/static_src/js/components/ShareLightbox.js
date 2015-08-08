import Lightbox from './Lightbox';
import utils from '../utils/social-worker';


export class SocialShareLightbox extends Lightbox {
    constructor(options) {
        super(options)
        this.url = options.url;

        if (!this.url) {
            return;
        }

        this.show();
    }

    componentDidMount() {
        var innerDiv = document.createElement('div');
        var html = ['<h3>Share this</h3>'];
        var facebookLink = utils.buildFacebookLink(this.url);
        var twitterLink = utils.buildTwitterLink('Check this out', this.url);

        html.push("<p><a href='" + facebookLink + "' class='icon-text btn-primary btn-icon'><svg><use xlink:href='#twitter'></svg><span>Share on Twitter</span></a></p>")
        html.push("<p><a href='" + twitterLink + "' class='icon-text btn-primary btn-icon'><svg><use xlink:href='#social-facebook'></svg><span>Share on Facebook</span></a></p>")
        innerDiv.innerHTML = html.join('\n');

        this.contentNode.appendChild(innerDiv);
    }

    componentWillUnmount() {

    }
}


export class ShareButton {
    constructor(options) {
        this.el = options.el;
        this.handleClick = this.handleClick.bind('this');
        this.el.addEventListener('click', this.handleClick, false);
    }

    handleClick(e) {
        e.preventDefault();
        var lightbox = new SocialShareLightbox({
            url: this.el.getAttribute('data-flag-share')
        });
    }
}
