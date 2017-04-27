# -*-coding:Utf-8 -*
"""Parsing a VCF file into an Excel metadata file used for NCBI submission"""


import os
import re
import sys
import argparse
import openpyxl

###HELP###

#if len ( sys.argv ) < 2:
 #   print ( "Please enter only one parameter: the name of your VCF file." )

def help() :
	parser = argparse.ArgumentParser ( description = "Parsing a VCF file into an Excel metadata file used for NCBI submission" )
	parser.add_argument ( "--vcf", dest = "vcfFilename", required = "True", help = "Name of your VCF file" )
	parser.add_argument ( "--excel", dest = "excelFilename", required = "True", help = "Name of your VCF file" )
	parser.add_argument ( "--exp", dest = "idExperiment", default = "1", help = "ID of your Experiment coming from NCBI's excel metadata ( default: %(default)s ) " )
	parser.add_argument ( "--vcfWorkdir", default = "/home/ecamenen/Documents/", help = "Workdirectory of your VCF file ( default: your current one ) ." )
	parser.add_argument ( "-excelWorkdir", default = "/home/ecamenen/Documents/", help = "Workdirectory of your excel file ( default: your current one ) ." )
	parser.add_argument ( "--download", dest = "ifDownload", help = "Workdirectory of your excel file ( default: your current one ) ." )
	args = parser.parse_args()
	return args

args = help()

if len ( sys.argv ) < 2:
	args.print_help()



###PARAMETERS###

#os.listdir('.')
#os.chdir()
excelFile = openpyxl.load_workbook(args.vcfWorkdir + args.vcfFilename)
sheet = excelFile.get_sheet_by_name('VARIANT CALLS')
idExperiment = args.idExperiment

#ajouter curl pour catch d'erreur de co
try :
	excelFilename = args.ifDownload
	os.system('wget -P '+ os.getcwd() + ' https://www.ncbi.nlm.nih.gov/core/assets/dbvar/files/dbVarSubmissionTemplate_v3.3.xlsx')
	excelWorkdir = os.getcwd()
except:
	excelFilename = args.excelFilename
	excelWorkdir = args.excelWorkdir
finally:
	vcfFile = open(excelWorkdir + excelFilename, 'r')


###FUNCTION####

def parseChr ( chrField ) :
	chr = re.search ( r"CHR (?P<chr>\w+)", chrField.upper() )
	if ( re.match ( r"0", chr.group ( 'chr' ) ) ) :
		chr = re.sub ( r"0 (?P<chr>\w+)", r"\g<chr>", chr.group ( 'chr' ) )
	return chr

###MAIN###

cptVar = 0

for record in vcfFile :
	cptCall = -1
	for callName in vcfFile.samples :
		cptVar += 1
		cptCall += 1
		call = record.genotype ( callName )
		parsingCall(record, cptCall)

####FOOT###

vcfFile.save(vcfFilename)
vcfFile.close()
exit(0)







listVariantType = [
'complex substitution',
'copy number gain',
'copy number loss',
'copy number variation',
'deletion',
'duplication',
'indel',
'insertion',
'interchromosomal translocation',
'intrachromosomal translocation',
'inversion',
'mobile element insertion',
'Alu insertion',
'LINE1 insertion',
'SVA insertion',
'novel sequence insertion',
'sequence alteration',
'short tandem repeat variation',
'tandem duplication'
]

def parsingCall(record, call):
	#list(string.ascii_uppercase[:6])
	listColumn = ('A' , 'B', 'C', 'D', 'F', 'G', 'J', 'N', 'O', 'Q', 'U')
listInputs = (cptVar, record.var_type, idExperiment, call.sample, setAssembly(), 
	record.CHROM, record.POS, setOuterstop(), setInsertionLength(), setCopyNumber(),
	)
	for i in range(0 ,len(listColumn)):
		setCell(listColumn[i], call, listInputs[i])

def setCell ( column, line, parameter ) :
	header = 4
	sheet [ column + str ( header + line ) ].value  = parameter

##call_id
setCell ( 'A', cptCall, cptVar )

##call_type
#TODO
setCell ( 'B', cptCall, record.var_type )

##experiment id
setCell ( 'C', cptCall, idExperiment )

##sample id
setCell ( 'D', cptCall, call.sample )

##assembly

def setAssembly():
	try:
		assembly = vcfFile.metadata [ 'reference' ]
	except KeyError:
		try:
			assembly = vcfFile.metadata [ 'assembly' ] #else the url is taken
		except KeyError:
			assembly = ''

	return assembly

setCell ( 'F', cptCall, assembly )


##chrom
setCell ( 'G', cptCall, record.CHROM )

##start
#record.affected_start + 1
setCell ( 'J', cptCall, record.POS )

##outerstop
#TODO: cas par defaut? END

def calculateCallLength():
	return record.INFO [ 'SVLEN' ] [ cptCall ]

def setOuterstop():
	try:
		#file.infos [ 'SVLEN' ]
		outerstop = record.POS + calculateCallLength() + 1
	except KeyError:
		outerstop = ''
	finally:
		return outerstop

setCell ( 'N', cptCall, outerstop )

##insertion length

def roundCallLength ( callLength ) :
		return str ( int ( round ( float ( callLength ) , 2 - len ( callLength ) ) ) )

def setInsertionLength() :
	if ( re.match ( r"^<(.)*>$", str ( record.ALT [ cptCall ] ) ) != None ) :
		return '~' + roundCallLength ( str ( calculateCallLength() ) )
	else:
		return ''


setCell ( 'O', cptCall, insertionLength() )


##copy number
#sh [ 'Q' + str ( 4 + cptVar ) ] = len ( record.ALT )

def getFormat():
	return record.FORMAT.split ( ':' )

def searchGQPos () :
	cpt = -1
	for f in getFormat():
		cpt += 1
		if ( re.match ( r"CN", f ) != None ) :
			return cpt

def setCopyNumber():
	try:
		return call.data [ searchCNPos () ]
	except KeyError:
		return ''


##zygosity

if call.gt_type != None :
	if call.gt_type == 1 :
		zygo = "Heterozygous"
	else:
		zygo = "Homozygous"
else :
	zygosity = call [ 'GT' ].split ( '/' ) #taking acount of polypoid case
	for z in zygosity:
		if z = =  '.' :
			cptZ += 1
		if cptZ == len ( zygosity ) :
			zygo = ''
		else :
			zygo = "Hemizygous"


setCell ( 'U', cptCall, zygo)





























########









for line in vcf:
	if ( re.match ( r"^#", line ) != None ) :
		match = re.search ( r"##assembly=(?P<assembly>\w+)", line )
		if ( match != None ) :
			assembly = match.group ( 'assembly' )
		elif:
			match = re.search ( r"##reference=(?P<ref>\w+)", line )
			if ( match != None ) :
				assembly = match.group ( 'ref' )
	else:
		line = re.split ( '\s{1, }', test )
		cptVar += 1
		sh [ 'A' + str ( 4 + cptVar ) ].value =
		for elt in line:
			sh [ 'G' + str ( 4 + cptVar ) ].value = line [ 1 ]
			sh [ 'J' + str ( 4 + cptVar ) ].value = line [ 2 ]
			if ( elt != '.' ) :

	else:
		
print ( cptVar )
headers = line [ 9: ]

#print ( 'Error: unexpected VCF format' )
#A FAIRE: if/else a inverse pour diminuer complexité



