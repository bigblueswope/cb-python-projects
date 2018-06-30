import sys
sys.path.append('../../../cbapi/client_apis/python/src/')
import cbapi
from cbapi.util.cli_helpers import main_helper

def main(cb, args):
    for (proc, events) in cb.process_search_and_events_iter(r"filemod:ntuser.dat"):
        filemods = events.get('process', {}).get('filemod_complete', [])
        for filemod in filemods:
            
            print filemod
            # TODO -- figure out fields
            action, timestamp, filepath, md5, junk1, junk2 = filemod.split('|')
            
            filepath = filepath.lower()
            if not filepath.endswith(".exe") or not filepath.endswith(".dll"):
                continue
            
            if action == "1":
                action = "CREATE"
            elif action == "2":
                action = "MODIFY"
            elif action == "4":
                action = "DELETE"
            elif action == "8":
                action = "EXECUTABLE_WRITE"
            
            print "%s,%s,%s,%s,%s,%s" % (timestamp, proc['hostname'], proc['username'], proc['path'], filepath, action)

if __name__ == "__main__":
    main_helper("Search for processes writing to ntuser.dat", main)
