cms-uploader
========

This application allows you to upload an assignment to CMS through the command line, 
allowing for much faster uploads. This means you can submit work closer to the 
assignment deadline, and can spend less time fiddling around with files.

Dependencies
--------------------
The following dependencies are *required* to use the cms-uploader. Install these first.

### Mechanize

Mechanize is a headless web browser that allows for programatic browsing of the web.
This is used to enumate a users's clicks through the CMS system.

[Installation Link](http://wwwsearch.sourceforge.net/mechanize/download.html)

Download, extract, and install just like any other python library using: 
``` python setup.py install ```

### Argparse
Argparse is an command line argument parser for python. It comes preinstalled in recent versions
of python. If you do not have it, see:

[Installation Link](http://pypi.python.org/pypi/argparse)

Download, extract, and install just like any other python library using: 
``` python setup.py install ```


Configuration
-------------

cms-uploader needs your Cornell netid and password in order to log into CMS.

There are three ways to do this.

 1. Change nothing. When you run cms-uploader, you will be prompted.
 2. Generate a password file and specify it in cms-uploader.py
 3. Add your netid and password to cms-uploader.py *(BAD PRACTICE)*

### Creating a password file

Create a new file on your system with your netid and password in the
following format (on a single line):
```
jeh295:password
```
Let's suppose this file is saved to `/passwords/cms_password`

You should now change the permissions on this file to secure it from prying eyes:
```
chmod 400 /passwords/cms_password
```

Finally, change cms-uploader.py's `PASSWORD_FILE` variable to point to this password file.
__NOTE__: If you intend to use cms-uploader in your path, you should use an absolute
path here.

Basic Usage
-----------

You can also run `./cms-uploader.py --help` to get info about usage.



A Fun Script
------------

Assuming the following hierarchy

 > git-project-directory
 > > .git
 > > code.h
 > > code.c
 > documentation
 > > documentation.tex
 > > documentation.pdf


``` bash
#!/bin/bash
```
