#!/usr/bin/env python

import requests.packages.urllib3
import re
from cbapi.response import CbEnterpriseResponseAPI, Sensor
from cbapi.response.live_response_api import LiveResponseError

requests.packages.urllib3.disable_warnings()
c = CbEnterpriseResponseAPI()

print("Enter Sensor ID")
sensor_id = raw_input()
sensor = c.select(Sensor, sensor_id)

#Environment variables  for later consideration/extension of this script
#HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session Manager\Environment

#Autoruns
# autoruns source: http://www.forensicswiki.org/wiki/Windows_Registry#Persistence_keys
autoruns = [
{'name': 'WindowsRunKeys', 'key_path': 'HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Policies\Explorer\Run\*', 'value_name': '*'},
{'name': 'WindowsRunKeys', 'key_path': 'HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Run\*', 'value_name': '*'},
{'name': 'WindowsRunKeys', 'key_path': 'HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\RunOnce\*', 'value_name': '*'},
{'name': 'WindowsRunKeys', 'key_path': 'HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\RunOnce\Setup\*', 'value_name': '*'},
{'name': 'WindowsRunKeys', 'key_path': 'HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\RunOnceEx\*', 'value_name': '*'},
{'name': 'WindowsRunKeys', 'key_path': 'HKEY_LOCAL_MACHINE\Software\Wow6432Node\Microsoft\Windows\CurrentVersion\Run\*', 'value_name': '*'},
{'name': 'WindowsRunKeys', 'key_path': 'HKEY_LOCAL_MACHINE\Software\Wow6432Node\Microsoft\Windows\CurrentVersion\RunOnce\*', 'value_name': '*'},
{'name': 'WindowsRunKeys', 'key_path': 'HKEY_LOCAL_MACHINE\Software\Wow6432Node\Microsoft\Windows\CurrentVersion\RunOnce\Setup\*', 'value_name': '*'},
{'name': 'WindowsRunKeys', 'key_path': 'HKEY_LOCAL_MACHINE\Software\Wow6432Node\Microsoft\Windows\CurrentVersion\RunOnceEx\*', 'value_name': '*'},
{'name': 'WindowsRunKeys', 'key_path': 'HKEY_LOCAL_MACHINE\Software\Wow6432Node\Microsoft\Windows\CurrentVersion\Policies\Explorer\Run\*', 'value_name': '*'},
{'name': 'WindowsRunKeys', 'key_path': 'HKEY_USERS\%SID%\Software\Microsoft\Windows\CurrentVersion\Policies\Explorer\Run\*', 'value_name': '*'},
{'name': 'WindowsRunKeys', 'key_path': 'HKEY_USERS\%SID%\Software\Microsoft\Windows\CurrentVersion\Run\*', 'value_name': '*'},
{'name': 'WindowsRunKeys', 'key_path': 'HKEY_USERS\%SID%\Software\Microsoft\Windows\CurrentVersion\RunOnce\*', 'value_name': '*'},
{'name': 'WindowsRunKeys', 'key_path': 'HKEY_USERS\%SID%\Software\Microsoft\Windows\CurrentVersion\RunOnce\Setup\*', 'value_name': '*'},
{'name': 'WindowsRunKeys', 'key_path': 'HKEY_USERS\%SID%\Software\Microsoft\Windows\CurrentVersion\RunOnceEx\*', 'value_name': '*'},
{'name': 'WindowsRunKeys', 'key_path': 'HKEY_USERS\%SID%\Software\Wow6432Node\Microsoft\Windows\CurrentVersion\Policies\Explorer\Run\*', 'value_name': '*'},
{'name': 'WindowsRunKeys', 'key_path': 'HKEY_USERS\%SID%\Software\Wow6432Node\Microsoft\Windows\CurrentVersion\Run\*', 'value_name': '*'},
{'name': 'WindowsRunKeys', 'key_path': 'HKEY_USERS\%SID%\Software\Wow6432Node\Microsoft\Windows\CurrentVersion\RunOnce\*', 'value_name': '*'},
{'name': 'WindowsRunKeys', 'key_path': 'HKEY_USERS\%SID%\Software\Wow6432Node\Microsoft\Windows\CurrentVersion\RunOnce\Setup\*', 'value_name': '*'},
{'name': 'WindowsRunKeys', 'key_path': 'HKEY_USERS\%SID%\Software\Wow6432Node\Microsoft\Windows\CurrentVersion\RunOnceEx\*', 'value_name': '*'},
{'name': 'WindowsRunServices', 'key_path': 'HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\RunServicesOnce\*', 'value_name': '*'},
{'name': 'WindowsRunServices', 'key_path': 'HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\RunServices\*', 'value_name': '*'},
{'name': 'WindowsRunServices', 'key_path': 'HKEY_LOCAL_MACHINE\Software\Wow6432Node\Microsoft\Windows\CurrentVersion\RunServicesOnce\*', 'value_name': '*'},
{'name': 'WindowsRunServices', 'key_path': 'HKEY_LOCAL_MACHINE\Software\Wow6432Node\Microsoft\Windows\CurrentVersion\RunServices\*', 'value_name': '*'},
{'name': 'WindowsSessionManagerBootExecute', 'key_path': 'HKEY_LOCAL_MACHINE\System\CurrentControlSet\Control\Session Manager', 'value_name': 'BootExecute'},
{'name': 'WindowsSessionManagerExecute', 'key_path': 'HKEY_LOCAL_MACHINE\System\CurrentControlSet\Control\Session Manager', 'value_name': 'Execute'},
{'name': 'WindowsSessionManagerSetupExecute', 'key_path': 'HKEY_LOCAL_MACHINE\System\CurrentControlSet\Control\Session Manager', 'value_name': 'SetupExecute'},
{'name': 'WindowsSessionManagerWOWCommandLine', 'key_path': 'HKEY_LOCAL_MACHINE\System\CurrentControlSet\Control\Session Manager\WOW', 'value_name': 'cmdline'},
{'name': 'WindowsSessionManagerWOWCommandLine', 'key_path': 'HKEY_LOCAL_MACHINE\System\CurrentControlSet\Control\Session Manager\WOW', 'value_name': 'wowcmdline'},
{'name': 'WindowsServiceControlManagerExtension', 'key_path': 'HKEY_LOCAL_MACHINE\System\CurrentControlSet\Control\ServiceControlManagerExtension\*', 'value_name': '*'},
{'name': 'WindowsShellIconOverlayIdentifiers', 'key_path': 'HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Explorer\ShellIconOverlayIdentifiers\*', 'value_name': '*'},
{'name': 'WindowsShellIconOverlayIdentifiers', 'key_path': 'HKEY_LOCAL_MACHINE\Software\Wow6432Node\Microsoft\Windows\CurrentVersion\Explorer\ShellIconOverlayIdentifiers\*', 'value_name': '*'},
{'name': 'WindowsShellIconOverlayIdentifiers', 'key_path': 'HKEY_USERS\%SID%\Software\Microsoft\Windows\CurrentVersion\Explorer\ShellIconOverlayIdentifiers\*', 'value_name': '*'},
{'name': 'WindowsShellIconOverlayIdentifiers', 'key_path': 'HKEY_USERS\%SID%\Software\Wow6432Node\Microsoft\Windows\CurrentVersion\Explorer\ShellIconOverlayIdentifiers\*', 'value_name': '*'},
{'name': 'WindowsShellExtensions', 'key_path': 'HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Shell Extensions\Approved', 'value_name': '*'},
{'name': 'WindowsShellExtensions', 'key_path': 'HKEY_LOCAL_MACHINE\Software\Wow6432Node\Microsoft\Windows\CurrentVersion\Shell Extensions\Approved', 'value_name': '*'},
{'name': 'WindowsShellExtensions', 'key_path': 'HKEY_USERS\%SID%\Software\Microsoft\Windows\CurrentVersion\Shell Extensions\Approved', 'value_name': '*'},
{'name': 'WindowsShellExtensions', 'key_path': 'HKEY_USERS\%SID%\Software\Wow6432Node\Microsoft\Windows\CurrentVersion\Shell Extensions\Approved', 'value_name': '*'},
{'name': 'WindowsShellExecuteHooks', 'key_path': 'HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Explorer\ShellExecuteHooks\*', 'value_name': '*'},
{'name': 'WindowsShellExecuteHooks', 'key_path': 'HKEY_LOCAL_MACHINE\Software\Wow6432Node\Microsoft\Windows\CurrentVersion\Explorer\ShellExecuteHooks\*', 'value_name': '*'},
{'name': 'WindowsShellLoadAndRun', 'key_path': 'HKEY_CURRENT_USER\Software\Microsoft\Windows NT\CurrentVersion\Windows', 'value_name': 'Load'},
{'name': 'WindowsShellLoadAndRun', 'key_path': 'HKEY_CURRENT_USER\Software\Wow6432Node\Microsoft\Windows NT\CurrentVersion\Windows', 'value_name': 'Load'},
{'name': 'WindowsShellLoadAndRun', 'key_path': 'HKEY_CURRENT_USER\Software\Microsoft\Windows NT\CurrentVersion\Windows', 'value_name': 'Run'},
{'name': 'WindowsShellLoadAndRun', 'key_path': 'HKEY_CURRENT_USER\Software\Wow6432Node\Microsoft\Windows NT\CurrentVersion\Windows', 'value_name': 'Run'},
{'name': 'WindowsShellServiceObjects', 'key_path': 'HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\ShellServiceObjectDelayLoad', 'value_name': '*'},
{'name': 'WindowsShellServiceObjects', 'key_path': 'HKEY_LOCAL_MACHINE\Software\Wow6432Node\Microsoft\Windows\CurrentVersion\ShellServiceObjectDelayLoad', 'value_name': '*'},
{'name': 'WindowsCredentialProviderFilters', 'key_path': 'HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Authentication\Credential Provider Filters\*', 'value_name': '*'},
{'name': 'WindowsCredentialProviderFilters', 'key_path': 'HKEY_LOCAL_MACHINE\Software\Wow6432Node\Microsoft\Windows\CurrentVersion\Authentication\Credential Provider Filters\*', 'value_name': '*'},
{'name': 'WindowsCredentialProviders', 'key_path': 'HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Authentication\Credential Providers\*', 'value_name': '*'},
{'name': 'WindowsCredentialProviders', 'key_path': 'HKEY_LOCAL_MACHINE\Software\Wow6432Node\Microsoft\Windows\CurrentVersion\Authentication\Credential Providers\*', 'value_name': '*'},
{'name': 'WindowsPLAPProviders', 'key_path': 'HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Authentication\PLAP Providers\*', 'value_name': '*'},
{'name': 'WindowsPLAPProviders', 'key_path': 'HKEY_LOCAL_MACHINE\Software\Wow6432Node\Microsoft\Windows\CurrentVersion\Authentication\PLAP Providers\*', 'value_name': '*'},
{'name': 'WindowsWinlogonShell', 'key_path': 'HKEY_LOCAL_MACHINE\Software\Microsoft\Windows NT\CurrentVersion\Winlogon', 'value_name': 'GinaDLL'},
{'name': 'WindowsWinlogonShell', 'key_path': 'HKEY_USERS\%SID%\Software\Microsoft\Windows NT\CurrentVersion\Winlogon', 'value_name': 'GinaDLL'},
{'name': 'WindowsWinlogonNotify', 'key_path': 'HKEY_LOCAL_MACHINE\Software\Microsoft\Windows NT\CurrentVersion\Winlogon\Notify\*', 'value_name': 'DLLName'},
{'name': 'WindowsWinlogonNotify', 'key_path': 'HKEY_USERS\%SID%\Software\Microsoft\Windows NT\CurrentVersion\Winlogon\Notify\*', 'value_name': 'DLLName'},
{'name': 'WindowsWinlogonShell', 'key_path': 'HKEY_LOCAL_MACHINE\Software\Microsoft\Windows NT\CurrentVersion\Winlogon', 'value_name': 'Shell'},
{'name': 'WindowsWinlogonShell', 'key_path': 'HKEY_USERS\%SID%\Software\Microsoft\Windows NT\CurrentVersion\Winlogon', 'value_name': 'Shell'},
{'name': 'WindowsWinlogonSystem', 'key_path': 'HKEY_LOCAL_MACHINE\Software\Microsoft\Windows NT\CurrentVersion\Winlogon', 'value_name': 'System'},
{'name': 'WindowsWinlogonSystem', 'key_path': 'HKEY_USERS\%SID%\Software\Microsoft\Windows NT\CurrentVersion\Winlogon', 'value_name': 'System'},
{'name': 'WindowsWinlogonTaskman', 'key_path': 'HKEY_LOCAL_MACHINE\Software\Microsoft\Windows NT\CurrentVersion\Winlogon', 'value_name': 'Taskman'},
{'name': 'WindowsWinlogonTaskman', 'key_path': 'HKEY_USERS\%SID%\Software\Microsoft\Windows NT\CurrentVersion\Winlogon', 'value_name': 'Taskman'},
{'name': 'WindowsWinlogonUserinit', 'key_path': 'HKEY_LOCAL_MACHINE\Software\Microsoft\Windows NT\CurrentVersion\Winlogon', 'value_name': 'Userinit'},
{'name': 'WindowsWinlogonUserinit', 'key_path': 'HKEY_USERS\%SID%\Software\Microsoft\Windows NT\CurrentVersion\Winlogon', 'value_name': 'Userinit'},
{'name': 'WindowsWinlogonVMApplet', 'key_path': 'HKEY_LOCAL_MACHINE\Software\Microsoft\Windows NT\CurrentVersion\Winlogon', 'value_name': 'VMApplet'},
{'name': 'WindowsWinlogonVMApplet', 'key_path': 'HKEY_USERS\%SID%\Software\Microsoft\Windows NT\CurrentVersion\Winlogon', 'value_name': 'VMApplet'},
{'name': 'WindowsSystemPolicyShell', 'key_path': 'HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Policies\System', 'value_name': 'Shell'},
{'name': 'WindowsSystemPolicyShell', 'key_path': 'HKEY_LOCAL_MACHINE\Software\Wow6432Node\Microsoft\Windows\CurrentVersion\Policies\System', 'value_name': 'Shell'},
{'name': 'WindowsStubPaths', 'key_path': 'HKEY_LOCAL_MACHINE\Software\Microsoft\Active Setup\Installed Components\*', 'value_name': '*'},
{'name': 'WindowsStubPaths', 'key_path': 'HKEY_LOCAL_MACHINE\Software\Wow6432Node\Microsoft\Active Setup\Installed Components\*', 'value_name': '*'},
{'name': 'WindowsStubPaths', 'key_path': 'HKEY_USERS\%SID%\Software\Microsoft\Active Setup\Installed Components\*', 'value_name': '*'},
{'name': 'WindowsStubPaths', 'key_path': 'HKEY_USERS\%SID%\Software\Wow6432Node\Microsoft\Active Setup\Installed Components\*', 'value_name': '*'},
{'name': 'WindowsAppInitDLLs', 'key_path': 'HKEY_LOCAL_MACHINE\Software\Microsoft\Windows NT\CurrentVersion\Windows', 'value_name': 'AppInit_DLLs'},
{'name': 'WindowsAppInitDLLs', 'key_path': 'HKEY_LOCAL_MACHINE\Software\Wow6432Node\Microsoft\Windows NT\CurrentVersion\Windows', 'value_name': 'AppInit_DLLs'},
{'name': 'WindowsAppInitDLLs', 'key_path': 'HKEY_USERS\%SID%\Software\Microsoft\Windows NT\CurrentVersion\Windows', 'value_name': 'AppInit_DLLs'},
{'name': 'WindowsAppInitDLLs', 'key_path': 'HKEY_USERS\%SID%\Software\Wow6432Node\Microsoft\Windows NT\CurrentVersion\Windows', 'value_name': 'AppInit_DLLs'},
{'name': 'WindowsSecurityProviders', 'key_path': 'HKEY_LOCAL_MACHINE\System\CurrentControlSet\Control\SecurityProviders\*', 'value_name': '*'},
{'name': 'WindowsAlternateShell', 'key_path': 'HKEY_LOCAL_MACHINE\System\CurrentControlSet\Control\SafeBoot', 'value_name': 'AlternateShell'},
{'name': 'WindowsBootVerificationProgram', 'key_path': 'HKEY_LOCAL_MACHINE\System\CurrentControlSet\Control\BootVerificationProgram', 'value_name': 'ImagePath'}
]

