#! /usr/bin/env python

###################################################################################
###
###     Title: rdams-client.py
###    Author: Doug Schuster, schuster@ucar.edu
###      Date: 06/30/2014
###   Purpose: List dataset metadata, subset data subset requests, check on request
###            status.
###
###  SVN File: $HeadURL: https://subversion.ucar.edu/svndss/schuster/rest_client/rdams-client.py $
###
###  Usage: 
###   rdams-client.py -get_summary <dsnnn.n>
###   rdams-client.py -get_metadata <dsnnn.n> <-f>
###   rdams-client.py -submit [control_file_name]
###   rdams-client.py -get_status <RequestIndex> <-proc_status>
###   rdams-client.py -download [RequestIndex]
###   rdams-client.py -get_control_file_template <dsnnn.n>
###   rdams-client.py -help
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
        cj.save('./auth.rda_ucar_edu', True, True)

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
base='https://rda.ucar.edu/apps/'
jsondata=''
username=''
password=''
pwfile='./rdamspw.txt'
pwstring=''
npwstring=''
controlfile=''
controlparms = {}
cookie_file='auth.rda_ucar_edu'
loginurl='https://rda.ucar.edu/cgi-bin/login'
exitstring="\nUsage: \nrdams-client.py -get_summary <dsnnn.n>\nrdams-client.py -get_metadata <dsnnn.n>\nrdams-client.py -submit [control_file_name]\nrdams-client.py -get_status <RequestIndex> <-proc_status>\nrdams-client.py -download [RequestIndex]\nrdams-client.py -purge [RequestIndex]\nrdams-client.py -get_control_file_template <dsnnn.n>\nrdams-client.py -help\n\n" 

if (len(sys.argv)>1):
	if(sys.argv[1]=="-get_summary"):
		print '\nGetting summary information.  Please wait as this may take awhile.\n'
		theurl = base+'summary' 
		if(len(sys.argv)>2):
    			theurl = base+'summary/'+sys.argv[2]
	elif(sys.argv[1]=="-get_metadata"):
		print '\nGetting metadata.  Please wait as this may take awhile.\n'
		theurl = base+'metadata'
		if(len(sys.argv)==3):
			theurl = base+'metadata/'+sys.argv[2]
		elif(len(sys.argv)==4):
			theurl = base+'metadata/'+sys.argv[2]+'/formatted'
        elif(sys.argv[1]=="-help"):
                theurl = base+'help'
        elif(sys.argv[1]=="-get_control_file_template"):
                theurl = base+'template'
		controlfile='./dsnnn.n_control_file'
                if(len(sys.argv)>2):
                        theurl = base+'template/'+sys.argv[2]
			controlfile='./'+sys.argv[2]+'_control_file'
        elif(sys.argv[1]=="-get_status"):
                theurl = base+'request'
                if(len(sys.argv)==3):
                        theurl = base+'request/'+sys.argv[2]
		elif(len(sys.argv)==4):
			theurl = base+'request/'+sys.argv[2]+'/'+sys.argv[3]
	elif(sys.argv[1]=="-download"):
                if(len(sys.argv)>2):
                        theurl = base+'request/'+sys.argv[2]+'/filelist'
		else:
			sys.exit("\nUsage: \nrdams-client.py -download [RequestIndex]\n")
        elif(sys.argv[1]=="-purge"):
                if(len(sys.argv)>2):
                        theurl = base+'request/'+sys.argv[2]
                else:
                        sys.exit("\nUsage: \nrdams-client.py -purge [RequestIndex]\n")
        elif(sys.argv[1]=="-submit"):
                if(len(sys.argv)>2):
                        theurl = base+'request'
			with open (sys.argv[2], "r") as myfile:
				for line in myfile:
					if line.startswith('#'):
						continue
					li=line.rstrip()
					(key,value)=li.split('=',2)
					controlparms[key]=value	
			jsondata='{'
			for k in controlparms.keys():
				jsondata+='"'+k+'"'+":"+'"'+controlparms[k]+'",'
			jsondata = jsondata[:-1]
			jsondata+='}'
			print '\nSubmitting request.  Please wait as this may take awhile.\n'
                else:
			sys.exit("\nUsage: \nrdams-client.py -submit [control_file_name]\n") 			
	else:
		sys.exit(exitstring)
else:
	sys.exit(exitstring)


if os.path.isfile(pwfile) and os.path.getsize(pwfile) >0 :
	(username,password)=read_pw_file(pwfile)
else:
	(username,password)=get_userinfo()

#opener = add_http_auth(theurl,username,password)

#try using cookie authentication
cj=cookielib.MozillaCookieJar('./cookie.txt')
cj.load()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
urllib2.install_opener(opener)

if(len(jsondata)>1):
	request = urllib2.Request(theurl,jsondata,{'Content-type': 'application/json'})
else:
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


if(sys.argv[1]=="-get_control_file_template"):
 	print '\nWriting example control file to '+controlfile+'\n'
	fo=open(controlfile, "wb")
	fo.write(url.read())
	fo.close    
	sys.exit()
if(sys.argv[1]=="-download"):
	authdata='email='+username+'&password='+password+'&action=login'

	jsonfilelist=url.read()

	if(jsonfilelist[0]!="{"):
        	print jsonfilelist
        	sys.exit()

	filelist=json.loads(jsonfilelist)
	length=len(filelist)

	directory='rda_request_'+sys.argv[2]

        # get cookie required to download data files
        add_http_cookie(loginurl,authdata)

        print "\n\nStarting Download.\n\n"

        download_files(filelist,directory)

	sys.exit()

print url.read()
