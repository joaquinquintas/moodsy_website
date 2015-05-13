Moodsy website
==============

This is the website for moodsy.me.

Development is split in two:

 * Templates and CSS files are generated at development/deployment time from jade
   and SCSS files. These files are contained in `src/`.

 * These templates are used at runtime by [tornado][tornado] to serve pages to
   users. Tornado and the rest of the python code is in `moodsy_www`. All of
   the python code is `python2` and `python3` compatible.

[tornado]: http://www.tornadoweb.org/

Development
-----------

You'll need to install [iojs][iojs] (or [nodejs][nodejs]), [npm][npm],
[grunt-cli][grunt-cli] and [python][python] (either 2.7 or 3.4).

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

[iojs]: https://iojs.org/
[nodejs]: https://nodejs.org/
[npm]: https://www.npmjs.com/
[grunt-cli]: https://github.com/gruntjs/grunt-cli
[python]: https://www.python.org/

Deploying
---------

Deploying requires running `grunt build` and uploading the build static files
plus the tornado application.
You'll need to set up the `virtualenv` on the production server (unless you
globally install the dependencies), though you will not need npm or grunt.

Copyright © 2015, Moodsy LLC <contact@moodsy.me>
