#!/usr/bin/env python

import tempfile, os, datetime


tmpDir = tempfile.gettempdir()

dirExtn = 'cbd_se_test'

outDir = os.path.join(tmpDir, dirExtn)

if not os.path.exists(outDir):
	os.makedirs(outDir)

print "File will be written to: %s" % (outDir)

dteString = datetime.datetime.now().strftime("%Y%m%d_%H%M%S.py")

fName = os.path.join(tmpDir, dirExtn, dteString)

print "Fully qualified file name: %s" % (fName)

with open(fName,'w') as f:
	f.write("print 'If you see this, we ran the file.\\r\\nWe just created and executed the following file name: %s'" % (fName))

execfile(fName)
