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

    rsync:
      options:
        recursive: true
      static:
        options:
          src: 'build/static/'
          dest: '/var/www/python/moodsy.me/static/'
          host: 'root@moodsy.me'  # FIXME: not-root!
          delete: true
      templates:
        options:
          src: 'build/'  # FIXME: build/templates
          dest: '/var/www/python/moodsy.me/templates/'
          host: 'root@moodsy.me'
          delete: true
      python:
        options:
          src: 'moodsy_www/'
          dest: '/var/www/python/moodsy.me/moodsy_www/'
          host: 'root@moodsy.me'
          delete: false



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
  grunt.registerTask "deploy", "Deploy all files to production", [
    "build"
    "rsync:templates"
    "rsync:static"
    "rsync:python"
  ]
