'==========================================================================
'
' NAME:    Bit9 Agent Email
' VERSION: 0.1
' PURPOSE: Populate the notifer email field with address read from Actrive Directory
'
' AUTHOR:  Cordingley, Benjamin
' DATE:    04/0/2015
'
'==========================================================================
Option Explicit
	
Dim objShell, objADSInfo, objUser 'Standard objects'
Dim strEmail

Set objShell   = CreateObject("WScript.Shell")
Set objADSInfo = CreateObject("ADSystemInfo")
Set objUser    = GetObject("LDAP://" & objADSInfo.UserName)

strEmail = objUser.mail
objShell.RegWrite "HKCU\Software\Bit9\Parity Agent\Notifier\Email",strEmail,"REG_SZ"
