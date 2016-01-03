#! /usr/bin/python

import subprocess
import sys


def protoc_installed():
    try:
        subprocess.check_output(['which', 'protoc'])
    except:
        return False
    return True

def curl_installed():
    try:
        subprocess.check_output(['which', 'curl'])
    except:
        return False
    return True

if __name__ == '__main__':
    if not protoc_installed():
        print '[error] protoc is not installed.'
        sys.exit(1)

    if not curl_installed():
        print '[error] curl is not installed.'
        sys.exit(1)

