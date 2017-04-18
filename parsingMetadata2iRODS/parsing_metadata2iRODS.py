# -*-coding:Utf-8 -*
"""A modulate that takes the metadata from an ad hoc file and associate them to a VCF file"""

#os.system("curl -u rods:rods -XPUT 'http://localhost:8080/irods-rest/rest/dataObject/tempZone/home/rods/test/test_new2.csv/metadata'  -H 'Accept: application/json' -H 'Content-type: application/json' -d '{\"metadataEntries\":[" + output + "]}'")

import os
import sys
import requests
import argparse

###HELP###

if len(sys.argv) != 2:
    print("Please enter only one parameter: the name of your metadata file.")
    sys.exit(1)

parser = argparse.ArgumentParser()
parser.add_argument("filename", help="the name of your metadata file")
args = parser.parse_args()


###PARAMETERS###

os.chdir("/home/ecamenen/Documents/git/GnpCNV/dataTest")
filename=args.filename
my_file=open(filename, 'r')
parsing=""
cpt=0
outputFile='test_new.csv'
#workdir=""

url='http://localhost:8080/irods-rest/rest/dataObject/tempZone/home/rods/test/' + outputFile + '/metadata'
user="rods"
password="rods"
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

for line in my_file:
	if line!="\n":
		key,value=line.split("\t")
		value = value.rstrip()
		cpt+=1
		if cpt!=1:
			parsing+=","		
		parsing+="{\"attribute\":\""+key+"\",\"value\":\""+value+"\"}"
	else:
		my_file.close()
		print(data)
		r = requests.put(url,headers=headers,data="{\"metadataEntries\":[" + parsing + "]}",auth=(user,password))
		print(r.status_code)
		print(r.content)
		exit(0)


		
