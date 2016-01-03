#!/usr/bin/python

from datetime import datetime
import os.path
import subprocess
import sys

# check if protoc command is installed
def protoc_installed():
    try:
        subprocess.check_output(['which', 'protoc'])
    except:
        return False
    return True

# check if curl command is installed
def curl_installed():
    try:
        subprocess.check_output(['which', 'curl'])
    except:
        return False
    return True

# parse command-line arguments and return proto_script and curl_options
# proto_script is a path to protobuf data loading script file
# curl_options is a list to pass curl command
def parse_args(args):
    proto_script = ''
    curl_options = []
    for arg in sys.argv[1:]:
        if arg[:8] == '--proto=':
            proto_script = arg[8:]
        else:
            curl_options.append(arg)
    return (proto_script, curl_options)

# load proto_script file and return succeed(True) or not(False), and binary
def get_proto_binary(proto_script):
    variables = dict()
    try:
        exec open(proto_script) in variables
    except:
        return (False, '')

    if not 'result' in variables:
        return (False, '')
    return (True, variables['result'])

# write binary(protobuf) data to path
# return True if this succeeded
def write_binary(path, data):
    try:
        f = open(path, 'wb')
        f.write(data)
        f.close()
    except IOError:
        return False
    return True

# run curl command with curl_options
# this send data stored at binary_path
def process_curl(binary_path, curl_options):
    curl_command = [
        'curl',
        '--request', 'POST',
        '--header', 'Content-Type: x-protobuf',
        '--data-binary', '-', # use cat stdout
    ]
    cat_ret = subprocess.Popen(
        ['cat', binary_path],
        stdout = subprocess.PIPE,
    )
    curl_ret = subprocess.Popen(
        curl_command + curl_options,
        stdin  = cat_ret.stdout,
        stdout = subprocess.PIPE,
        shell  = False
    )
    cat_ret.stdout.close()

    return curl_ret.communicate()[0]

#
# Main procedure
#
if __name__ == '__main__':
    # check commands depended by this script
    if not protoc_installed():
        print '[error] protoc is not installed.'
        sys.exit(1)
    if not curl_installed():
        print '[error] curl is not installed.'
        sys.exit(1)

    # parse command-line arguments
    (proto_script, curl_options) = parse_args(sys.argv)
    if proto_script == '' or not len(sys.argv) > 2:
        # check reference if you are not familiar with PROTOBUF_SCRIPT
        print '[error] usage:', sys.argv[0], '--proto=PROTOBUF_SCRIPT', '[curl option(s)], URL'
        sys.exit(1)

    # load proto_script and get binary
    if not os.path.isfile(proto_script):
        print '[error] PROTOBUF_SCRIPT is missing or not file.'
        sys.exit(1)
    (result, data) = get_proto_binary(proto_script)
    if not result:
        print '[error] invalid binary data given. check your protobuf script.'
        sys.exit(1)

    # write binary to temporary file
    binary_path = '/tmp/purl_cache_' + datetime.now().isoformat()
    if not write_binary(binary_path, data):
        print '[error] writing binary failed'
        sys.exit(1)

    # process curl
    print process_curl(binary_path, curl_options)

    # delete temporary file
    os.remove(binary_path)

