'''
    Deploying to mandla.me via FTP
'''
from __future__ import print_function
from fabric.api import task
from fabric.colors import red, green, yellow, blue

from ftplib import FTP

import os
from ConfigParser import SafeConfigParser


def get_config(default_path='config.ini'):
    '''Setup application configuration '''
    config = SafeConfigParser()
    path = default_path
    if os.path.exists(path):
        with open(path) as source:
            config.readfp(source)
    else:
        error_msg = "{} does not exist".format(path)
        print(red(error_msg))
        raise IOError(error_msg)
    return config


def connect(config):
    '''Connects to the FTP server'''
    host = config.get("credentials", "host")
    username = config.get("credentials", "username")
    password = config.get("credentials", "password")

    ftp = FTP(host=host)
    ftp.login(user=username, passwd=password)

    return ftp


@task
def test_ftp():
    config = get_config()
    ftp = connect(config)
    print(blue(FTP.getwelcome(ftp)))
    ftp.quit()


@task
def deploy():
    config = get_config()

    ftp = connect(config)
    remote_root = config.get("directories", "remote_root")
    local_root = config.get("directories", "local_root")

    ftp.cwd(remote_root)
    f = os.path.join(local_root, "index", "test.txt")
    split = os.path.split(f)

    print(blue('STOR %s' % f), end="")
    print(blue(" -> "), end="")
    print(os.path.join(remote_root, split[1]), end="")

    try:
       ftp.storlines("STOR %s" % split[1], open(f, "r"))
       print(green(u' \u2713'))
    except IOError as e:
       print(red('>> %s' % e.strerror))

    ftp.quit()
