#!/usr/bin/env python

import sys
from cbapi.response import *

def main():

        args=input('Enter alert unique_id: ')
        print(args)

        c = CbResponseAPI()
        alert = c.select(Alert, args)
        print(alert)
        alert.status = "Resolved"
        alert.save()


if __name__ == "__main__":
    sys.exit(main())
