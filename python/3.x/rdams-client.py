#!/usr/bin/env python
"""List dataset metadata, subset data subset requests,
check on request status.

Usage:
```
rdams-client.py -get_summary <dsnnn.n>
rdams-client.py -get_metadata <dsnnn.n> <-f>
rdams-client.py -get_param_summary <dsnnn.n> <-f>
rdams-client.py -submit [control_file_name]
rdams-client.py -get_status <RequestIndex> <-proc_status>
rdams-client.py -download [RequestIndex]
rdams-client.py -globus_download [RequestIndex]
rdams-client.py -get_control_file_template <dsnnn.n>
rdams-client.py -help
```
"""
__version__ = '2.0.0'
__author__ = 'Doug Schuster (schuster@ucar.edu), Riley Conroy (rpconroy@ucar.edu)'

import pdb
import sys
import os
import requests
import urllib.request
import urllib.error
import urllib.parse
import getpass
import http.cookiejar
import json
import argparse


BASE_URL = 'https://rda.ucar.edu/json_apps/'
USE_NETRC = False
DEFAULT_AUTH_FILE = './rdamspw.txt'

def update_progress(progress, outdir):
    """Displays or updates a console progress bar

    Accepts a float between 0 and 1. Any int will be converted to a float.
    A value under 0 represents a 'halt'.
    A value at 1 or bigger represents 100%
    """
    barLength = 20  # Modify this to change the length of the progress bar
    status = ""
    if isinstance(progress, int):
        progress = float(progress)
    if not isinstance(progress, float):
        progress = 0
        status = "error: progress var must be float\r\n\n"
    if progress < 0:
        progress = 0
        status = "Halt...\r\n\n"
    if progress >= 1:
        progress = 1
        status = "Done...\r\n\n"
    block = int(round(barLength * progress))
    text = "\rDownloading Request to './{0}' directory.  Download Progress: [{1}] {2}% {3}".format(
        outdir, "=" * block + " " * (barLength - block), progress * 100, status)
    sys.stdout.write(text)
    sys.stdout.flush()

def download_file(remfile, outfile):
    """Download a file from a remote server (remfile) to a local location (outfile)."""
    frequest = urllib.request.Request(remfile)
    fresponse = urllib.request.urlopen(remfile)
    with open(outfile, 'wb') as handle:
        handle.write(fresponse.read())

def add_ds_str(ds_num):
    """Adds 'ds' to ds_num if needed.
    Throws error if ds number isn't valid.
    """
    ds_num = ds_num.strip()
    if ds_num[0:2] != 'ds':
        ds_num = 'ds' + ds_num
    if len(ds_num) != 7:
        print("'" + ds_num + "' is not valid.")
        sys.exit()
    return ds_num

def get_userinfo():
    """Get username and password from the command line."""
    user = input("Enter your RDA username or email: ")
    pasw = getpass.getpass("Enter your RDA password: ")
    try:
        write_pw_file(user, pasw)
    except:
        pass
    return(user, pasw)

def add_http_auth(url, user, pasw):
    """Add authentication information to opener and return opener."""
    passman = urllib.request.HTTPPasswordMgrWithDefaultRealm()
    passman.add_password(None, theurl, username, password)
    authhandler = urllib.request.HTTPBasicAuthHandler(passman)
    opener = urllib.request.build_opener(authhandler)
    urllib.request.install_opener(opener)
    return opener

def add_http_cookie(url, authstring, cookie_file='auth.rda_ucar_edu'):
    """Get and add authentication cookie to http file download handler."""
    cj = http.cookiejar.MozillaCookieJar(cookie_file)
    openrf = urllib.request.build_opener(
        urllib.request.HTTPCookieProcessor(cj))
    frequest = urllib.request.Request(url, authstring)
    cj.add_cookie_header(frequest)
    response = openrf.open(frequest)
    openerf = urllib.request.build_opener(
        urllib.request.HTTPCookieProcessor(cj))
    urllib.request.install_opener(openerf)

