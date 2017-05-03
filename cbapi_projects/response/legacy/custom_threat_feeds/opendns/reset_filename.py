#!/bin/env python

import os, pprint, re

for i in os.listdir("."):
    if re.match("securityActivity_.*zip", i):
        pprint.pprint(i)
        os.rename(i, "securityActivity.zip")
