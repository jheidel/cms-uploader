cms-uploader
========

This application allows you to upload an assignment to Cornell CMS (Course Management System) through the command line,
allowing for much faster uploads. This means you can submit work closer to the
assignment deadline, and can spend less time fiddling around with files.

The usual disclaimer:
```
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
```
Please be careful using this software. Double check your uploads.

Also, please take it easy on the CMS servers.

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

First, go to CMS in your browser and find your assignment. Notice the URL, for instance:

https://cms.csuglab.cornell.edu/web/auth/?action=assignment&assignid=1089

This URL contains an *assignid* field, in this example, __1089__.
We need to pass this ID to cms-uploader so the files can be uploaded to the correct assignment.


### Uploading a Single File
Suppose you want to upload the file `project3_submit.zip` to assignment ID __1089__.
Moreover, this assignment expects one file (there is one upload box).

```bash
./cms-uploader.py --id=1089 project3_submit.zip
```

### Uploading Multiple Files
Suppose you want to upload the files `code.c` and `code.h` to assignment ID __1089__.
Moreover, this assignment expects two files (there are two upload boxes), and
they are ordered such that `code.c` is the first box and `code.h` is the second.

```bash
./cms-uploader.py --id=1089 code.c code.h
```

_Note: the order you specify files is the order they are uploaded to the respective
boxes._

### Uploading only some files
Suppose you want to upload the file `midpoint_check.zip` to assignment ID __1073__.
Moreover, this assignment expects two files (there are two upload boxes), and
they are ordered such that `midpoint_submission.zip` is the first box and `final_submission.zip` is the second.

```bash
./cms-uploader.py --id=1073 midpoint_check.zip NULL
```
Notice that we replace the second file with NULL. The number of files specified must match up with the
number of files that the assignment expects. If we do not want to upload any of these files,
we can use NULL to indicate which files to omit from the upload.

A Fun Little Script
-------------------

Here's a bash script that automatically packs and uploads a typical git project every minute.
(Useful for those last minute bug-fixes).

If you're really awesome, you can modify this script to take advantage of git hooks to 
have your server automatically pack and submit the code whenever anyone pushes a change.

Please be careful if you decide to use this script. I hold no responsibility
for its correctness.

Assuming the following hierarchy for this script (and that cms-uploader.py is placed in your working PATH):

 * git-project-directory/
  * .git/
  * .gitignore
  * code.h
  * code.c
 * documentation/
  * documentation.tex


``` bash
#!/bin/sh

PROJECT_DIR="git-project-directory"
ZIP_FILE="project3_submit.zip" #zip file name to upload to CMS
ASSIGNMENT_ID=1089 #ID of the CMS assignment (see Basic Usage)
PERIOD=60 #time in seconds between uploads

#Time to stop uploading
STOP_HOUR=23 #24 hour time
STOP_MINUTE=55
#Known bug: Don't expect 12:05 AM to be after 11:59 PM.
#Stop condition is met when both the hour and minute
#exceeds the given stop hour and minute.

while :
do
    #Check for stop condition
    CUR_HOUR=`date +%H`
    CUR_MIN=`date +%M`
    if [ $CUR_HOUR -ge $STOP_HOUR -a $CUR_MIN -ge $STOP_MINUTE ]; then
        echo "----"
        echo "Deadline! Stopping upload."
        exit 0
    fi

    echo "--- Starting pack and upload"

    #Remove any existing zip files
    rm $ZIP_FILE

    #Archive git project
    cd $PROJECT_DIR
    git archive --format=zip -o ../$ZIP_FILE master
    cd ..

    #Delete any superfluous files from project zip
    zip -d $ZIP_FILE .gitignore

    #Generate new documentation pdf and add to zip
    cd documentation
    pdflatex documentation.tex
    zip -9 ../$ZIP_FILE documentation.pdf #add documenation to zip
    cd ..

    #Upload to CMS!
    cms-uploader.py --id=$ASSIGNMENT_ID $ZIP_FILE

    #Sleep until next iteration
    echo "Sleeping until next iteration"
    sleep $PERIOD

done
```
