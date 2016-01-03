#! /usr/bin/python

from datetime import datetime
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

def parse_arg(args):
    proto_script = ''
    curl_options = ''
    for arg in sys.argv:
        if arg[:8] == '--proto=':
            proto_script = arg[8:]
        else:
            curl_options += ' ' + arg
    return (proto_script, curl_options)

def get_proto_binary(proto_script):
    # TODO:
    raise Exception()

def write_binary(path, binary):
    try:
        f = open(path, 'w')
        f.write(binary)
        f.close()
    except:
        return False
    return True

# Main procedure
if __name__ == '__main__':
    if not protoc_installed():
        print '[error] protoc is not installed.'
        sys.exit(1)

    if not curl_installed():
        print '[error] curl is not installed.'
        sys.exit(1)

    (proto_script, curl_options) = parse_arg(sys.argv)

    if proto_script == '' or not len(sys.argv) > 2:
        print '[error] usage:', sys.argv[0], '--proto=PROTOBUF_SCRIPT', '[curl option(s)], URL'
        sys.exit(1)

    data = get_proto_binary(proto_script)
    path = '/tmp/purl_cache_' + datetime.now().isoformat()
    if not write_binary(path, data):
        print '[error] writing binary failed'
        sys.exit(1)

    subprocess.call(['cat''curl', '--request POST', '--data-binary %s' % data, curl_options])

