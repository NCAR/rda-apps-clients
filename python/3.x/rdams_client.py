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


BASE_URL = 'https://rda-web-dev.ucar.edu/json_apps/'
USE_NETRC = False
DEFAULT_AUTH_FILE = './rdamspw.txt'


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

def write_pw_file(username, password, pwfile=DEFAULT_AUTH_FILE):
    """Write out file with user information."""
    with open(pwfile, "w") as fo:
        npwstring = username + ',' + password
        fo.write(npwstring)

def read_pw_file(pwfile):
    """Read user information from pw file.

    Args:
        pwfile (str): location of password file.

    Returns:
        (tuple): (username,password)
    """
    with open(pwfile, 'r') as f:
        pwstring = f.read()
        (username, password) = pwstring.split(',', 2)
    return(username, password)


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
            help="Do not print result of queries.")
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
            const='ALL',
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
    """Checks that status of return object.

    Exits if a 401 status code.

    Args:
        ret (response.Response): Response of a request.

    Returns:
        None
    """
    if ret.status_code == 401:
        print(ret.content)
        exit(1)

def check_file_status(filepath, filesize):
    """Prints file download status as percent of file complete.

    Args:
        filepath (str): File being downloaded.
        filesize (int): Expected total size of file in bytes.

    Returns:
        None
    """
    sys.stdout.write('\r')
    sys.stdout.flush()
    size = int(os.stat(filepath).st_size)
    percent_complete = (size/filesize)*100
    sys.stdout.write('%.3f %s' % (percent_complete, '% Completed'))
    sys.stdout.flush()

def download_files(filelist, out_dir='./', cookie_file=None):
    """Download files in a list.

    Args:
        filelist (list): List of web files to download.
        out_dir (str): directory to put downloaded files

    Returns:
        None
    """
    if cookie_file is None:
        cookies = get_cookies()
    for _file in filelist:
        file_base = os.path.basename(_file)
        out_file = out_dir + file_base
        print('Downloading',file_base)
        req = requests.get(_file, cookies=cookies, allow_redirects=True, stream=True)
        filesize = int(req.headers['Content-length'])
        with open(out_file, 'wb') as outfile:
            chunk_size=1048576
            for chunk in req.iter_content(chunk_size=chunk_size):
                outfile.write(chunk)
                if chunk_size < filesize:
                    check_file_status(out_file, filesize)
        check_file_status(out_file, filesize)
        print()

def get_authentication(pwfile=DEFAULT_AUTH_FILE):
    """Attempts to get authentication.

    Args:
        pwfile (str): location of password file.

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

def get_cookies(username=None, password=None):
    """Authenticates with RDA and returns authentication cookies.

    The user must authenticate with
    authentication cookies per RDA policy.

    Args:
        username (str): RDA username. Typically the user's email.
        password (str): RDA password.

    Returns:
        requests.cookies.RequestsCookieJar: Login request's cookies.
    """
    if username is None and password is None:
        username,password = get_authentication()

    login_url = "https://rda.ucar.edu/cgi-bin/login"
    values = {'email' : username, 'passwd' : password, 'action' : 'login'}
    ret = requests.post(login_url, data=values)
    if ret.status_code != 200:
        print('Bad Authentication')
        print(ret.text)
        exit(1)
    return ret.cookies


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

def get_filelist(request_idx):
    """Gets filelist for request

    Args:
        request_idx (str): Request Index, typically a 6-digit integer.

    Returns:
        dict: JSON decoded result of the query.
    """
    url = BASE_URL + 'request/'
    url += str(request_idx)
    url += '/filelist_json'

    user_auth = get_authentication()
    ret = requests.get(url, auth=user_auth)

    check_status(ret)

    return ret.json()


def download(request_idx):
    """Download files given request Index

    Args:
        request_idx (str): Request Index, typically a 6-digit integer.

    Returns:
        None
    """
    ret = get_filelist(request_idx)
    if ret['status'] != 'ok':
        return ret

    filelist = ret['result']['web_files']

    user_auth = get_authentication()

    username, password = user_auth
    cookies = get_cookies(username,password)

    web_files = list(map(lambda x: x['web_path'], filelist))

    download_files(web_files)
    return ret

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
    # Maps an argument to function call
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
    if not args.noprint:
        print(json.dumps(result, indent=3))
    return result

if __name__ == "__main__":
    """Calls main method"""
    query(sys.argv[1:])
