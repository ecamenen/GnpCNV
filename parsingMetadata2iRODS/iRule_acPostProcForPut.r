acPostProcForPut { ON($objPath like "/tempZone/home/*") {
  msiExecCmd("parsing_metadata2iRODS.sh", "-c $objPath --zone inraUrgiZone --user rflores --pass ****", "null", "null", "null", *CMD_OUT);
  msiGetStdoutInExecCmdOut(*CMD_OUT,*OUT);
  writeLine("serverLog",*OUT);}
 }

