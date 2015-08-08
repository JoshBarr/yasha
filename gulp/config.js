var path = require("path");
var sourcePath = "./static_src";
var distPath = "./static";

var prod = process.env.NODE_ENV === 'production';


module.exports = {

    paths: {
        appName: "site.js",
        sass: path.join(sourcePath, "sass"),
        css: path.join(distPath, "css"),
        jsSrc: path.join(sourcePath, "js"),
        js: path.join(distPath, "js"),
        svg: path.join(sourcePath, "svg"),
        images: path.join(distPath, "images"),
        slug: "my-site",
        views: "./templates",
    },

    PlzOptions: {
        minifier: prod,
        sourcemaps: !prod,
        mqpacker: false,
        filters: false,
        rem: true,
        pseudoElements: true,
        opacity: true,
        autoprefixer: {
            browsers: ['ie 8', 'ie 9', '> 1%']
        }
    }

};
