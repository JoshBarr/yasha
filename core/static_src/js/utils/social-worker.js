export function createYoutubePlayer(videoId, options) {
    var src = 'https://www.youtube.com/embed/' + videoId + "?";
    var playerElement = document.createElement('iframe');
    var queryString = [];
    var params = {
        enablejsapi: 1,
        origin: window.location.origin
    };

    playerElement.className = 'modal__video-wrapper';
    playerElement.setAttribute('frameborder', 0);
    playerElement.setAttribute('allowfullscreen', 1);
    playerElement.setAttribute('title', 'YouTube video player');
    playerElement.setAttribute('width', options.width);
    playerElement.setAttribute('height', options.height);

    var extraVars = options.playerVars;

    // Extend the params object
    if (extraVars) {
        for (var opt in extraVars) {
            if (extraVars.hasOwnProperty(opt)) {
                params[opt] = extraVars[opt];
            }
        }
    }

    for (var key in params) {
        var str = key + '=' + params[key];
        queryString.push(str);
    }

    playerElement.setAttribute('src', src + queryString.join("&"));
    return playerElement;
}


// Very basic facebook link sharing
export function buildFacebookLink(url) {
    var str = "//www.facebook.com/sharer/sharer.php?u=";
    str.push(encodeURIComponent(url));
    return str.join('');
}

// Extremely simple twitter sharing
export function buildTwitterLink(message, url) {
    var str = ['https://twitter.com/intent/tweet/?'];
    str.push('text=' + encodeURIComponent(message))
    str.push('url=' + encodeURIComponent(url))
    return str.join('&');
}

