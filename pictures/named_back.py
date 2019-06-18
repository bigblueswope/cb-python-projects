#!/usr/bin/env python

import sys, os, time, datetime, exifread 

def is_a_file(path, file, xtn):
    """
    We only want to rename the files right?
    Return True or False depending on whether object is a file or a directory
    """
    
    if os.path.isdir(os.path.join(path,file)):
        print "This is a directory not a file.  Will not rename!"
        return False
    if allowed_files.count(xtn):
        return True
    else:
        print file, "is not a in the list of allowed extensions. Will not rename!"
        return False


def renameFile(good_name, bad_name):
    """ Rename <old_filename> with the using the date/time created or modified for the new file name"""

    print 'Renaming:', bad_name, 'to', good_name
    os.rename(bad_name, good_name)

if __name__ == '__main__':
    s = open('/Users/BJSwope/Desktop/to_be_named_back.txt', 'rb')
    for line in s:
        line = line[:-1]
        print line
        parts = str.split(line,'|')
        good_name = parts[0]
        bad_name = parts[1]
        renameFile(good_name, bad_name)
