var gulp = require("gulp");
var concat = require("gulp-concat");
var uglify = require("gulp-uglify");
var plumber = require("gulp-plumber");
var gutil = require("gulp-util");
var PRODUCTION = gutil.env.production || process.env.NODE_ENV === "production";

gulp.task("js", function() {
    return gulp.src([
        "static_src/js/flash_message.js",
        "static_src/js/lib.js",
        "static_src/js/script.js",
    ])
        .pipe(plumber({}))
        .pipe(concat("scripts.js"))
        .pipe((PRODUCTION ? uglify() : gutil.noop()))
        .pipe(gulp.dest("static/shuup_wishlist/js/"));
});

gulp.task("js:watch", ["js"], function() {
    gulp.watch(["static_src/js/**/*.js"], ["js"]);
});

gulp.task("default", ["js"]);

gulp.task("watch", ["js:watch", "less:watch"]);
