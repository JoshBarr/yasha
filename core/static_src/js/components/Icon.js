import React, { PropTypes } from 'react';

const propTypes = {
    name: PropTypes.string.isRequired,
    title: PropTypes.string,
    cssClass: PropTypes.string,
};

const defaultProps = {
    title: '',
    cssClass: '',
};

/**
 * An icon that's rendered using inline SVG.
 */
class Icon extends React.Component {

    render() {
        const { name, title, cssClass } = this.props;
        const dangerousInnerSVG = {
            __html: `<use xlink:href="#i-${name}"/>`,
        };

        return (
            <svg
                className={`i-${name} ${cssClass}`}
                dangerouslySetInnerHTML={dangerousInnerSVG}
                title={title}
            />
        );
    }
}

Icon.propTypes = propTypes;
Icon.defaultProps = defaultProps;

export default Icon;
