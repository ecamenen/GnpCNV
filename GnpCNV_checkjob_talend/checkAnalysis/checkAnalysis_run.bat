%~d0
cd %~dp0
java -Xms256M -Xmx1024M -cp .;../lib/routines.jar;../lib/commons-collections-3.2.2.jar;../lib/commons-lang-2.6.jar;../lib/geronimo-stax-api_1.0_spec-1.0.1.jar;../lib/log4j-1.2.15.jar;../lib/log4j-1.2.16.jar;../lib/dom4j-1.6.1.jar;../lib/poi-ooxml-schemas-3.11-20141221.jar;../lib/jxl.jar;../lib/advancedPersistentLookupLib-1.0.jar;../lib/jboss-serialization.jar;../lib/xmlbeans-2.6.0.jar;../lib/poi-ooxml-3.11-20141221_modified_talend.jar;../lib/talendcsv.jar;../lib/trove.jar;../lib/poi-3.11-20141221_modified_talend.jar;../lib/simpleexcel.jar;../lib/talend_file_enhanced_20070724.jar;../lib/poi-scratchpad-3.11-20141221.jar;checkanalysis_0_3.jar; checkgnpcnv.checkanalysis_0_3.checkAnalysis --context= %* 