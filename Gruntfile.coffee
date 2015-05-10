module.exports = (grunt) ->
  grunt.initConfig
    copy:
      build:
        cwd: "src"
        src: [
          "**"
          "!**/*.scss"
          "!**/*.jade"
        ]
        dest: "build/static"
        expand: true

    clean:
      build:
        src: ["build"]

    jade:
      compile:
        options:
          data: {}

        files: [
          expand: true
          cwd: "src"
          src: ["**/*.jade"]
          dest: "build"
          ext: ".html"
        ]

    watch:
      jade:
        files: "src/**/*.jade"
        tasks: ["jade", "copy"]

      sass:
        files: "src/**/*.scss"
        tasks: ["sass"]

      copy:
        files: [
          "src/**"
          "!src/**/*.jade"
        ]

    sass:
      dist:
        files: [
          expand: true
          cwd: "src"
          src: ["**/*.scss"]
          dest: "build/static"
          ext: ".css"
        ]


  #load tasks
  require("load-grunt-tasks") grunt

  #define tasks
  grunt.registerTask "build", "Compiles everything and copy into build.", [
    "clean"
    "copy"
    "sass"
    "jade"
  ]
  grunt.registerTask "serve", "Serve locally and update file on change.", [
    "build"
    "watch"
  ]
