# -*-coding:Utf-8 -*
"""A module that takes the metadata from an ad hoc file and associate them to a VCF file"""

#os.system("curl -u rods:rods -XPUT 'http://localhost:8080/irods-rest/rest/dataObject/tempZone/home/rods/test/test_new2.csv/metadata'  -H 'Accept: application/json' -H 'Content-type: application/json' -d '{\"metadataEntries\":[" + output + "]}'")

import os
import sys
import requests
import argparse

###HELP###

#if len(sys.argv) < 2:
 #   print("Please enter only one parameter: the name of your metadata file.")

def help():
	parser = argparse.ArgumentParser(description="A module that takes the metadata from an ad hoc file and associate them to a VCF file")
	#TODO: ajouter workdir au namefile
	parser.add_argument("-c", dest="cnvFile", required="True", help="the name of your cnv file")
	parser.add_argument("-m", dest="metadataFile", default="metadata.csv", help="the name of your metadata file (default: %(default)s)")
	parser.add_argument("--user", "-u", default="rods", help="your iRODS user name (default: %(default)s)")
	parser.add_argument("--pass", "-p", dest="password", default="rods", help="your iRODS password (default: %(default)s)")
	#parser.add_argument("-w", dest="workdir", default="/home/ecamenen/Documents/git/GnpCNV/dataTest", help="the workdirectory of your metadata file (default: your current one).")
	#TODO: tempZone/home/rods/test a reflechir sur codage en dur sur cette partie
	parser.add_argument("-url", default="http://localhost:8080/irods-rest/rest/dataObject/tempZone/home/rods/test/", help="the workdirectory of your cnv file (default: your current one).")
	args = parser.parse_args()
	return args

args=help()

if len(sys.argv) < 2:
	args.print_help()



###PARAMETERS###


os.chdir(args.workdir)
metadataFile=open(args.metadataFile, 'r')
user=args.user
password=args.passwordhtop

parsing=""
cpt=0

url=args.url + args.cnvFile + '/metadata'
headers=dict()
headers['Content-type']='application/json'
#headers['Accept']='application/json'


###FUNCTION####

def escape(string):
	"""Escape the special characters"""
	for ch in ['\"','\'']:
		if ch in string:
			string=string.replace(ch,"\\"+ch)
	return(string)


###MAIN###

for line in metadataFile:
	if line!="\n":
		line=escape(line)
		key,value=line.split("\t")
		value = value.rstrip()
		cpt+=1
		if cpt!=1:
			parsing+=","
			#TODO: reflechir fonction attribution clé/valeur	
		parsing+="{\"attribute\":\""+key+"\",\"value\":\""+value+"\"}"
		#TODO: boucle while a la place de for et formatter en JSON a la fin (catcher aussi les erreurs de format)
		#else, le mettre en fin de boucle
	else:
		try:
			r = requests.put(url,headers=headers,data="{\"metadataEntries\":[" + parsing + "]}",auth=(user,password))
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


		
