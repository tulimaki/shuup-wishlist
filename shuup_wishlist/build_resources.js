const { getParcelBuildCommand, runBuildCommands } = require("shuup-static-build-tools");

runBuildCommands([
    getParcelBuildCommand({
        cacheDir: "shuup-wishlist",
        outputDir: "static/shuup_wishlist/js",
        outputFileName: "scripts",
        entryFile: "static_src/js/index.js"
    }),
    getParcelBuildCommand({
        cacheDir: "shuup-wishlist",
        outputDir: "static/shuup_wishlist/css",
        entryFile: "static_src/less/style.less"
    })
]);
