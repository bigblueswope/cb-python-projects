#!/usr/bin/env python

import sys
from cbapi.protection.models import *
from cbapi.protection.rest_api import CbEnterpriseProtectionAPI
from cbapi.example_helpers import build_cli_parser, get_cb_protection_object, disable_insecure_warnings

disable_insecure_warnings()

def main():
    parser = build_cli_parser()
    parser.add_argument("--query", help="file property to query upon. e.x.\nmd5:D2F7A0ADC2EE0F65AB1F19D2E00C16B8", default='')
    parser.add_argument("--list", help="If provided this will list all the queryable fields", action="store_true")
    args = parser.parse_args()
    
    cb = get_cb_protection_object(args)
    
    if args.list:
        print "Here's a list of all the available fields in the File Catalog (and can be used in a query):"
        file = cb.select(FileCatalog).where('prevalence:1')
        print file[0]
        print "="*80
        
        print "Here's a list of all the fields available from the File Instance table."
        fi_query = 'fileCatalogId:%s' % (file[0].id)
        file_instance = cb.select(FileInstance).where(fi_query)
        print file_instance[0]
        sys.exit(0)
    
    if not args.query:
        raise TypeError('Missing the query argument.  Run %s --help for additional instructions'% (sys.argv[0]))
    
    try:
        file_catalog = cb.select(FileCatalog).where(args.query)
    except:
        raise

    for f in file_catalog:
        print "File Name  : ", f.fileName
        print "Sha256 Hash: ", f.sha256

        fi_query='fileCatalogId:%s' % (f.id)
        file_instances = cb.select(FileInstance).where(fi_query)
    
        for file in file_instances:
            comp_query = 'id:%s' % (file.computerId)
            comp = cb.select(Computer).where(comp_query)
            for c in comp:
                cname = c.name
            print cname, file.pathName

if __name__ == "__main__":
    sys.exit(main())

