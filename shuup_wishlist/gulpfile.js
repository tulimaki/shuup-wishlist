var gulp = require("gulp");
var less = require("gulp-less");
var concat = require("gulp-concat");
var uglify = require("gulp-uglify-es").default;
var plumber = require("gulp-plumber");
var minifycss = require("gulp-cssnano");
var gutil = require("gulp-util");
var PRODUCTION = gutil.env.production || process.env.NODE_ENV === "production";

gulp.task("js", function() {
    return gulp.src([
        "static_src/js/lib.js",
        "static_src/js/script.js",
    ])
        .pipe(plumber({}))
        .pipe(concat("scripts.js"))
        .pipe((PRODUCTION ? uglify() : gutil.noop()))
        .pipe(gulp.dest("static/shuup_wishlist/js/"));
});

gulp.task("js:watch", gulp.parallel(["js"]), function() {
    gulp.watch(["static_src/js/**/*.js"], ["js"]);
});

gulp.task("less", function() {
    return gulp.src([
        "static_src/less/style.less"
    ])
        .pipe(plumber({}))
        .pipe(less().on("error", function(err) {
            console.log(err.message);  // eslint-disable-line no-console
            this.emit("end");
        }))
        .pipe(concat("style.css"))
        .pipe((PRODUCTION ? minifycss() : gutil.noop()))
        .pipe(gulp.dest("static/shuup_wishlist/css/"));
});

gulp.task("less:watch", gulp.parallel(["less"]), function() {
    gulp.watch(["static_src/less/**/*.less"], ["less"]);
});

gulp.task("default", gulp.parallel(["js", "less"]));
gulp.task("watch", gulp.parallel(["js:watch", "less:watch"]));
