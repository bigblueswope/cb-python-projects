
applications = {
    'When known malware that has a verified signature': {'type': 'REPUTATION', 'value': 'KNOWN_MALWARE'},
    'When applications that appear on the company blacklist': {'type': 'REPUTATION', 'value': 'COMPANY_BLACK_LIST'},
    'When suspected malware': {'type': 'REPUTATION', 'value': 'SUSPECT_MALWARE'},
    'When adware or a potentially unwanted program': {'type': 'REPUTATION', 'value': 'PUP'},
    'When an unknown application': {'type': 'REPUTATION', 'value': 'RESOLVING'},
    'When a not listed application': {'type': 'REPUTATION', 'value': 'ADAPTIVE_WHITE_LIST'},
    'When an application at path': {'type': 'NAME_PATH', 'value': ''}
}

operations = {
    'Tries to communicate over the network': 'NETWORK',
    'Tries to execute code from memory': 'RUN_INMEMORY_CODE',
    'Tries to inject code or modify memory of another process': 'CODE_INJECTION',
    'Tries to invoke an untrusted application': 'POL_INVOKE_NOT_TRUSTED',
    'Tries to run or is running': 'RUN',
    'Tries to scrape memory of another process': 'MEMORY_SCRAPE'
}

actions = {
    'Terminate process': 'TERMINATE',
    'Deny': 'DENY',
    'Allow': 'ALLOW',
    'Ignore': 'IGNORE'
}

# If you desire something other than what is set here
#  You can edit the values in av_config and the policy
#  will be created with a new default value
av_config = {
    'avSettings': {
        'features': [
            {
                'enabled': 'true',
                'name': 'SIGNATURE_UPDATE'
            },
            {
                'enabled': 'true',
                'name': 'ONACCESS_SCAN'
            },
            {
                'enabled': 'true',
                'name': 'ONDEMOND_SCAN'
            }
        ],
        'onAccessScan': {
            'profile': 'NORMAL'
        },
        'onDemandScan': {
            'profile': 'NORMAL',
            'scanCdDvd': 'AUTOSCAN',
            'scanUsb': 'AUTOSCAN',
            'schedule': {
                'days': None,
                'rangeHours': 0,
                'recoveryScanIfMissed': 'true',
                'startHour': 0
            }
        },
        'settings': None,
        'signatureUpdate': {
            'schedule': {
                'fullIntervalHours': 0,
                'initialRandomDelayHours': 1,
                'intervalHours': 2
            }
        },
        'updateServers': {
            'servers': [
                {
                    'flags': 0,
                    'regId': None,
                    'server': [
                        'http://updates.cdc.carbonblack.io/update'
                    ]
                }
            ],
            'serversForOffSiteDevices': [
                'http://updates.cdc.carbonblack.io/update'
            ],
            'serversOverride': [],
            'useServersOverride': 'false'
        }
    }
}

misc_config = {
    'directoryActionRules': [],
    'mobileSensorSettings': None,
    'phishingSettings': None
}


# Just like with av_config, if you don't like the value of 
#  a setting in sensor_config, edit it here and new policies
#  created will have that value set
sensor_config = {
    'sensorAutoUpdateEnabled': 'true',
    'sensorSettings': [
        {
            'name': 'ALLOW_UPLOADS',
            'value': 'false'
        },
        {
            'name': 'SHOW_UI',
            'value': 'true'
        },
        {
            'name': 'BACKGROUND_SCAN',
            'value': 'true'
        },
        {
            'name': 'POLICY_ACTION_OVERRIDE',
            'value': 'true'
        },
        {
            'name': 'QUARANTINE_DEVICE_MESSAGE',
            'value': 'Your device has been quarantined by your Cb Defense administrator.'
        },
        {
            'name': 'LOGGING_LEVEL',
            'value': 'NORMAL'
        },
        {
            'name': 'ALLOW_UNINSTALL',
            'value': 'true'
        },
        {
            'name': 'QUARANTINE_DEVICE',
            'value': 'false'
        },
        {
            'name': 'RATE_LIMIT',
            'value': '0'
        },
        {
            'name': 'CONNECTION_LIMIT',
            'value': '0'
        },
        {
            'name': 'QUEUE_SIZE',
            'value': '100'
        },
        {
            'name': 'LEARNING_MODE',
            'value': '0'
        },
        {
            'name': 'SCAN_NETWORK_DRIVE',
            'value': 'false'
        },
        {
            'name': 'BYPASS_AFTER_LOGIN_MINS',
            'value': '0'
        },
        {
            'name': 'BYPASS_AFTER_RESTART_MINS',
            'value': '0'
        },
        {
            'name': 'SCAN_EXECUTE_ON_NETWORK_DRIVE',
            'value': 'true'
        },
        {
            'name': 'DELAY_EXECUTE',
            'value': 'true'
        },
        {
            'name': 'PRESERVE_SYSTEM_MEMORY_SCAN',
            'value': 'false'
        },
        {
            'name': 'HASH_MD5',
            'value': 'false'
        },
        {
            'name': 'SCAN_LARGE_FILE_READ',
            'value': 'false'
        },
        {
            'name': 'SHOW_FULL_UI',
            'value': 'true'
        },
        {
            'name': 'HELP_MESSAGE',
            'value': ''
        }
    ]
}

