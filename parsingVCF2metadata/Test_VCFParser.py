# -*-coding:Utf-8 -*
'''
@dateCreation: 05/05/17
@author: INRA Versailles (URGI) - Etienne CAMENEN
@description:  Parsing a VCF file into an Excel metadata file used for NCBI submission
'''

import os, shutil, unittest, openpyxl
from VcfParser import *


class Test(unittest.TestCase):
       
    def setUp(self):
        os.makedirs('./temp')
        self._vcfFile = './temp/dummyVCF.vcf'
        self._excelFile = './temp/dummyExcel.xlsx'
        
    def tearDown(self):
        shutil.rmtree('./temp')
        
    def writeDummyExcel(self):
        #listCol=list(string.ascii_uppercase) + ['A' + elt for elt in string.ascii_uppercase[:18]]
        listHeaders = ["variant_call_id" , "variant_call_type" , "experiment_id" , "sample_id" , "sampleset_id" , "assembly" , "chr" , "contig" , "outer_start" , "start" , "inner_start" , "inner_stop" , "stop" , "outer_stop" , "insertion_length" , "variant_region_id" , "copy_number" , "ref_copy_number" , "description" , "validation" , "zygosity" , "origin" , "phenotype" , "alt_status" , "assembly_" , "from_chr" , "from_coord" , "from_strand" , "to_chr" , "to_coord" , "to_strand" , "mutation_id" , "mutation_order" , "mutation_molecule" , "external_links" , "evidence" , "sequence" , "support" , "support_count" , "log2_value" , "5'_outer_flank" , "5'_inner_flank" , "3'_inner_flank" , "3'_outer_flank"]
        dummyExcel = openpyxl.Workbook(write_only=True)
        dummySheet = dummyExcel.create_sheet('VARIANT CALLS')
        for i in range(0 ,3):
            dummySheet.append(['' for j in range(0, len(listHeaders))])
        dummySheet.append(listHeaders)
        dummySheet.append(['1', 'sv', '1', 'NA00001', '', '1000Genomes', '1', '', '', '2827693', '', '', '', '2827628', '', '', '', '', '', '', 'Homozygous', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''])
        dummySheet.append(['2', 'sv', '1', 'NA00001', '', '1000Genomes', '2', '', '', '321682', '', '', '', '321578', '~100', '', '', '', '', '', 'Heterozygous', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''])
        dummySheet.append(['3', 'sv', '1', 'NA00001', '', '1000Genomes', '2', '', '', '14477084', '', '', '', '14476788', '~300', '', '', '', '', '', 'Hemizygous', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''])
        dummySheet.append(['4', 'sv', '1', 'NA00001', '', '1000Genomes', '3', '', '', '9425916', '', '', '', '9431944', '~6000', '', '', '', '', '', 'Homozygous', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''])
        dummySheet.append(['5', 'sv', '1', 'NA00001', '', '1000Genomes', '3', '', '', '12665100', '', '', '', '12686201', '~21000', '', '3', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''])
        dummySheet.append(['6', 'sv', '1', 'NA00001', '', '1000Genomes', '4', '', '', '18665128', '', '', '', '18665205', '~76', '', '5', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''])
        dummyExcel.save(self._excelFile)
        dummyExcel.close()
        
    def writeDummyVCF(self, boolReferenceFile = True, reference='1000Genomes', assembly='http://urlAssembly.com', boolALTHeaders = True, version = '4.0'):
        dummyVCF=open(self._vcfFile, 'w')
        dummyVCF.write('##fileformat=VCFv' + version + '\n')
        if boolReferenceFile == True :
            dummyVCF.write('##reference=' + reference + '\n')
        if boolALTHeaders == True :
            dummyVCF.write('##ALT=<ID=DEL,Description="Deletion">\n')
            dummyVCF.write('##ALT=<ID=DEL:ME:ALU,Description="Deletion of ALU element">\n')
            dummyVCF.write('##ALT=<ID=DEL:ME:L1,Description="Deletion of L1 element">\n')
            dummyVCF.write('##ALT=<ID=DUP,Description="Duplication">\n')
            dummyVCF.write('##ALT=<ID=DUP:TANDEM,Description="Tandem Duplication">\n')
            dummyVCF.write('##ALT=<ID=INS,Description="Insertion of novel sequence">\n')
            dummyVCF.write('##ALT=<ID=INS:ME:ALU,Description="Insertion of ALU element">\n')
            dummyVCF.write('##ALT=<ID=INS:ME:L1,Description="Insertion of L1 element">\n')
            dummyVCF.write('##ALT=<ID=INV,Description="Inversion">\n')
            dummyVCF.write('##ALT=<ID=CNV,Description="Copy number variable region">\n')
        dummyVCF.write('##assembly=' + assembly + '\n')
        dummyVCF.write('#CHROM  POS   ID  REF ALT   QUAL  FILTER  INFO  FORMAT  NA00001\n')
        dummyVCF.write('1 2827693   . CCGTGGATGCGGGGACCCGCATCCCCTCTCCCTTCACAGCTGAGTGACCCACATCCCCTCTCCCCTCGCA  C . PASS  SVTYPE=DEL;END=2827680;BKPTID=Pindel_LCS_D1099159;HOMLEN=1;HOMSEQ=C GT:GQ 1/1:13.9\n')
        dummyVCF.write('9311_chr02 321682    . T <DEL>   6 PASS    IMPRECISE;SVTYPE=DEL;END=321887;SVLEN=-105;CIPOS=-56,20;CIEND=-10,62  GT:GQ 0/1:12\n')
        dummyVCF.write('2 14477084  . C <DEL:ME:ALU>  12  PASS  IMPRECISE;SVTYPE=DEL;END=14477381;SVLEN=-297;MEINFO=AluYa5,5,307,+;CIPOS=-22,18;CIEND=-12,32  GT:GQ 1/1/.:12\n')
        dummyVCF.write('3 9425916   . C <INS:ME:L1> 23  PASS  IMPRECISE;SVTYPE=INS;END=9425916;SVLEN=6027;CIPOS=-16,22;MIINFO=L1HS,1,6025,- GT:GQ 1/1:15\n')
        dummyVCF.write('3 12665100  . A <DUP>   14  PASS  IMPRECISE;SVTYPE=DUP;END=12686200;SVLEN=21100;CIPOS=-500,500;CIEND=-500,500   GT:GQ:CN:CNQ  ./.:0:3:16.2\n')
        dummyVCF.write('4 18665128  . T <DUP:TANDEM>  11  PASS  IMPRECISE;SVTYPE=DUP;END=18665204;SVLEN=76;CIPOS=-10,10;CIEND=-10,10  GT:GQ:CN:CNQ  ./.:0:5:8.3\n')
        dummyVCF.close()
    
    def readExcel(self, excelName):
        wb = openpyxl.load_workbook(self._excelFile)
        sheet = wb.get_sheet_by_name('VARIANT CALLS')
        multiple_cells = sheet['A4':'U10']
        parsing = ''
        line = ''
        print '\n'
        for row in multiple_cells:
            line =''
            for cell in row:
                if cell.value != None:
                    line += cell.value + '\t'
                else:
                    line += '\t'
            parsing+=line + '\n'
            #print line
        return parsing
    
    def createFiles(self, boolReferenceFile = True, observedReference='1000Genomes', expectedAssembly='1000Genomes', boolALTHeaders = True, version = '4.0'):
        self.writeDummyExcel()
        self.writeDummyVCF(boolReferenceFile, observedReference, 'http://urlAssembly.com', boolALTHeaders, version)
        return VCFParser(open(self._vcfFile), self._excelFile, 1)
    
    def getRecord(self,  timeNext=1, boolALTHeaders = True):
        iVcfParser = self.createFiles(boolALTHeaders = boolALTHeaders)
        for i in range(0, timeNext):
            record = next(iVcfParser)
        #print record
        return record

    def getCall(self, timeNextRecord = 1, timeNextCall=1, boolALTHeaders = True):
        record = self.getRecord(timeNextRecord, boolALTHeaders)
        for i in range(0, timeNextCall):
            call = next(record)
        #print call
        return call
        
    def test_VCF_getVersion (self):
        iVcfParser = self.createFiles()
        iVcfParser = self.createFiles(version='4.2')
        iVcfParser = self.createFiles(version='5')
        iVcfParser = self.createFiles(version='')

        
    def VCF_getAssembly(self, boolReferenceFile = True, observedReference='1000Genomes', expectedAssembly='1000Genomes'):
        iVcfParser = self.createFiles(boolReferenceFile, observedReference, expectedAssembly)
        parsedAssembly = iVcfParser.getAssembly()
        #print parsedAssembly
        self.assertEquals(parsedAssembly, expectedAssembly)

    def test_VCF_getAssembly(self):
        self.VCF_getAssembly()
        self.VCF_getAssembly(boolReferenceFile = False, expectedAssembly='http://urlAssembly.com')
        self.VCF_getAssembly(observedReference='FalseRef', expectedAssembly='FalseRef')
            
    def record_parseChr(self, timeNext=1, expectedChr=1):
        record = self.getRecord(timeNext)
        parsedChr = record.parseChr()
        #print parsedChr
        self.assertEquals(parsedChr, str(expectedChr))
    
    def test_record_parseChr(self):
        self.record_parseChr()
        self.record_parseChr(2, 2)
        
    def call_getZygosity(self, timeNextRecord = 1, expectedZygosity='Homozygous', timeNextCall = 1):  
        call=self.getCall(timeNextRecord,timeNextCall)
        parsedZygosity=call.getZygosity()
        #print parsedZygosity
        self.assertEquals(parsedZygosity, expectedZygosity)
        
    def test_call_getZygosity(self):
        self.call_getZygosity()
        self.call_getZygosity(2, 'Heterozygous')
        self.call_getZygosity(3, 'Hemizygous') #and polyploidy case
        self.call_getZygosity(5,'')
    
    def test_call_getCopyNumber(self, timeNextRecord = 5, expectedCN=3, timeNextCall = 1):
        call=self.getCall(timeNextRecord,timeNextCall)
        parsedCN=call.getCopyNumber()
        #print parsedCN
        self.assertEquals(parsedCN, expectedCN)
        
    def call_getInsertionLength(self, timeNextRecord = 1, expectedInsertionLength=69, timeNextCall = 1):
        call=self.getCall(timeNextRecord,timeNextCall)
        parsedInsertionLength=call.getInsertionLength()
        #print parsedInsertionLength
        self.assertEquals(parsedInsertionLength, str(expectedInsertionLength))
    
    def test_call_getInsertionLength(self):
        #TODO: absolute or not ?
        self.call_getInsertionLength()
        self.call_getInsertionLength(2,'~100')
        self.call_getInsertionLength(3,'~300') # '.' case and polyploidy
        
    def call_calculateAlleleLength(self, timeNextRecord = 1, expectedLength=69, timeNextCall = 1):
        call=self.getCall(timeNextRecord,timeNextCall)
        parsedLength=call.calculateAlleleLength()
        #print parsedLength
        self.assertEquals(parsedLength, expectedLength)
        
    def test_call_calculateAlleleLength(self):
        self.call_calculateAlleleLength()
        self.call_calculateAlleleLength(2,-105)
        
    def call_getOuterstop(self, timeNextRecord = 1, expectedOuterstop = 2827763, timeNextCall = 1):
        call=self.getCall(timeNextRecord,timeNextCall)
        parsedOuterstop=call.getOuterstop()
        #print parsedOuterstop
        self.assertEquals(parsedOuterstop, expectedOuterstop)
        
    def test_call_getOuterstop(self):
        self.call_getOuterstop()
        self.call_getOuterstop(4,9431944)
        
    def call_getVarType(self, timeNextRecord = 1, expectedVarType = 'deletion', timeNextCall = 1, boolALTHeaders = True):
        call=self.getCall( timeNextRecord,timeNextCall, boolALTHeaders )
        #print call.site
        parsedVarType=call.getVarType()
        #print VCFParser.headerAlt
        self.assertEquals( parsedVarType, expectedVarType )
        
    def test_call_getVarType(self):
        self.call_getVarType()
        self.call_getVarType(3)
        self.call_getVarType(4, 'LINE1 insertion')
        self.call_getVarType(5, 'duplication')
        self.call_getVarType(boolALTHeaders = False)
        self.call_getVarType(3, boolALTHeaders = False)
        self.call_getVarType(4, 'LINE1 insertion', boolALTHeaders = False)
        self.call_getVarType(5, 'duplication', boolALTHeaders = False)
    
    def test_VCF_parseVCF(self):
        iVcfParser = self.createFiles()
        iVcfParser.parseVCF()
        iVcfParser.dbVar.filename = './temp/parsedExcel.xlsx'
        iVcfParser.dbVar.write()
        expectedExcel = self.readExcel(self._excelFile)
        parsedExcel = self.readExcel('./temp/parsedExcel.xlsx')
        self.assertEquals(parsedExcel,expectedExcel)
        
if __name__ == "__main__":
    unittest.main()