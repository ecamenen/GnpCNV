# -*-coding:Utf-8 -*

import os, sys, re
reload(sys)
sys.setdefaultencoding('utf8')

def parseChr ( chrField ) :
	chr = re.search ( r"CHR(?P<chr>\w+)", chrField.upper() )
	if ( chr != None):
		if ( re.match ( r"0", chr.group ( 'chr' ) ) != None) :
			chr = re.sub ( r"0(?P<chr>\w+)", r"\g<chr>", chr.group ( 'chr' ) )
		else:
			chr = chr.group ( 'chr' )
	else:
		chr = chrField
	return chr

def MEparse ( ME) :
	if  ME != 'na':
		return ";METYPE=" + ME + ';MECLASS=' + getClassME (ME)
	else:
		return ''

def getClassME (ME):
	class1 = ['SINE', 'N>80%', 'LINE L1']; class2 = ['Class II unknown', 'Helitron']
	if ((ME in class1) | (re.search ( r"LTR.",ME) != None)):
		return 'Classe I'
	elif ((ME in class2) | (re.search ( r"TIR.",ME) != None)):
		return 'Classe II'
	else:
		return 'Undefined'

def NAparse ( values):
	try:
		if values[14].rstrip() != '':
			id = ";GENEID=" +  values[14]
		else:
			id =''
	except IndexError:
		id =''
	try:
		if values[15].rstrip() != '':
			desc = ";BLAST2GO=" +  values[15].rstrip()
		else:
			desc =''
	except IndexError:
		desc =''	
	return id + desc


def INSLEN(values):
	alt_length = int(values[3])
	ref_length = int(values[4])
	if(alt_length!=1 and ref_length!=1):
		return ';INSLEN=' + str(alt_length)
	return ''

def calculateLength(values):
	return int(values[3])-int(values[4])

def ALT(line2, alt_length):
	if alt_length==1:
		return line2[0]
	else:
		return '.'

infile=open('/home/ecamenen/Documents/test.vcf', 'r')
#infile1=open('/home/ecamenen/Documents/test3.txt', 'r')
values = []
for line in infile:
	if line!="\n":
		values=line.split("\t")
		os.system('sudo /home/ecamenen/bin/bin/samtools faidx /home/ecamenen/bin/JBrowse-1.12.3/Ptrichocarpa_210.fa ' +  values[0] + ':' + values[1] + '-' + values[2] + '>> /var/www/html/jbrowse/JBrowse-1.12.3/data/REF.fa')
	
			


os.system('awk \'/^>/ {printf("\n");next; } { printf("%s",$0);}  END {printf("\n");}\' < /home/ecamenen/bin/JBrowse-1.12.3/REF.fa | tail -n +2  > /home/ecamenen/bin/JBrowse-1.12.3/REF2.fa')



vcfContent='##fileformat=VCFv4.2\n'
vcfContent+='##fileDate=20170721\n'
vcfContent+='##source=https://www.ncbi.nlm.nih.gov/pubmed/27499133\n'
vcfContent+='##assembly=Populus trichocarpa v3.0\n'
vcfContent+='##INFO=<ID=END,Number=1,Type=Integer,Description="End position of the variant described in this record">\n'
vcfContent+='##INFO=<ID=SVLEN,Number=-1,Type=Integer,Description="Difference in length between REF and ALT alleles">\n'
vcfContent+='##INFO=<ID=SVTYPE,Number=1,Type=String,Description="Type of structural variant">\n'
vcfContent+='##INFO=<ID=METYPE,Number=1,Type=String,Description="Type of mobile element">\n'
vcfContent+='##INFO=<ID=MECLASS,Number=1,Type=String,Description="Class of mobile element">\n'
vcfContent+='##INFO=<ID=GENEID,Number=1,Type=String,Description="Gene ID in Phytozome database">\n'
vcfContent+='##INFO=<ID=BLAST2GO,Number=1,Type=String,Description="Gene Ontologt terms obtained by BLAST2GO tool and mapped with Plant GO-Slim">\n'
vcfContent+='##INFO=<ID=INSLEN,Number=1,Type=String,Description="Length of insertion">\n'
vcfContent+='##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">\n'
vcfContent+='##SAMPLE=<ID=Nisqually-1,Genomes=Nisqually-1,Description="Populus trichocarpa">\n'
vcfContent+='##SAMPLE=<ID=L150-089,Genomes=L150-089,Description="Populus deltoides">\n'
vcfContent+='##SAMPLE=<ID=L155-079,Genomes=L155-079,Description="Populus deltoides">\n'
vcfContent+='##SAMPLE=<ID=BDG,Genomes=BDG,Description="Populus nigra">\n'
vcfContent+='##SAMPLE=<ID=71077-308,Genomes=71077-308,Description="Populus nigra">\n'
vcfContent+='##SAMPLE=<ID=Poli,Genomes=Poli,Description="Populus nigra">\n'
vcfContent+='##SAMPLE=<ID=BEN3,Genomes=BEN3,Description="Populus nigra">\n'
vcfContent+='#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\tNisqually-1\tL150-089\tL155-079\tBDG\tBEN3\tPOLI\t71077-308\n'

infile=open("/var/www/html/jbrowse/JBrowse-1.12.3/data/test4.vcf", 'r')
outfile=open('/var/www/html/jbrowse/JBrowse-1.12.3/data/Pinosioetal2016.vcf', 'w')
cpt=0
values = []
while cpt<18475:
	line = next(infile)
	values=line.split("\t")
	values[16]=values[16].rstrip()
	cpt+=1
	vcfContent+="\t".join(values[:2]) + "\tPtri3." + parseChr(values[0]) + "." + values[1] + "\t" + values[16] + '\t' + ALT(values[16],int(values[3])) + "\t.\t.\tSVTYPE=" + values[5] + ";END=" + values[2] + ";SVLEN=" + str(int(values[3])-int(values[4])) + INSLEN(values) + MEparse(values[6]) + NAparse(values) + "\tGT\t" + '\t'.join(values[7:14]) + '\n'

outfile.write(vcfContent)