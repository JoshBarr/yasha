var gulp = require("gulp");

require("./gulp/watch");
require("./gulp/js");
require("./gulp/css");
require("./gulp/svg");

gulp.task('build', ['js', 'css', 'svg'], function(done) {
    done();
});

gulp.task('default', ['build']);
