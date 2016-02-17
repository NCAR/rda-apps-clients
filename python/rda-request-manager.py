#! /usr/bin/env python

###################################################################################
###
###     Title: rda-request-manager.py
###    Author: Doug Schuster, schuster@ucar.edu
###      Date: 10/25/2013
###   Purpose: Use to download completed RDA requests. 
###
###  SVN File: $HeadURL: https://subversion.ucar.edu/svndss/schuster/rest_client/rda-request-manager.py $
###
###  Usage: 
###    request_download-client.py [RequestIndex]
####################################################################################


import sys
import urllib2
import os
import sys
import getpass
import cookielib
import json

# update_progress() : Displays or updates a console progress bar
## Accepts a float between 0 and 1. Any int will be converted to a float.
## A value under 0 represents a 'halt'.
## A value at 1 or bigger represents 100%
def update_progress(progress,outdir):
    barLength = 20 # Modify this to change the length of the progress bar
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
    block = int(round(barLength*progress))
    text = "\rDownloading Request to './{0}' directory.  Download Progress: [{1}] {2}% {3}".format( outdir,"="*block + " "*(barLength-block), progress*100, status)
    sys.stdout.write(text)
    sys.stdout.flush()

# download_file(remfile,outfile) : download a file from a remote server (remfile) to a local location (outfile) 
def download_file(remfile,outfile):
    frequest = urllib2.Request(remfile)
    fresponse = urllib2.urlopen(remfile)
    handle = open(outfile, 'w')
    handle.write(fresponse.read())
    handle.close()

# get_userinfo() : get username and password
def get_userinfo():
	user=raw_input("Enter your RDA username or email: ")
      	pasw=getpass.getpass("Enter your RDA password: ")
	return(user,pasw)

# add_http_auth(url,user,pasw): add authentication information to opener and return opener
def add_http_auth(url,user,pasw):
	passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
	passman.add_password(None, theurl, username, password)
	authhandler = urllib2.HTTPBasicAuthHandler(passman)
	opener = urllib2.build_opener(authhandler)
	urllib2.install_opener(opener)
        return opener

# add_http_cookie(url,authstring): Get and add authentication cookie to http file download handler
def add_http_cookie(url,authstring):
        cj = cookielib.MozillaCookieJar(cookie_file)
        openrf=urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))		
	frequest = urllib2.Request(url,authstring)
	cj.add_cookie_header(frequest)
	response=openrf.open(frequest)
	openerf = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
	urllib2.install_opener(openerf)

# write_pw_file : Write out file with user information
def write_pw_file(pwfile,username,password):
	fo=open(pwfile, "wb")
	npwstring=username+','+password
	fo.write(npwstring)
	fo.close

# read_pw_file(pwfile) : Read user information from pw file
def read_pw_file(pwfile):
	f=open(pwfile, 'r')
        pwstring=f.read()
        (username,password)=pwstring.split(',',2)
        f.close()
        return(username,password)

# download_files(filelist,directory): Download multiple files from the rda server and save them to a local directory
def download_files(filelist,directory):
	backslash='/'
	filecount=0
	percentcomplete=0
	localsize=''
	length=0
	length=len(filelist)
	if not os.path.exists(directory):
    		os.makedirs(directory)
	for key, value in filelist.iteritems():
       		downloadpath,localfile=key.rsplit("/",1)
        	outpath=directory+backslash+localfile
        	percentcomplete=(float(filecount)/float(length))
        	update_progress(percentcomplete,directory)
        	if os.path.isfile(outpath):
                	localsize=os.path.getsize(outpath)
                	if(str(localsize) != value):
                        	download_file(key,outpath)
        	elif(not os.path.isfile(outpath)):
                	download_file(key,outpath)

        	filecount=filecount+1
        	percentcomplete=(float(filecount)/float(length))
        update_progress(percentcomplete,directory)


sys.tracebacklimit = 0
base='https://rda.ucar.edu/apps/request'
username=''
password=''
pwfile='./rdamspw.txt'
pwstring=''
npwstring=''
cookie_file='auth.rda_ucar_edu'
loginurl='https://rda.ucar.edu/cgi-bin/login'