def lookup_registry_entry(t):
	if multikeys == 'True':
		try:
			rk = session.list_registry_keys(t)
			for k in rk:
				print t, " :: ", k['value_data']
		except LiveResponseError as e:
			if e.win32_error == 0x80070002:
				pass
			else:
				raise
	else:
		try:
			rv = session.get_registry_value(t)
			print t, ' :: ' , rv['value_data']
		except LiveResponseError as e:
			if e.win32_error == 0x80070002:
				pass
			else:
				raise
	

try:
	with sensor.lr_session() as session:  # this will wait until the Live Response session is established
		for ar in autoruns:
			# In the format of the http://www.forensicswiki.org page on persistence keys
			# Registry Keys that conatain multiple values are listed with a trailing \*
			# Clean those two trailing characters off to match the registry keys without multiple values
			key_path_clean = ar['key_path'].rstrip('*')
			key_path_clean = key_path_clean.rstrip('\\')
			
			# Registry keys with multiple values will list the name of the key as *
			# If the name is * we need to call a different live_reponse_api function
			# Build the registry key diffently for the appropriate function
			if ar['value_name'] == '*':
				key_name = key_path_clean
				multikeys = 'True'
			else:
				key_name = key_path_clean + '\\' + str(ar['value_name'])
				multikeys = 'False'
			
			# In the format of the http://www.foreniscswiki.org page on persistence keys
			# Registry Keys that are tied to a particular User account conatain %SID% as a placeholder
			#  for the variable SID portion of the registry key
			if re.search ("%SID%", key_name):
				# Grab the portion of the registry path to the left of the %SID% string
				sid_root = key_name.split("%SID%")[0]
				# Build a list containing all the sub_keys of the registry path
				sid_dict = session.list_registry_keys_and_values(sid_root)
				# Iterate over each permutation in the list and query for that unique registry key
				for s in sid_dict['sub_keys']:
					# Replace the string %SID% with the SID from our list in the key_name
					t = re.sub("%SID%", s, key_name)
					lookup_registry_entry(t)
			else:
				t = key_name
				lookup_registry_entry(t)
				
except Exception as e:
	print type(e)
	print e

