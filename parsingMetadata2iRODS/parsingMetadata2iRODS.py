# # -*-coding:Utf-8 -*
"""A module that takes the metadata from an ad hoc file and associate them to a VCF file"""

import os, sys, argparse
from irods.session import iRODSSession
from irods import exception as iExc
reload(sys)
sys.setdefaultencoding('utf8')

###HELP###


def help():
	parser = argparse.ArgumentParser(description="A module that takes the metadata from an ad hoc file and associate them to a VCF file")
	parser.add_argument("-c", dest="filePath", required="True", help="the path of your cnv file (ex: /test/test.csv)")
	parser.add_argument("-m", dest="metadataName", default="/metadata.csv", help="the name of your metadata file (default: %(default)s)")
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
filePath = args.filePath
user=args.user
password = args.password
zone = args.zone
port = args.port
host = args.host


#getCollPath(filePath)
listPath = filePath.split("/")
listPath.pop()
collPath="/".join(listPath)


###MAIN###

#openSessioniRODS(self,host,port, user, password)
try:
	sess = iRODSSession(host=host, port=int(port), user=user, password=password, zone=zone)
except iExc.CAT_INVALID_USER:
	print ("Invalid user: " + user); exit(0)
except iExc.CAT_INVALID_AUTHENTICATION:
	print ("Invalid password"); exit(0)
except (ValueError, iExc.NetworkException):
	print ("Could not connect to specified host and port: " + host + ":" + port)


#getCollection(collPath)
try:
	coll = sess.collections.get(collPath)
except iExc.CollectionDoesNotExist:
	print ("Collection does not exist : " + zone); exit(0)


#metadataFileExist(collPath, metadataName)
try:
	metadata=sess.data_objects.get(collPath + args.metadataName)
except iExc.DataObjectDoesNotExist:
	print ("There is any metadata file in your folder !"); exit(0)


#testEmptyFolder(coll)
try:
     assert len(coll.data_objects) > 1
except AssertionError:
     print ("There is no other data files in this repository !"); exit(0)


#removeMetadata(coll)
for obj in coll.data_objects:
	obj.metadata.remove_all()


#parsingMetadata(metadata, coll)
with metadata.open('r+') as metadataFile:
	for line in metadataFile:
		if line!="\n":
			key,value=line.split("\t")
			value = value.rstrip()
			for obj in coll.data_objects:
				if obj.name != 'metadata.csv':
					try:
						obj.metadata.add(key,value)
					except iExc.CATALOG_ALREADY_HAS_ITEM_BY_THAT_NAME:
						print ("Item already in database ! Key: " + key + "; Value: " + value + ".")

#deleteMetadataFile(metadata)
#metadata.unlink(force=True)

exit(0)