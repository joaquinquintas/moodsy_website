module.exports = (grunt) ->
  grunt.initConfig
    copy:
      build:
        cwd: "src"
        src: [
          "**"
          "!**/*.coffee"
          "!**/*.scss"
          "!**/*.jade"
        ]
        dest: "build"
        expand: true

    clean:
      build:
        src: ["build"]

    coffee:
      glob_to_multiple:
        expand: true
        flatten: true
        cwd: 'src'
        src: ['*.coffee']
        dest: 'build/'
        ext: '.js'
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
      scripts:
        files: ["src/**/*.coffee", "src/**/*.js"]
        tasks: ["scripts", "copy"]

      jade:
        files: "src/**/*.jade"
        tasks: ["jade", "copy"]

      sass:
        files: "src/**/*.scss"
        tasks: ["sass"]

      copy:
        files: [
          "src/**"
          "!src/**/*.coffee"
          "!src/**/*.jade"
        ]

    connect:
      server:
        options:
          port: 4000
          base: "build"
          hostname: "*"

    bowercopy:
      libs:
        options:
          destPrefix: "build"

        files:
          "moment.js": "moment/min/moment.min.js"
    sass:
      dist:
        files: [
          expand: true
          cwd: "src"
          src: ["**/*.scss"]
          dest: "build"
          ext: ".css"
        ]


  #load tasks
  require("load-grunt-tasks") grunt

  #define tasks
  grunt.registerTask "scripts", "Compile scripts only.", ["coffee"]
  grunt.registerTask "build", "Compiles everything and copy into build.", [
    "clean"
    "copy"
    "bowercopy"
    "sass"
    "scripts"
    "jade"
  ]
  grunt.registerTask "serve", "Serve locally and update file on change.", [
    "build"
    "connect"
    "watch"
  ]
