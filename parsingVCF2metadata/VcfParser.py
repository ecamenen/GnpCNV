# -*-coding:Utf-8 -*
'''
@dateCreation: 26/04/17
@author: INRA Versailles (URGI) - Etienne CAMENEN
@description:  Parsing a VCF file into an Excel metadata file used for NCBI submission
'''

import vcf, re, openpyxl

#Error from undefined workbook variable, works anyway.
class DbVarWriter(openpyxl.workbook.workbook.Workbook):
	
	def __init__(self, fileName):
		self.wb = openpyxl.load_workbook(fileName)
		self.sheet = self.wb.get_sheet_by_name('VARIANT CALLS')
		self.filename = fileName
		
	def write(self):
		self.wb.save(self.filename)
		self.close()
	
	#TODO: set the Excel format parameters (bold, text size) to avoid any format errors
	def setCell (self, column, line, parameter ) :
		header = 4
		self.sheet [ column + str ( header + line ) ].value  = parameter

		

###########################################
class VCFParser(vcf.parser.Reader):
	dbVar=''
	headerAlt=''
	
	def __init__(self, vcfFile, excelFilename, idExperiment):
		vcf.parser.Reader.__init__(self, fsock=vcfFile, filename=None, compressed=None,
		prepend_chr=False, strict_whitespace=False, encoding='ascii')
		self.idExperiment = idExperiment
		VCFParser.dbVar=DbVarWriter(excelFilename)
		VCFParser.headerAlt=self.getParsingHeaderAlt()
		self.version = self.getVCFversion ()
		
	def next(self) :
		record = vcf.parser.Reader.next(self)
		idExperiment = self.idExperiment
		vcfFile = self
		return Record2(record, vcfFile, idExperiment)
	
	def getVCFversion (self):
		version = re.search ( r"VCFv(?P<version>[\w.]+)*", self.metadata['fileformat'] )
		msg = 'this script is fitted for an older VCF version (v4.2)'
		if ( version != None):
			if ( float(version.group('version')) > 4.2) :
				print 'Warning: ' + msg
		else:
			print 'Warning: unknown version, ' + msg
	
	def getParsingHeaderAlt (self) :
		varTypeDict = {}
		if self.alts.values() :
			for id,desc in self.alts.values():
				if (re.match ( r'(.)*insertion(.)*', str ( desc.lower() ) ) != None) :
					if (re.match ( r'(.)*ALU(.)*', str ( desc.upper() ) ) != None) :
						varTypeDict[id] = 'Alu insertion'
					elif (re.match ( r'(.)*L(INE)*( )?1(.)*', desc.upper() ) != None) :
						varTypeDict[id] = 'LINE1 insertion'
					else :
						varTypeDict[id] = 'insertion'
				elif (re.match ( r'(.)*deletion(.)*', str ( desc.lower() ) ) != None) :
					varTypeDict[id] = 'deletion'
				elif (re.match ( r'(.)*duplication(.)*', str ( desc.lower() ) ) != None) :
					if (re.match ( r'(.)*tandem(.)*', str ( desc.lower() ) ) != None) :
						varTypeDict[id] = 'tandem duplication' #short a coder
					else :
						varTypeDict[id] = 'duplication'
				elif (re.match ( r'(.)*inversion(.)*', str ( desc.lower() ) ) != None) :
					varTypeDict[id] = 'inversion'
				elif (re.match ( r'(.)*copy number(.)*', str ( desc.lower() ) ) != None) :		
					varTypeDict[id] = 'copy number variation'
		return varTypeDict
	
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
				chr = chr.group ( 'chr' )
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
		Call2.cptVar += 1
		self.vcfFile = vcfFile
	
	def getVarType (self) :
		varTypeDict = VCFParser.headerAlt
		if (re.match ( r'^snp$', str ( self.site.var_type )) != None ) :
			if (re.match ( r'^tv$', str ( self.site.var_type )) != None or re.match ( r'^ts$', str ( self.site.var_type ) ) != None ) :
				varType = 'sequence alteration'				
			elif (re.match ( r'^ins$', str ( self.site.var_type ) ) != None ) :
				varType = 'insertion'
			else :
				varType = 'duplication'
		elif (re.match ( r'^indel$', str ( self.site.var_type )) != None ) :
			varType = 'indel'
		elif (re.match ( r'^sv$', str ( self.site.var_type )) != None ) :
			try :
				varType = varTypeDict[self.site.var_subtype]
			except (KeyError, TypeError) :
				varType = self.getParsingAlt()
		return varType
	
	def getParsingAlt (self) :
		if (re.match ( r'(.)*INS:ME:ALU(.)*', str(self.site.var_subtype) ) != None) :
				return 'Alu insertion'
		elif (re.match ( r'(.)*INS:ME:L1(.)*', str(self.site.var_subtype )) != None) :
				return 'LINE1 insertion'
		elif (re.match ( r'(.)*INS(.)*', str(self.site.var_subtype )) != None) :
				return 'insertion'
		elif (re.match ( r'(.)*DEL(.)*', str(self.site.var_subtype )) != None) :
			return 'deletion'
		elif (re.match ( r'(.)*DUP:TANDEM(.)*', str(self.site.var_subtype )) != None) :
			return  'tandem duplication' #short a coder		
		elif (re.match ( r'(.)*DUP(.)*', str(self.site.var_subtype )) != None) :
			return 'duplication'
		elif (re.match ( r'(.)*INV(.)*', str(self.site.var_subtype )) != None) :
			return  'inversion'
		elif (re.match ( r'(.)*CNV(.)*', str(self.site.var_subtype )) != None) :		
			return 'copy number variation'
		else :
			return ''
		
	def getZygosity ( self ) :
		if self.gt_type != None :
			if self.gt_type == 1 :
				return 'Heterozygous'
			else:
				return 'Homozygous'
		else :
			cptZygo = 0
			zygosity = self [ 'GT' ].split ( '/' ) #taking account of polypoid case
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
		if self.gt_type != 0:
			if self.calculateAlleleLength()!='':
				if ( re.match ( r'^<(.)*>$', str ( self.site.ALT [ 0 ] ) ) != None ) :
					return '~' + self.roundCallLength ( str ( self.calculateAlleleLength() ) )
				else:
					return str ( abs( self.calculateAlleleLength() ) )
			else:
				return ''
		else:
			return ''
	
	#TODO: envisager possibilite de prendre en compte tag INFO CISPOS et CISEND	
	def roundCallLength (self, callLength) :
			return str ( abs( int ( round ( float ( callLength ) , 2 - len ( callLength ) ) ) ) )
		
	def calculateAlleleLength(self):
		length = 0
		if self.gt_type != 0 :
			alleles = self[ 'GT' ].split ( '/' )
			for a in alleles :
				if (a != '0' and a != '.'):
					try:
						a = int(a) -1
						result = self.calculateLength(a)
						if result < 0 : # cas deletion 
							if length > result :
								length = result
						else:
							if length < result :
								length = result
					except ValueError:
						return '' # cas GT=string, p.ex 'na', erreur a la convertion en int
			return length
		else:
			return len( self.site.REF )
	
	def calculateLength (self, cptAllele) :
		try:
			return self.site.INFO [ 'SVLEN' ] [ cptAllele ]
		except KeyError:
			if ( re.match ( r'^<(.)*>$', str ( self.site.ALT [ cptAllele ] ) ) == None ) :
				return len( self.site.REF ) - len( self.site.ALT [ cptAllele ] )
			else:
				return ''
			
	def getOuterstop (self) :
		if self.calculateAlleleLength()!='':
			return self.site.POS + self.calculateAlleleLength()
		else:
			return ''
	
	def parsingCall(self) :
		listColumn = ('A' , 'B', 'C', 'D', 'F', 'G', 'J', 'N', 'O', 'Q', 'U')
		listInputs = (
		Call2.cptVar,
		self.getVarType(),
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
	
	#TODO: sequence variant
	#TODO: ???? variant region ID(evidence, support, support count: probe) (log2)
	#TODO: breakpoint, contig
	
	#genome du mais, vigne ?
	#champ propre pour contigs = assemly pseudomolecultype( chromosome, scafold, contig)
				
#if __name__ == "__main__":
#	pass
