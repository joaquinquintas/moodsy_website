Moodsy website
==============

This is the website for moodsy.me.
To set up a dev environment, run:

    npm install

To build the website run:

    grunt build

If you want to serve changes locally and automatically recompile/update file
when they're modified run:

    grunt serve

Testing /m/SHORT_ID
-------------------

Since this page runs a script that fetches data based on it's URL, testing is
non-trivial. You'll have to move/copy `/m/base` to `/m/WPCFZAM6QB` (for
example), and then use that one for testing.

Please make sure you restore this before committing.

A better framework will be devised in future.

Copyright © 2015, Moodsy LLC <contact@moodsy.me>
