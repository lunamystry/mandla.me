'''
Credit to Adam Presley, who's ftpsyncing fabfile I used as a starting point
http://adampresley.com/#!post/2013/04/how-i-deployed-a-php-app-via-ftp-using-fabric-and-git
'''
import fabric
import ftplib
import re
import os
from git import *
from ftplib import FTP
from fabric.api import task
from fabric.colors import *
from subprocess import Popen, PIPE


###############################################################################
# SECTION: Constants
###############################################################################
FTP_ADDRESS = ""
FTP_USER = ""
FTP_PASSWORD = ""
FTP_ROOT_DIR = "/public_html"

REPO_ROOT = "/home/leny/Projects/mandla.me/mandla.me"
DIR_FILTER = ("application/", "assets/")


###############################################################################
# SECTION: Private methods
###############################################################################
workingDir = ''

def _connectToFTP():
   global ftp

   ftp = FTP(host=FTP_ADDRESS)
   ftp.login(user=FTP_USER, passwd=FTP_PASSWORD)

   return ftp

def _cwdFTP(directory):
   global workingDir
   global ftp

   if workingDir != directory:
      print cyan('CWD %s' % directory),
      try:
         ftp.cwd(os.path.join(FTP_ROOT_DIR, directory))
         print green(u'\u2713')
         workingDir = directory
         return True
      except ftplib.error_perm as e:
         print red('>> FTP ERROR %s' % e)
         return False

def _filterThroughDirs(fileList):
   return [f for f in fileList if f.startswith(DIR_FILTER)]

def _gitLatestFiles():
   g = Git(REPO_ROOT)
   repo = Repo(REPO_ROOT)
   branch = repo.active_branch
   headCommit = repo.commit(branch)

   print "Current branch: %s" % branch
   print "Head commit revision: %s" % headCommit
   print "Message: %s" % headCommit.message

   os.chdir(REPO_ROOT)

   process = Popen("git show --name-status --diff-filter=AM",
      shell=True,
      stdout=PIPE)

   out, err = process.communicate()
   files = out.split("\n")

   regexedFiles = [f for f in files if re.match(r'^[A|M]\t', f)]
   trimmedFiles = [re.sub(r'[A|M]\t', '', f) for f in regexedFiles]

   return _filterThroughDirs(fileList=trimmedFiles)
   #return trimmedFiles

def _gitLatestDeletedFiles():
   os.chdir(REPO_ROOT)

   process = Popen("git show --name-status --diff-filter=D",
      shell=True,
      stdout=PIPE)

   out, err = process.communicate()
   files = out.split("\n")

   regexedFiles = [f for f in files if re.match(r'^D\t', f)]
   trimmedFiles = [re.sub(r'D\t', '', f) for f in regexedFiles]

   return _filterThroughDirs(fileList=trimmedFiles)
   #return trimmedFiles

def _filterOutDeleted(fileList, filter):
   return [f for f in fileList if any(f in x for x in filter)]


###############################################################################
# SECTION: Actions
###############################################################################
@task
def commit():
   local('git add -A')
   local('git commit')
   local('git push')

@task
def testftp():
   ftp = _connectToFTP()
   print cyan(FTP.getwelcome(ftp))
   ftp.quit()

@task
def dryrun():
   print ""
   print green("** Dry Running Deploy **")

   files = _gitLatestFiles()
   deleted = _gitLatestDeletedFiles()

   if len(files) > 0:
      for f in files:
         print yellow('STOR %s' % f)
   else:
      print cyan('Nothing to upload')

   if len(deleted) > 0:
      for d in deleted:
         print red('DELE %s' % d)
   else:
      print cyan('Nothing to delete')

@task
def deploy():
   print ""
   print green("** Upload latest changes **")

   ftp = _connectToFTP()
   files = _gitLatestFiles()
   deleted = _gitLatestDeletedFiles()

#Parse Uploads
   for f in files:
      split = os.path.split(f)

      if _cwdFTP(split[0]):
         print yellow('STOR %s' % f),
         try:
            ftp.storlines("STOR %s" % split[1], open(f, "r"))
            print green(u'\u2713')
         except IOError as e:
            print red('>> %s' % e.strerror)

#Parse Deletes
   for d in deleted:
      split = os.path.split(f)

      if _cwdFTP(split[0]):
         print magenta('DELE %s' % split[1]),
         try:
            ftp.delete(f)
            print green(u'\u2713')
         except ftplib.error_perm as e:
            print red('>> FTP ERROR %s' % e)

   print ""
   print green('** Closing FTP connection **')
   ftp.quit()