def write_pw_file(username, password, pwfile=DEFAULT_AUTH_FILE):
    """Write out file with user information."""
    with open(pwfile, "w") as fo:
        npwstring = username + ',' + password
        fo.write(npwstring)

def read_pw_file(pwfile):
    """Read user information from pw file."""
    with open(pwfile, 'r') as f:
        pwstring = f.read()
        (username, password) = pwstring.split(',', 2)
    return(username, password)

def download_files(filelist, directory):
    """Download multiple files from the rda server and save them to a local directory."""
    backslash = '/'
    filecount = 0
    percentcomplete = 0
    localsize = ''
    length = 0
    length = len(filelist)
    if not os.path.exists(directory):
        os.makedirs(directory)
    for key, value in filelist.items():
        downloadpath, localfile = key.rsplit("/", 1)
        outpath = directory + backslash + localfile
        percentcomplete = (float(filecount) / float(length))
        update_progress(percentcomplete, directory)
        if os.path.isfile(outpath):
            localsize = os.path.getsize(outpath)
            if(str(localsize) != value):
                download_file(key, outpath)
        elif(not os.path.isfile(outpath)):
            download_file(key, outpath)

        filecount = filecount + 1
        percentcomplete = (float(filecount) / float(length))
    update_progress(percentcomplete, directory)

def read_control_file(control_file):
    """Reads control file, and return python dict.

    Args:
        control_file (str): Location of control file to parse.

    Returns:
        (dict) python dict representing control file.
    """
    control_params = {}
    with open(control_file, "r") as myfile:
        for line in myfile:
            if line.startswith('#'):
                continue
            li = line.rstrip()
            (key, value) = li.split('=', 2)
            control_params[key] = value
    return control_params

def get_parser():
    """Creates and returns parser object.

    Returns:
        (argparse.ArgumentParser): Parser object from which to parse arguments.
    """
    description = "Queries NCAR RDA REST API."
    parser = argparse.ArgumentParser(prog='rdams', description=description)
    parser.add_argument('-noprint', '-np',
            action='store_true',
            required=False,
            help="Print result of queries.")
    parser.add_argument('-use_netrc', '-un',
            action='store_true',
            required=False,
            help="Use your .netrc file for authentication.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-get_summary', '-gsum',
            type=str,
            metavar='<dsid>',
            required=False,
            help="Get a summary of the given dataset.")
    group.add_argument('-get_metadata', '-gm',
            type=str,
            metavar='<dsid>',
            required=False,
            help="Get metadata for a given dataset.")
    group.add_argument('-get_param_summary', '-gpm',
            type=str,
            metavar='<dsid>',
            required=False,
            help="Get only parameters for a given dataset.")
    group.add_argument('-submit', '-s',
            type=str,
            metavar='<dsid>',
            required=False,
            help="Submit a request using a control file.")
    group.add_argument('-get_status', '-gs',
            type=str,
            nargs='?',
            default='ALL',
            metavar='<Request Index>',
            required=False,
            help="Get a summary of the given dataset.")
    group.add_argument('-download', '-d',
            type=str,
            required=False,
            metavar='<Request Index>',
            help="Download data given a request id.")
    group.add_argument('-globus_download', '-gd',
            type=str,
            required=False,
            metavar='<Request Index>',
            help="Start a globus transfer for a give request index.")
    group.add_argument('-get_control_file_template', '-gt',
            type=str,
            metavar='<dsid>',
            required=False,
            help="Get a template control file used for subsetting.")
    group.add_argument('-purge', # Sorry no -p
            type=str,
            metavar='<Request Index>',
            required=False,
            help="Purge a request.")
    return parser

def check_status(ret):
    """Checks that status of return object."""
    if ret.status_code == 401:
        print(ret.content)
        exit(1)

def get_authentication(pwfile=DEFAULT_AUTH_FILE):
    """Attempts to get authentication.

    Returns:
        (tuple): username, passord
        (None): If using .netrc file
    """
    if USE_NETRC:
        return None
    if os.path.isfile(pwfile) and os.path.getsize(pwfile) > 0:
        return read_pw_file(pwfile)
    else:
        return get_userinfo()

