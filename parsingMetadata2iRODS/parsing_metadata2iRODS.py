# -*-coding:Utf-8 -*
"""A modulate that takes the metadata from an ad hoc file and associate them to a VCF file
"""

import os
import sys

os.chdir("/home/ecamenen/Documents")
namefile=sys.argv[1]
my_file=open(namefile, 'r')
output=""
cpt=0

for line in my_file:
	if line!="\n":
		key,value=line.split("\t")
		value = value.rstrip()
		cpt+=1
		if cpt!=1:
			output+=","		
		output+="{\"attribute\":\""+key+"\",\"value\":\""+value+"\"}"
	else:
		print(output)
		#os.system ("curl -u rods:rods -XPUT 'http://localhost:8080/irods-rest/rest/dataObject/tempZone/home/rods/test/test_new.csv/metadata' -d '{\"metadataEntries\":[" + output + "]}\'"
		exit(0)



#curl -u rods:rods -XPUT 'http://localhost:8080/irods-rest/rest/dataObject/tempZone/home/rods/test/test_new.csv/metadata' -d '{"metadataEntries":[{"attribute":"Name","value":"Robert"}]}'

