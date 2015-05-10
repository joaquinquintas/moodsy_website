Moodsy website
==============

This is the website for moodsy.me.

Development is split in two:

Templates and CSS files are generated at development/deployment time from jade
and SCSS files.

These templates are used at runtime by tornado to serve pages to users.

Development
-----------

To set up a development environment, run:

    npm install
    virtualenv env

To build the website, run:

    grunt build

To serve the website, run

    python moodsy_www/main.py

If you intend to alter the templates while testing locally, you should run
tornado, and then run grunt in serve mode, so it automatically recompiles and
updates files as you modify them:

    grunt serve

Make sure tornado is running in development mode so that it picks up any
changes to python code.

Deploying
---------

Deploying requires running `grunt build` and uploading the build static files
plus the tornado application.
You'll need to set up the virtualenv on the production server, though you will
not need npm or grunt.

Copyright © 2015, Moodsy LLC <contact@moodsy.me>
