myTestRule{
	
	msiExecCmd("parsing_metadata2iRODS.sh", *ARG,"null", "null", "null", *CMD_OUT);
	msiGetStdoutInExecCmdOut(*CMD_OUT,*OUT);
	#writeLine("stdout","*OUT");
	*list=split(*OUT, "\n");
	foreach (*line in *list){
		*metadata=split(*line, "\t");
		*key=elem(*metadata, 0);
		*val=elem(*metadata, 1);
		writeLine("stdout","*key");
		writeLine("stdout","*val");		
		#msiAddKeyVal(*test,*key,*val);
		#msiAssociateKeyValuePairsToObj(*test,*file, "-d");
	}
}
INPUT *file="/tempZone/home/rods/test/test", *ARG="metadata.csv"
OUTPUT ruleExecOut