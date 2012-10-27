#!/usr/bin/env python
from time import sleep
import sys
import os.path
import hashlib
import getpass

try:
    import mechanize, cookielib
except ImportError:
    print "Mechanize is required"
    print "See README for instalation instructions"
    sys.exit(1)

try:
    import argparse
except ImportError:
    print "Argparse is required"
    print "See README for instructions"
    sys.exit(1)

"""

### CMS Command Line Uploader ###
Because working up until the last second is great fun.

See README for usage details, or run with --help

Disclaimer: I take no responsibility for your usage of this
            program. Please don't blindly rely on it. Double
            check your uploads.

 - Jeff Heidel 2012

"""


#######################
# User Settings
#######################

#See README for how to  set up a password file.
#Alternatively, define USERNAME = "" and PASSWORD = ""
#below if you're less picky about security.

#Recommended: Provide a password file (see README)
PASSWORD_FILE = "/passwords/cms_password"

#Not recommended: simply add your CMS username and password here
USERNAME = ""
PASSWORD = ""


#Enable to see form data (useful if something is broken)
DEBUG = False

#######################

#Argument parsing a la Argparse
ap = argparse.ArgumentParser(description='CMS command line upload utility')
ap.add_argument('--id', dest="ASSIGNMENT_ID", type=int, help=("REQUIRED: Assignment ID to upload "
        "files to. This corresponds to the assignid field in the URL of the CMS assignment page."), required=True)
ap.add_argument('filename', type=str, nargs='+', help=("List of files to upload. This must match "
        "the number and order of upload slots on the assignment page. To NOT upload to a specific "
        "slot, specify NULL as the filename for that slot."))
args = vars(ap.parse_args())

#URL settings
LOGIN_URL = "https://cms.csuglab.cornell.edu/web/auth/?action=loginview"
CMS_URL = "https://cms.csuglab.cornell.edu/web/auth/?action=assignment&assignid=%s" % str(args["ASSIGNMENT_ID"])

#parse file list
files = []
files_md5 = []

print "Checking input files..."

for f in args["filename"]:
    if f.lower() == "null":
        files.append(None)
    else:
        if not os.path.isfile(f):
            print "ERROR: %s is not a valid file." % f
            sys.exit(1)
        files.append((f,hashlib.md5(open(f).read()).hexdigest()))

#Check / set up password
if os.path.isfile(PASSWORD_FILE):
    f = open(PASSWORD_FILE).readline()
    l = f.split(":")
    if len(l) != 2:
        print "ERROR: Invalid password file. See README for proper format."
        sys.exit(1)
    USERNAME = l[0].strip()
    PASSWORD = l[1].strip()
    print "Password acquired from password file"

if len(USERNAME) == 0:
    #No credentials provided, prompt
    print "No password file was provided. See README for how to set this up"
    print "Falling back to prompt for CMS credentials..."

    #get username
    sys.stdout.write("Cornell NetID: ")
    USERNAME = sys.stdin.readline().rstrip()

    #get password
    PASSWORD = getpass.getpass()


"""
Browser Initiation
"""

# Browser
br = mechanize.Browser(factory=mechanize.RobustFactory())

# Cookie Jar
cj = cookielib.LWPCookieJar()
br.set_cookiejar(cj)

# Browser options
br.set_handle_equiv(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)

# Follows refresh 0 but not hangs on refresh > 0
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

# User-Agent (fake agent to google-chrome linux x86_64)
br.addheaders = [('User-agent','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11'),
                 ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),
                 ('Accept-Encoding', 'deflate,sdch'),
                 ('Accept-Language', 'en-US,en;q=0.8'),
                 ('Accept-Charset', 'ISO-8859-1,utf-8;q=0.7,*;q=0.3')]

"""
Log into CMS
"""
print "Logging on to CMS..."

# The site we will navigate into
br.open(LOGIN_URL)

# Go though all the forms (for debugging only)
if DEBUG:
    print "Login Forms detected:"
    for f in br.forms():
        print f

print "Inserting login data"
br.select_form(nr=0)

br.form["netid"] = USERNAME
br.form["password"] = PASSWORD

br.submit()

pageresp = br.response().read()

if "Course Management System" not in pageresp: #XXX: This validation will break whenever CMS changes their page text
    print "### ERROR: Unable to log in! Check your user credentials."
    sys.exit(1)

print "CMS login successful!"


"""
Access assignment
"""

print "Accessing CMS assignment %d..." % args["ASSIGNMENT_ID"]

br.open(CMS_URL)

if DEBUG:
    print "CMS Page Forms detected:"
    for f in br.forms():
        print f

try:
    #Select data submission form
    br.select_form(nr=0)
except:
    print "### ERROR: Unable to access assignment. Perhaps you don't have access? Verify your Assignment ID is correct."
    sys.exit(1)

#Find all file upload boxes
uploads = filter(lambda x: x.type=='file', br.form.controls)

if len(uploads) != len(files):
    print "### ERROR: Invalid number of files provided."
    print "The number of files provided must equal the number of"
    print "files that the assignment requests. You can choose"
    print "not to upload a file by specififying NULL."
    print "See --help for details."
    sys.exit(1)

#Attach all files
for (fl, field) in zip(files, uploads):

    if fl is None:
        continue

    (filename, _) = fl

    #Add the file to the field
    print "Attaching \"%s\"..." % filename
    field.add_file(open(filename), None, filename)

#Submit to CMS!
br.submit()

print "File Upload Complete!"

pageresp = br.response().read()

#Test for MD5s on response page
files_good = True
for fl in files:
    if fl is not None:
        (fn, hsh) = fl
        if hsh not in pageresp:
            print "### ERROR: File \"%s\" (md5 %s) was not uploaded." % (fn, hsh)
            files_good = False

if not files_good:
    print "One or more files failed to upload."
    sys.exit(1)
else:
    print "Checksums verified. File upload successful."

sys.exit(0)