def get_summary(ds):
    """Returns summary of dataset.

    Args:
        ds (str): Datset id. e.g. 'ds083.2'

    Returns:
        dict: JSON decoded result of the query.
    """
    url = BASE_URL + 'summary/'
    url += ds

    user_auth = get_authentication()
    ret = requests.get(url, auth=user_auth)

    check_status(ret)
    return ret.json()

def get_metadata(ds):
    """Return metadata of dataset.

    Args:
        ds (str): Datset id. e.g. 'ds083.2'

    Returns:
        dict: JSON decoded result of the query.
    """
    url = BASE_URL + 'metadata/'
    url += ds

    user_auth = get_authentication()
    ret = requests.get(url, auth=user_auth)

    check_status(ret)
    return ret.json()

def get_param_summary(ds):
    """Return summary of parameters for a dataset.

    Args:
        ds (str): Datset id. e.g. 'ds083.2'

    Returns:
        dict: JSON decoded result of the query.
    """
    url = BASE_URL + 'paramsummary/'
    url += ds

    user_auth = get_authentication()
    ret = requests.get(url, auth=user_auth)

    check_status(ret)
    return ret.json()

def submit_json(json_file):
    """Submit a RDA subset or format conversion request using json file or dict.

    Args:
        json_file (str): json control file to submit.
                OR
                Python dict to submit.

    Returns:
        dict: JSON decoded result of the query.
    """
    if type(json_file) is str:
        assert os.path.isfile(json_file)
        with open(json_file) as fh:
            control_dict = json.load(fh)
    else:
        assert type(json_file) is dict
        control_dict = json_file

    url = BASE_URL + 'request/'

    user_auth = get_authentication()
    ret = requests.post(url, data=control_dict, auth=user_auth)

    check_status(ret)
    return ret.json()

def submit(control_file_name):
    """Submit a RDA subset or format conversion request.
    Calls submit json after reading control_file

    Args:
        control_file_name (str): control file to submit.

    Returns:
        dict: JSON decoded result of the query.
    """
    _dict = read_control_file(control_file_name)
    return submit_json(_dict)


def get_status(request_idx=None):
    """Get status of request.
    If request_ix not provided, get all open requests

    Args:
        request_idx (str, Optional): Request Index, typcally a 6-digit integer.

    Returns:
        dict: JSON decoded result of the query.
    """
    url = BASE_URL + 'request/'
    url += request_idx

    user_auth = get_authentication()
    ret = requests.get(url, auth=user_auth)

    check_status(ret)
    return ret.json()

def download(request_idx):
    """Download files from request Index

    Args:
        request_idx (str): Request Index, typically a 6-digit integer.

    Returns:
        dict: JSON decoded result of the query.
    """
    url = BASE_URL + 'request/'
    url += request_idx
    url += 'filelist'

    user_auth = get_authentication()
    ret = requests.get(url, auth=user_auth)

    check_status(ret)
    return ret.json()

def globus_download(request_idx):
    """Begin a globus transfer.

    Args:
        request_ix (str): Request Index, typically a 6-digit integer.

    Returns:
        dict: JSON decoded result of the query.
    """
    url = BASE_URL + 'request/'
    url += request_idx
    url += '-globus_download'

    user_auth = get_authentication()
    ret = requests.get(url, auth=user_auth)

    check_status(ret)
    return ret.json()

def get_control_file_template(ds):
    """Write a control file for use in subset requests.

    Args:
        ds (str): datset id. e.g. 'ds083.2'

    Returns:
        dict: JSON decoded result of the query.
    """
    url = BASE_URL + 'template/'
    url += ds

    user_auth = get_authentication()
    ret = requests.get(url, auth=user_auth)

    check_status(ret)
    control_str = ret.content.decode("utf-8")
    return ret.json()

def write_control_file_template(ds, write_location=None):
    """Write a control file for use in subset requests.

    Args:
        ds (str): datset id. e.g. 'ds083.2'
        write_location (str, Optional): Directory in which to write.
                Defaults to working directory

    Returns:
        None
    """
    url = BASE_URL + 'template/'
    url += ds

    user_auth = get_authentication()
    ret = requests.get(url, auth=user_auth)

    check_status(ret)
    return ret.json()

