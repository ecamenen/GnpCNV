# -*-coding:Utf-8 -*
'''Parsing a VCF file into an Excel metadata file used for NCBI submission'''


import os
import re
import sys
import vcf
import argparse
import openpyxl

###HELP###

#if len ( sys.argv ) < 2:
 #   print ( 'Please enter only one parameter: the name of your VCF file.' )

def help() :
	parser = argparse.ArgumentParser ( description = 'Parsing a VCF file into an Excel metadata file used for NCBI submission' )
	parser.add_argument ( '-vcf', dest = 'vcfFilename', required = 'True', help = 'Name of your VCF file' )
	parser.add_argument ( '-xl', dest = 'excelFilename', required = 'True', help = 'Name of your VCF file' )
	parser.add_argument ( '-exp', dest = 'idExperiment', default = '1', help = 'ID of your Experiment coming from NCBI\'s excel metadata ( default: %(default)s ) ' )
	parser.add_argument ( '-vcfwd', dest = 'vcfWorkdir', default = '/home/ecamenen/Documents', help = 'Workdirectory of your VCF file ( default: your current one ) .' )
	parser.add_argument ( '-xlwd', dest = 'excelWorkdir', default = '/home/ecamenen/Documents', help = 'Workdirectory of your excel file ( default: your current one ) .' )
	#parser.add_argument ( '-dwld', dest = 'ifDownload', help = 'Download the metada excel file for NCBI submission.' )
	args = parser.parse_args()
	return args

args = help()

if len ( sys.argv ) < 2:
	args.print_help()



###GLOBAL PARAMETERS###

#os.listdir('.')
#os.chdir('/home/ecamenen/Documents/')
#vcfFile = vcf.Reader(open('example_CNV.vcf'))
vcfFile = vcf.Reader(open(args.vcfWorkdir + '/' + args.vcfFilename, 'r'))
idExperiment = args.idExperiment

#ajouter curl pour catch d'erreur de co
#try :
#excelFilename = args.ifDownload
#os.system('wget -P '+ os.getcwd() + ' https://www.ncbi.nlm.nih.gov/core/assets/dbvar/files/dbVarSubmissionTemplate_v3.3.xlsx')
#excelWorkdir = os.getcwd()
#except:
excelFilename = args.excelFilename
excelWorkdir = args.excelWorkdir
#finally:
excelFile = openpyxl.load_workbook(args.excelWorkdir + '/' + args.excelFilename)
sheet = excelFile.get_sheet_by_name('VARIANT CALLS')

#excelFile = openpyxl.load_workbook('dbVar4.xlsx')

#TODO
listVariantType = (
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
)




###FUNCTIONS####


def setCell ( column, line, parameter ) :
	header = 4
	sheet [ column + str ( header + line ) ].value  = parameter




##assembly

def getAssembly() :
	try:
		return vcfFile.metadata [ 'reference' ]
	except KeyError:
		try:
			return vcfFile.metadata [ 'assembly' ] #else the url is taken
		except KeyError:
			return ''


##outerstop
#TODO: cas par defaut? END

def calculateCallLength() :
	return record.INFO [ 'SVLEN' ] [ cptCall ]

def getOuterstop() :
	try:
		#file.infos [ 'SVLEN' ]
		outerstop = record.POS + calculateCallLength() + 1
	except KeyError:
		outerstop = ''
	finally:
		return outerstop


##insertion length

def roundCallLength ( callLength ) :
		return str ( int ( round ( float ( callLength ) , 2 - len ( callLength ) ) ) )

#TODO: prévoir length neg pour insertion
def getInsertionLength() :
	if ( re.match ( r'^<(.)*>$', str ( record.ALT [ cptCall ] ) ) != None ) :
		return '~' + abs(roundCallLength ( str ( calculateCallLength() ) ))
	else:
		return ''


##copy number
#sh [ 'Q' + str ( 4 + cptVar ) ] = len ( record.ALT )

def searchCNPos () :
	cpt = -1
	for f in record.FORMAT.split ( ':' ) :
		cpt += 1
		if ( re.match ( r'CN', f ) != None ) :
			return cpt

def getCopyNumber() :
	try:
		return call.data [ searchCNPos () ]
	except TypeError:
		return ''


##zygosity
#TODO: taking account of '|' separator

def getZygosity () :
	if call.gt_type != None :
		if call.gt_type == 1 :
			return 'Heterozygous'
		else:
			return 'Homozygous'
	else :
		cptZygo = 0
		zygosity = call [ 'GT' ].split ( '/' ) #taking acount of polypoid case
		for z in zygosity:
			if z ==  '.' :
				cptZygo += 1
		if cptZygo == len ( zygosity ) :
			return ''
		else :
			return 'Hemizygous'




###MAIN###

def parsingCall(record, cptCall, cptVar) :
	#list(string.ascii_uppercase[:6])
	listColumn = ('A' , 'B', 'C', 'D', 'F', 'G', 'J', 'N', 'O', 'Q', 'U')
	listInputs = (
	cptVar,
	record.var_type,
	idExperiment,
	call.sample,
	getAssembly(),
	record.CHROM,
	record.POS,
	getOuterstop(),
	getInsertionLength(),
	getCopyNumber(),
	getZygosity()
	)
	for i in range(0 ,len(listColumn)):
		setCell(listColumn[i], cptVar, listInputs[i])


cptVar = 0

for record in vcfFile :
	cptCall = -1
	for callName in vcfFile.samples :
		cptVar += 1
		print(cptVar)
		cptCall += 1
		call = record.genotype ( callName )
		parsingCall(record, cptCall, cptVar)



####FOOT###

#excelFile.save(args.vcfWorkdir + '/' + args.vcfFilename)
excelFile.save('dbVar4.xlsx')
excelFile.close()
exit(0)