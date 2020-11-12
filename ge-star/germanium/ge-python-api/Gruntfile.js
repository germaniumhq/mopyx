/**
 * Grunt project configuration.
 */
module.exports = function(grunt) {
    // configuration for the plugins.
    grunt.initConfig({
        concat: {
            options: {
                sourceMap: false
            },
            "impl/filter-not-displayed" : {
                files: [{
                    src: ["js/impl/filter-not-displayed.js"],
                    dest: "germanium/impl/filter-not-displayed.js"
                }]
            },
            "locators/positional-filter" : {
                files: [{
                    src: ["js/locators/positional-filter.js"],
                    dest: "germanium/locators/positional-filter.js"
                }]
            },
            "locators/inside-filter" : {
                files: [{
                    src: ["js/locators/inside-filter.js"],
                    dest: "germanium/locators/inside-filter.js"
                }]
            },
            "locators/text" : {
                files: [{
                    src: ["js/locators/text.js"],
                    dest: "germanium/locators/text.js"
                }]
            },
            "util/child-nodes" : {
                files: [{
                    src: ["js/util/child-nodes.js"],
                    dest: "germanium/util/child-nodes.js"
                }]
            },
            "util/get-attributes" : {
                files: [{
                    src: ["js/util/get-attributes.js"],
                    dest: "germanium/util/get-attributes.js"
                }]
            },
            "util/get-style" : {
                files: [{
                    src: ["js/util/get-style.js"],
                    dest: "germanium/util/get-style.js"
                }]
            },
            "points/box" : {
                files: [{
                    src: ["js/points/box.js"],
                    dest: "germanium/points/box.js"
                }]
            }
        },

        uglify: {
            options: {
                bare_returns: true,
                mangle: true,
                compress: true
            },
            "impl/filter-not-displayed" : {
                files: {
                    "germanium/impl/filter-not-displayed.min.js" : [
                        "germanium/impl/filter-not-displayed.js"
                    ]
                }
            },
            "locators/positional-filter" : {
                files: {
                    "germanium/locators/positional-filter.min.js" : [
                        "germanium/locators/positional-filter.js"
                    ]
                }
            },
            "locators/inside-filter" : {
                files: {
                    "germanium/locators/inside-filter.min.js" : [
                        "germanium/locators/inside-filter.js"
                    ]
                }
            },
            "locators/text" : {
                files: {
                    "germanium/locators/text.min.js" : [
                        "germanium/locators/text.js"
                    ]
                }
            },
            "util/child-nodes" : {
                files: {
                    "germanium/util/child-nodes.min.js" : [
                        "germanium/util/child-nodes.js"
                    ]
                }
            },
            "util/get-attributes" : {
                files: {
                    "germanium/util/get-attributes.min.js" : [
                        "germanium/util/get-attributes.js"
                    ]
                }
            },
            "util/get-style" : {
                files: {
                    "germanium/util/get-style.min.js" : [
                        "germanium/util/get-style.js"
                    ]
                }
            },
            "points/box" : {
                files: {
                    "germanium/points/box.min.js" : [
                        "germanium/points/box.js"
                    ]
                }
            }
        }
    });

    // load NPM tasks:
    // grunt.loadNpmTasks("grunt-contrib-watch");
    grunt.loadNpmTasks("grunt-contrib-concat");
    grunt.loadNpmTasks("grunt-contrib-uglify");

    // register our tasks:
    grunt.registerTask("default", ['concat', 'uglify']);
};
