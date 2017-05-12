# -*-coding:Utf-8 -*
'''
@dateCreation: 02/05/17
@author: INRA Versailles (URGI) - Etienne CAMENEN
@description:  Parsing a VCF file into an Excel metadata file used for NCBI submission
'''

import argparse, sys
from myProject.VcfParser import *

def help() :
    parser = argparse.ArgumentParser ( description = 'Parsing a VCF file into an Excel metadata file used for NCBI submission' )
    parser.add_argument ( '-vcf', dest = 'vcfFilename', required = 'True', help = 'Path of your VCF file' )
    parser.add_argument ( '-xl', dest = 'excelFilename', required = 'True', help = 'Path of your Excel metadata file' )
    parser.add_argument ( '-exp', dest = 'idExperiment', default = '1', help = 'ID of your Experiment coming from NCBI\'s excel metadata (default: %(default)s)')
    return parser

parser = help()

if len ( sys.argv ) < 2:
    parser.print_help()


args = parser.parse_args()

print ('Parsing in progress...\n')

class Launcher:
    def __init__(self, vcfFilename, excelFilename, idExperiment):
        Call2.cptVar = 0
        VCFParser.dbVar = DbVarWriter(excelFilename)
        self.vcf = VCFParser(open(vcfFilename), excelFilename, idExperiment)



if __name__ == '__main__':
    launch = Launcher(args.vcfFilename, args.excelFilename, args.idExperiment)
    launch.vcf.parseVCF()
    launch.vcf.dbVar.write()
    print ('\nVCF file has been parsed successfully.')
    