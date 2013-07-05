@echo off

set "FTP_INPUT=ftp.input"

call :upload 10.10.100.129 root nec
call :upload 192.168.177.241 root nec123
call :upload 192.168.8.193 root PNMS
call :upload 192.168.174.50 root nec
del %FTP_INPUT%
goto :EOF

:upload
	echo %~2> %FTP_INPUT%
	echo %~3>> %FTP_INPUT%
	echo cd /usr/bin>> %FTP_INPUT%
	echo put bin\necping>> %FTP_INPUT%
	echo put bin\necping-lib>> %FTP_INPUT%
	echo close>> %FTP_INPUT%
	echo quit>> %FTP_INPUT%
	ftp -s:%FTP_INPUT% %~1
goto :EOF
