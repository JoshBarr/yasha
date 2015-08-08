import Lightbox from './Lightbox';


class ImageLightbox extends Lightbox  {
    constructor(options) {
        super();
        this.src = options.src;
        this.show();
        this.contentNode.className += ' modal__image';
    }

    componentDidMount() {
        var imageEl = document.createElement('img');
        var innerDiv = document.createElement('div');

        imageEl.setAttribute('src', this.src);

        imageEl.className = 'modal__image-actual';
        innerDiv.className = 'modal__image-wrapper';

        this.el.classList.add('modal-image')

        innerDiv.appendChild(imageEl);
        this.contentNode.appendChild(innerDiv);
        this.imageEl = imageEl;
    }

    renderContent() {

    }

    componentWillUnmount() {

    }
}


export default ImageLightbox;
