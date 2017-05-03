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
	parser.add_argument ( '-vcf', dest = 'vcfFilename', required = 'True', help = 'Full path and name of your VCF file' )
	parser.add_argument ( '-xl', dest = 'excelFilename', required = 'True', help = 'Full path and name of your VCF file' )
	parser.add_argument ( '-exp', dest = 'idExperiment', default = '1', help = 'ID of your Experiment coming from NCBI\'s excel metadata ( default: %(default)s ) ' )
	#parser.add_argument ( '-vcfwd', dest = 'vcfWorkdir', default = '/home/ecamenen/Documents', help = 'Workdirectory of your VCF file ( default: your current one ) .' )
	#parser.add_argument ( '-xlwd', dest = 'excelWorkdir', default = '/home/ecamenen/Documents', help = 'Workdirectory of your excel file ( default: your current one ) .' )
	#TODO ?
	#parser.add_argument ( '-dwld', dest = 'ifDownload', help = 'Download the metada excel file for NCBI submission.' )
	args = parser.parse_args()
	return args

args = help()

if len ( sys.argv ) < 2:
	args.print_help()



###GLOBAL PARAMETERS###

#os.listdir('.')
#os.chdir('/home/ecamenen/Documents/')
#os.chdir(args.vcfWorkdir)
#vcfFile = vcf.Reader(open('example_CNV.vcf'))
#vcfFile = vcf.Reader(open('vcf_sample.vcf'))
vcfFile = vcf.Reader(open(args.vcfFilename, 'r'))
idExperiment = args.idExperiment

#ajouter curl pour catch d'erreur de co
#try :
#excelFilename = args.ifDownload
#os.system('wget -P '+ os.getcwd() + ' https://www.ncbi.nlm.nih.gov/core/assets/dbvar/files/dbVarSubmissionTemplate_v3.3.xlsx')
#excelWorkdir = os.getcwd()
#except:
#excelWorkdir = args.excelWorkdir
#finally:
excelFile = openpyxl.load_workbook(args.excelFilename)
#excelFile = openpyxl.load_workbook('dbVar4.xlsx')

sheet = excelFile.get_sheet_by_name('VARIANT CALLS')


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


##chr
def parseChr ( chrField ) :
	chr = re.search ( r"CHR(?P<chr>\w+)", chrField.upper() )
	if ( chr != None):
		if ( re.match ( r"0", chr.group ( 'chr' ) ) != None) :
			chr = re.sub ( r"0(?P<chr>\w+)", r"\g<chr>", chr.group ( 'chr' ) )
	else:
		chr = chrField
	return chr

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
	try: 
		return record.INFO [ 'SVLEN' ] [ cptCall ]
	except KeyError:
		if ( re.match ( r'^<(.)*>$', str ( record.ALT [ 0 ] ) ) == None ) :
			return len(record.REF) - len(record.ALT [ 0 ])
		else:
			return ''

def getOuterstop() :
		return record.POS + calculateCallLength() + 1




##insertion length

def roundCallLength ( callLength ) :
		return str ( abs( int ( round ( float ( callLength ) , 2 - len ( callLength ) ) ) ) )

#TODO: prévoir pour tous les ALT
#TODO: a faire pour SNP
def getInsertionLength() :
	if ( re.match ( r'^<(.)*>$', str ( record.ALT [ 0 ] ) ) != None ) :
		return '~' + roundCallLength ( str ( calculateCallLength() ) )
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
	parseChr (record.CHROM),
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
		print ('cptVar :' + str(cptVar))
		cptCall += 1
		print ('cptCall :' + str(cptCall))
		call = record.genotype ( callName )
		parsingCall(record, cptCall, cptVar)



####FOOT###

excelFile.save(args.excelFilename)
#excelFile.save('dbVar4.xlsx')
excelFile.close()
exit(0)
