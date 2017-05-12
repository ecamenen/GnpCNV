# -*-coding:Utf-8 -*
"""A module that takes the metadata from an ad hoc file and associate them to a VCF file"""

import os
import sys
import json
import requests
import argparse

###HELP###

def help():
	parser = argparse.ArgumentParser(description="A module that takes the metadata from an ad hoc file and associate them to a VCF file")
	parser.add_argument("-c", dest="cnvFile", required="True", help="the path of your cnv file (ex: /test/cnvFile.csv)")
	parser.add_argument("-m", dest="metadataFile", default="/home/ecamenen/Documents/metadata.csv", help="the name of your metadata file (default: %(default)s)")
	parser.add_argument("--user", "-u", default="rods", help="your iRODS user name (default: %(default)s)")
	parser.add_argument("--pass", "-p", dest="password", default="rods", help="your iRODS password (default: %(default)s)")
	parser.add_argument("-z", dest="zoneName", default="tempZone", help="your zone name (default: %(default)s)")
	#TODO: tempZone/home/rods/test a reflechir sur codage en dur sur cette partie
	parser.add_argument("-url", default="http://localhost:8080/irods-rest/rest/dataObject/", help="the workdirectory of your cnv file (default: your current one).")
	return parser

parser = help()

if len ( sys.argv ) < 2:
	parser.print_help()


args = parser.parse_args()


###PARAMETERS###


metadataFile=open(args.metadataFile, 'r')
user=args.user
password=args.password
url=args.url + args.zoneName + '/home/' + args.user + args.cnvFile + '/metadata'

metadata={}
metadata['metadataEntries'] = []

headers={}
headers['Content-type']='application/json'


###MAIN###

for line in metadataFile:
	if line!="\n":
		key,value=line.split("\t")
		value = value.rstrip()
		parsing={}
		parsing['attribute']=key
		parsing['value']=value
		#TODO: boucle while a la place de for + catcher aussi les erreurs de format
		metadata['metadataEntries'].append(parsing)

try:
	r = requests.put(url,headers=headers,data=json.dumps(metadata),auth=(user,password))
	print(r.status_code)
	assert r.status_code == 200
except AssertionError:
	#refactoring sous forme d'une fonction unique
	if r.status_code == 401:
		msg="Unrecognized users or password."
	elif r.status_code == 403:
		msg="Unauthorized users."
	elif r.status_code == 404:
		msg="File not found."
	elif r.status_code == 408:
		msg="Request Time-out."
	else:
		msg=r.reason
	print("Error: " + msg)
	exit(r.status_code)

#if r.status_code = 400:
#	print("Erroneous request format.")

# A FAIRE: fichier avec bcp de metadata

metadataFile.close()
exit(0)

