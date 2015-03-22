'''
'''
from fabric.api import task
from fabric.colors import red, green, yellow, blue

from ftplib import FTP

import os


FTP_ADDRESS = ""
FTP_USER = ""
FTP_PASSWORD = ""

INDEX_FTP_DIR = "/public_html"
BLOG_FTP_DIR = "/public_html/blog"
INDEX_LOCAL_DIR = "/home/leny/Projects/mandla.me/index"
BLOG_LOCAL_DIR = "/home/leny/Projects/mandla.me/blog"


def connect(host=FTP_ADDRESS, username=FTP_USER, passwd=FTP_PASSWORD):
    '''Connects to the FTP server'''
    ftp = FTP(host=host)
    ftp.login(user=username, passwd=passwd)

    return ftp


@task
def test_ftp():
    ftp = connect()
    print blue(FTP.getwelcome(ftp))
    ftp.quit()


@task
def deploy():
    print ""
    print green("** Upload latest changes **")

    ftp = connect()
    f = os.path.join(INDEX_LOCAL_DIR, "test.txt")
    split = os.path.split(f)
    remote_dir = INDEX_FTP_DIR
    ftp.cwd(remote_dir)

    print blue('STOR %s' % f) , blue(" -> "), os.path.join(remote_dir, split[1]),
    try:
       ftp.storlines("STOR %s" % split[1], open(f, "r"))
       print green(u'\u2713')
    except IOError as e:
       print red('>> %s' % e.strerror)

    print ""
    print green('** Closing FTP connection **')
    ftp.quit()