def purge_request(request_idx):
    """Write a control file for use in subset requests.

    Args:
        ds (str): datset id. e.g. 'ds083.2'
        write_location (str, Optional): Directory in which to write.
                Defaults to working directory

    Returns:
        None
    """
    url = BASE_URL + 'request/'
    url += request_idx

    user_auth = get_authentication()
    ret = requests.delete(url, auth=user_auth)

    check_status(ret)
    return ret.json()

def get_selected_function(args_dict):
    """Returns correct function based on options.
    Args:
        options (dict) : Command with options.

    Returns:
        (function): function that the options specified
    """
    action_map = {
            'get_summary' : get_summary,
            'get_metadata' : get_metadata,
            'get_param_summary' : get_param_summary,
            'submit' : submit,
            'get_status' : get_status,
            'download' : download,
            'globus_download' : globus_download,
            'get_control_file_template' : write_control_file_template,
            'purge' : purge_request
            }
    for opt,value in args_dict.items():
        if opt in action_map and value is not None:
            return (action_map[opt], value)

def query(args):
    """Perform a query based on command line like arguments.

    Args:
        args (list): argument list of querying commands.

    Returns:
        (dict): Output of json decoded API query.

    Example:
        ```
        >>> query(['-get_status', '123456']
        ```
    """
    parser = get_parser()
    if len(args) == 0:
        parser.parse_args(['-h'])
    args = parser.parse_args(args)
    if args.use_netrc:
        USE_NETRC = True
    args_dict = args.__dict__
    func,params = get_selected_function(args_dict)
    result = func(params)
    if args.print:
        print(json.dumps(result, indent=3))
    return result

    exit()

    sys.tracebacklimit = 0
    jsondata = ''
    username = ''
    password = ''
    pwstring = ''
    npwstring = ''
    controlfile = ''
    controlparms = {}
    loginurl = 'https://rda.ucar.edu/cgi-bin/login'
    exitstring = "\nUsage: \nrdams-client.py -get_summary <dsnnn.n>\nrdams-client.py -get_metadata <dsnnn.n>\nrdams-client.py -get_param_summary <dsnnn.n>\nrdams-client.py -submit [control_file_name]\nrdams-client.py -get_status <RequestIndex> <-proc_status>\nrdams-client.py -download [RequestIndex]\nrdams-client.py -globus_download [RequestIndex]\nrdams-client.py -purge [RequestIndex]\nrdams-client.py -get_control_file_template <dsnnn.n>\nrdams-client.py -help\n\n"

    if len(sys.argv) > 1:
        if sys.argv[1] == "-get_summary":
            print('\nGetting summary information.  Please wait as this may take awhile.\n')
            theurl = base + 'summary'
            if len(sys.argv) > 2:
                theurl = base + 'summary/' + add_ds_str(sys.argv[2])
        elif sys.argv[1] == "-get_metadata":
            print('\nGetting metadata.  Please wait as this may take awhile.\n')
            theurl = base + 'metadata'
            if len(sys.argv) == 3:
                theurl = base + 'metadata/' + add_ds_str(sys.argv[2])
            elif len(sys.argv) == 4:
                theurl = base + 'metadata/' + add_ds_str(sys.argv[2]) + '/formatted'
        elif sys.argv[1] == "-get_param_summary":
            print('\nGetting parameter summary.  Please wait as this may take awhile.\n')
            theurl = base + 'paramsummary'
            if len(sys.argv) == 3:
                theurl = base + 'paramsummary/' + add_ds_str(sys.argv[2])
            elif len(sys.argv) == 4:
                theurl = base + 'paramsummary/'+ add_ds_str(sys.argv[2]) + '/formatted'
        elif sys.argv[1] == "-help":
            theurl = base + 'help'
        elif sys.argv[1] == "-get_control_file_template":
            theurl = base + 'template'
            controlfile = './dsnnn.n_control_file'
            if len(sys.argv) > 2:
                theurl = base + 'template/' + add_ds_str(sys.argv[2])
                controlfile = './' + add_ds_str(sys.argv[2]) + '_control_file'
        elif sys.argv[1] == "-get_status":
            theurl = base + 'request'
            if len(sys.argv) == 3:
                theurl = base + 'request/' + sys.argv[2]
            elif len(sys.argv) == 4:
                theurl = base + 'request/' + sys.argv[2] + '/' + add_ds_str(sys.argv[3])
        elif sys.argv[1] == "-download":
            if len(sys.argv) > 2:
                theurl = base + 'request/' + sys.argv[2] + '/filelist'
            else:
                sys.exit("\nUsage: \nrdams-client.py -download [RequestIndex]\n")
        elif sys.argv[1] == "-globus_download":
            if len(sys.argv) > 2:
                theurl = base+'request/' + sys.argv[2] + '/-globus_download'
            else:
                sys.exit("\nUsage: \nrdams-client.py -globus_download [RequestIndex]\n")
        elif sys.argv[1] == "-purge":
            if len(sys.argv) > 2:
                theurl = base + 'request/' + sys.argv[2]
            else:
                sys.exit("\nUsage: \nrdams-client.py -purge [RequestIndex]\n")
        elif sys.argv[1] == "-submit":
            if len(sys.argv) > 2:
                theurl = base + 'request'
                with open(sys.argv[2], "r") as myfile:
                    for line in myfile:
                        if line.startswith('#'):
                            continue
                        li = line.rstrip()
                        (key, value) = li.split('=', 2)
                        controlparms[key] = value
                jsondata = '{'
                for k in list(controlparms.keys()):
                    jsondata += '"' + k + '"' + ":" + '"' + controlparms[k] + '",'
                jsondata = jsondata[:-1]
                jsondata += '}'
                print('\nSubmitting request.  Please wait as this may take awhile.\n')
            else:
                sys.exit(
                    "\nUsage: \nrdams-clientpy -submit [control_file_name]\n")
        else:
            sys.exit(exitstring)
    else:
        sys.exit(exitstring)


    if os.path.isfile(pwfile) and os.path.getsize(pwfile) > 0:
        (username, password) = read_pw_file(pwfile)
    else:
        (username, password) = get_userinfo()
    opener = add_http_auth(theurl, username, password)

    if len(jsondata) > 1:
        request = urllib.request.Request(
            theurl, jsondata.encode(), {'Content-type': 'application/json'})
    else:
        request = urllib.request.Request(theurl)

    if sys.argv[1] == "-purge":
        request.get_method = lambda: 'DELETE'

    try:
        url = opener.open(request)
    except urllib.error.HTTPError as e:
        if e.code == 401:
            print('RDA username and password invalid.  Please try again\n')
            (username, password) = get_userinfo()
            opener = add_http_auth(theurl, username, password)
            try:
                url = opener.open(request)
            except urllib.error.HTTPError as e:
                if e.code == 401:
                    print(
                        'RDA username and password invalid, or you are not authorized to access this dataset.\n')
                    print('Please verify your login information at http://rda.ucar.edu\n.')
                    sys.exit()


    write_pw_file(pwfile, username, password)


    if sys.argv[1] == "-get_control_file_template":
        print('\nWriting example control file to ' + controlfile + '\n')
        with open(controlfile, "wb") as fo:
            fo.write(url.read())
        sys.exit()
    if sys.argv[1] == "-download":
        authdata = 'email=' + username + '&password=' + password + '&action=login'
        authdata = authdata.encode()

        jsonfilelist = url.read().decode()

        if jsonfilelist[0] != "{":
            print(jsonfilelist)
            sys.exit()

        filelist = json.loads(jsonfilelist)
        length = len(filelist)

        directory = 'rda_request_' + sys.argv[2]

        # get cookie required to download data files
        add_http_cookie(loginurl, authdata)

        print("\n\nStarting Download.\n\n")

        download_files(filelist, directory)

        sys.exit()

    print(url.read().decode())

if __name__ == "__main__":
    """Calls Generic main method"""
    query(sys.argv[1:])
