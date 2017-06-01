from six.moves.configparser import RawConfigParser
import os
import attrdict
import six
from errors import CredentialError
default_profile = {
    "api_key": None,
    "conn_id": None,
    "cbd_api_url": None
}


class Credentials(attrdict.AttrDict):
    def __init__(self, *args, **kwargs):
        super(Credentials, self).__init__(default_profile)
        super(Credentials, self).__init__(*args, **kwargs)

        if not self.get("api_key", None):
            raise CredentialError("No API Key (api_key) specified")
        if not self.get("conn_id", None):
            raise CredentialError("No Connector ID (conn_id) specified")
        if not self.get("cbd_api_url", None):
            raise CredentialError("No CB API URL (cb_api_url) specified")


class CredentialStore(object):
    def __init__(self, **kwargs):
        self.credential_search_path = [
            os.path.join(os.path.sep, "etc", "cbdefense", "credentials"),
            os.path.join(os.path.expanduser("~"), ".cbdefense", "credentials"),
            os.path.join(".", ".cbdefense", "credentials"),
        ]

        if "credential_file" in kwargs:
            if isinstance(kwargs["credential_file"], six.string_types):
                self.credential_search_path = [kwargs["credential_file"]]
            elif type(kwargs["credential_file"]) is list:
                self.credential_search_path = kwargs["credential_file"]

        self.credentials = RawConfigParser(defaults=default_profile)
        self.credential_files = self.credentials.read(self.credential_search_path)

    def get_credentials(self, profile=None):
        credential_profile = profile or "default"
        if credential_profile not in self.get_profiles():
            raise CredentialError("Cannot find credential profile '%s' after searching in these files: %s." %
                                  (credential_profile, ", ".join(self.credential_search_path)))

        retval = {}
        for k, v in six.iteritems(default_profile):
                retval[k] = self.credentials.get(credential_profile, k)
		
        if not retval["api_key"] or not retval["conn_id"] or not retval["cbd_api_url"]:
            raise CredentialError("API Key and Connector ID not available for profile %s" % credential_profile)

        return Credentials(retval)

    def get_profiles(self):
        return self.credentials.sections()
