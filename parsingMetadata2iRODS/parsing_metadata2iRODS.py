# -*-coding:Utf-8 -*
"""A module that takes the metadata from an ad hoc file and associate them to a VCF file"""

import os, sys, json, requests, argparse
from irods.session import iRODSSession
from irods import exception as iExc
reload(sys)
sys.setdefaultencoding('utf8')

###HELP###

def help():
	parser = argparse.ArgumentParser(description="A module that takes the metadata from an ad hoc file and associate them to a VCF file")
	parser.add_argument("-c", dest="cnvFile", required="True", help="the path of your cnv file (ex: /test/cnvFile.csv)")
	parser.add_argument("-m", dest="metadataFile", default="/home/ecamenen/Documents/metadata.csv", help="the name of your metadata file (default: %(default)s)")
	parser.add_argument("--user", "-u", default="rods", help="your iRODS user name (default: %(default)s)")
	parser.add_argument("--pass", "-p", dest="password", default="rods", help="your iRODS password (default: %(default)s)")
	parser.add_argument("--zone", default="tempZone", help="your zone name (default: %(default)s)")
	parser.add_argument("--port", default=1247, help="the number of your port (default: %(default)s)")
	parser.add_argument("-host", default="localhost", help="the workdirectory of your cnv file (default: your current one).")
	#client_user='another_user', client_zone='another_zone
	return parser

parser = help()

if len ( sys.argv ) < 2:
	parser.print_help()


args = parser.parse_args()


###PARAMETERS###

cnvFile = args.cnvFile
metadataFile=open(args.metadataFile, 'r')
user=args.user
password = args.password
zone = args.zone
port = args.port
host = args.host

#sess = iRODSSession(host=host, port=port, user=user, password=password, zone=zoneName, client_user='another_user', client_zone='another_zone')

sess = iRODSSession(host=host, port=int(port), user=user, password=password, zone=zone)

try:
	obj = sess.data_objects.get("/" + zone + "/home/" + user + cnvFile)
	#refactoring exception?
except iExc.DataObjectDoesNotExist:
	print ("Object does not exist : " + cnvFile); exit(1)
except (ValueError, iExc.NetworkException):
	print ("Could not connect to specified host and port: " + host + ":" + port)
except iExc.CAT_INVALID_USER:
	print ("Invalid user: " + user); exit(1)
except iExc.CAT_INVALID_AUTHENTICATION:
	print ("Invalid password"); exit(1)
except iExc.CollectionDoesNotExist:
	print ("Collection does not exist : " + zone); exit(1)
	#autre??



###MAIN###


for line in metadataFile:
	if line!="\n":
		key,value=line.split("\t")
		value = value.rstrip()
		try:
			obj.metadata.add(key,value)
		except iExc.CATALOG_ALREADY_HAS_ITEM_BY_THAT_NAME:
			pass

# TODO: fichier avec bcp de metadata

metadataFile.close()
exit(0)

