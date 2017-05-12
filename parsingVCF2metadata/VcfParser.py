# -*-coding:Utf-8 -*
'''
@dateCreation: 26/04/17
@author: INRA Versailles (URGI) - Etienne CAMENEN
@description:  Parsing a VCF file into an Excel metadata file used for NCBI submission
'''

import vcf, re, openpyxl

#Error from undefined workbook variable works anyway.
class DbVarWriter(openpyxl.workbook.workbook.Workbook):
	
	def __init__(self, fileName):
		self.wb = openpyxl.load_workbook(fileName)
		self.sheet = self.wb.get_sheet_by_name('VARIANT CALLS')
		self.filename = fileName
		
	def write(self):
		self.wb.save(self.filename)
		self.close()
	
	#TODO: formatting
	def setCell (self, column, line, parameter ) :
		header = 4
		self.sheet [ column + str ( header + line ) ].value  = parameter

		

###########################################
#TODO: Print warning if VCF != 4.2
class VCFParser(vcf.parser.Reader):
	dbVar=''
	def __init__(self, vcfFile, excelFilename, idExperiment):
		vcf.parser.Reader.__init__(self, fsock=vcfFile, filename=None, compressed=None,
		prepend_chr=False, strict_whitespace=False, encoding='ascii')
		self.idExperiment = idExperiment
		VCFParser.dbVar=DbVarWriter(excelFilename)
		
	def next(self) :
		record = vcf.parser.Reader.next(self)
		idExperiment = self.idExperiment
		vcfFile = self
		return Record2(record, vcfFile, idExperiment)
	
	def getAssembly(self) :
		try:
			return self.metadata [ 'reference' ]
		except KeyError:
			try:
				return ''.join(self.metadata [ 'assembly' ]) #else the url is taken
			except KeyError:
				return ''
			
	def parseVCF(self) :
		for record in self :
			for call in record:
				call.parsingCall()


###########################################
class Record2 ( vcf.model._Record ):
	
	def __init__ ( self, record, vcfFile, idExperiment ):
		vcf.model._Record.__init__(self, record.CHROM, record.POS, record.ID,record.REF, record.ALT, record.QUAL, record.FILTER, record.INFO, record.FORMAT, None, record.samples)
		self.vcfFile = vcfFile
		self.cptCall = -1
		self.idExperiment = idExperiment
		self.position = 0
		self.call = self.samples [ 0 ]
		
	def __iter__ ( self ):
		return self
	
	def next ( self ):
		if self.position == len ( self.samples ):
			raise StopIteration
		call = self.samples [ self.position ]
		self.position += 1
		idExperiment = self.idExperiment
		self.cptCall += 1
		cptCall = self.cptCall
		vcfFile = self.vcfFile
		record = self
		return Call2(call, record, vcfFile, idExperiment, cptCall)
	
	def parseChr ( self ) :
		chr = re.search ( r"CHR(?P<chr>\w+)", self.CHROM.upper() )
		if ( chr != None):
			if ( re.match ( r"0", chr.group ( 'chr' ) ) != None) :
				chr = re.sub ( r"0(?P<chr>\w+)", r"\g<chr>", chr.group ( 'chr' ) )
		else:
			chr = self.CHROM
		return chr
	

###########################################
class Call2(vcf.model._Call):
	
	cptVar = 0
	
	def __init__(self, call, record, vcfFile, idExperiment, cptCall):
		vcf.model._Call.__init__(self, record, call.sample, call.data)
		self.idExperiment = idExperiment
		self.cptCall = cptCall
		Call2.cptVar +=1
		self.vcfFile = vcfFile
		
	def getZygosity ( self ) :
		if self.gt_type != None :
			if self.gt_type == 1 :
				return 'Heterozygous'
			else:
				return 'Homozygous'
		else :
			cptZygo = 0
			zygosity = self [ 'GT' ].split ( '/' ) #taking acount of polypoid case
			for z in zygosity:
				if z ==  '.' :
					cptZygo += 1
			if cptZygo == len ( zygosity ) :
				return ''
			else :
				return 'Hemizygous'
			
	def searchCNPos ( self ) :
		cpt = -1
		for f in self.site.FORMAT.split ( ':' ) :
			cpt += 1
			if ( re.match ( r'CN', f ) != None ) :
				return cpt
			
	def getCopyNumber ( self ) :
		try:
			return self.data [ self.searchCNPos () ]
		except TypeError:
			return ''
		
	def getInsertionLength ( self ) :
		if ( re.match ( r'^<(.)*>$', str ( self.site.ALT [ 0 ] ) ) != None ) :
			return '~' + self.roundCallLength ( str ( self.calculateCallLength() ) )
		else:
			return str ( abs( self.calculateCallLength()) )
		
	def roundCallLength (self, callLength) :
			return str ( abs( int ( round ( float ( callLength ) , 2 - len ( callLength ) ) ) ) )
		
	def calculateCallLength (self) :
		try:
			return self.site.INFO [ 'SVLEN' ] [ self.cptCall ]
		except KeyError:
			if ( re.match ( r'^<(.)*>$', str ( self.site.ALT [ 0 ] ) ) == None ) :
				return len( self.site.REF ) - len( self.site.ALT [ 0 ] )
			else:
				return ''
			
	def getOuterstop (self) :
			return self.site.POS + self.calculateCallLength() + 1
	
	def parsingCall(self) :
		listColumn = ('A' , 'B', 'C', 'D', 'F', 'G', 'J', 'N', 'O', 'Q', 'U')
		listInputs = (
		Call2.cptVar,
		self.site.var_type,
		self.idExperiment,
		self.sample,
		self.vcfFile.getAssembly(),
		self.site.parseChr (),
		self.site.POS,
		self.getOuterstop(),
		self.getInsertionLength(),
		self.getCopyNumber(),
		self.getZygosity()
		)
		for i in range(0 ,len(listColumn)):
			VCFParser.dbVar.setCell(listColumn[i], Call2.cptVar, listInputs[i])
	
	#TODO: OK >> sequence variant (buf if there is variant called 1/2, which one one take?)
	#TODO: ???? variant region ID, ref copie number, origin ????, (evidence, support, support count: probe) (log2)
	#TODO: breakpoint, contig, 
	#TODO: ajouter parametre arg script: numero sampleset, par defaut ''
			
#if __name__ == "__main__":
#	pass