useagestring="\nUsage: \nrda-request-manager.py -get_status <RequestIndex> <-proc_status>\nrda-request-manager.py -download [RequestIndex]\nrda-request-manager.py -globus_download [RequestIndex]\nrda-request-manager.py -purge [RequestIndex]\nrda-request-manager.py -help\n\n"

getstatusstring="\nOption '-get_status'                               dumps out the status of all RDA data requests.\nOption '-get_status <RequestIndex>'                dumps out the status of RDA data request 'RequestIndex'.\nOption '-get_status <RequestIndex> <-proc_status>' only dump out the request processing status of RDA data request 'RequestIndex' (e.g. O - Online, Q - Request Processing, etc...)\n\n"

downloadstring=   "Option '-download [RequestIndex]  '                download request output files for RDA data request 'RequestIndex' to your local system.\n\n"

globusdownloadstring=   "Option '-globus_download [RequestIndex]  '         set up a Globus endpoint share for RDA data request 'RequestIndex'.  An email will be sent to you with access instructions from Globus.\n\n"

purgestring=      "Option '-purge [RequestIndex]'                     purge request files for RDA data request 'RequestIndex' from RDA data server.  Use this after the request has been fully downloaded to local system.\n\n"

helpstring="rda-request-manager is a utility designed to managed RDA data requests submitted through the web interface or through the rdams-client utility.\n  Users can check on request status, download completed requests to their local system, and purge requests from the RDA data server once they have been downloaded to the local system.\n\n"+useagestring+getstatusstring+downloadstring+globusdownloadstring+purgestring


if (len(sys.argv)<2):
	sys.exit(useagestring)	

if (len(sys.argv)>1):
	if(sys.argv[1]=="-get_status"):
		theurl = base
                if(len(sys.argv)==3):
                        theurl = base+'/'+sys.argv[2]
                elif(len(sys.argv)==4):
                        theurl = base+'/'+sys.argv[2]+'/'+sys.argv[3]
	elif(sys.argv[1]=="-download"):
                if(len(sys.argv)>2):
                        theurl = base+'/'+sys.argv[2]+'/filelist'
                else:
                        sys.exit("\nUsage: \nrda-request-manager.py -download [RequestIndex]\n")
        elif(sys.argv[1]=="-globus_download"):
                if(len(sys.argv)>2):
                        theurl = base+'/'+sys.argv[2]+'/-globus_download'
                else:
                        sys.exit("\nUsage: \nrdams-client.py -globus_download [RequestIndex]\n")
        elif(sys.argv[1]=="-purge"):
		if(len(sys.argv)>2):
                        theurl = base+'/'+sys.argv[2]
                else:
                        sys.exit("\nUsage: \nrda-request-manager.py -purge [RequestIndex]\n")
	elif(sys.argv[1]=="-help"):
		sys.exit(helpstring)
	else:
                sys.exit(useagestring)
else:
        sys.exit(usagestring)


if os.path.isfile(pwfile) and os.path.getsize(pwfile) >0 :
	(username,password)=read_pw_file(pwfile)
else:
	(username,password)=get_userinfo()

opener = add_http_auth(theurl,username,password)
request = urllib2.Request(theurl)

if(sys.argv[1]=="-purge"):
	request.get_method = lambda: 'DELETE'


try:
	url = opener.open(request)
except urllib2.HTTPError, e:
        if e.code == 401:
                print 'RDA username and password invalid.  Please try again\n'
		(username,password)=get_userinfo()
		opener = add_http_auth(theurl,username,password)
                try:
                        url = opener.open(request)
                except urllib2.HTTPError, e:
                        if e.code == 401:
                                print 'RDA username and password invalid, or you are not authorized to access this dataset.\n'
                                print 'Please verify your login information at http://rda.ucar.edu\n.'
                                sys.exit()


write_pw_file(pwfile,username,password)

authdata='email='+username+'&password='+password+'&action=login'

jsonfilelist=url.read()

if(jsonfilelist[0]!="{"):
	print jsonfilelist
	sys.exit()

filelist=json.loads(jsonfilelist)

directory='rda_request_'+sys.argv[2]

# get cookie required to download data files
add_http_cookie(loginurl,authdata)

print "\n\nStarting Download.\n\n"

download_files(filelist,directory)
