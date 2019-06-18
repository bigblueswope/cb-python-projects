#!/usr/bin/env python

import sys, os, time, datetime, exifread 

DATE_FORMAT   = '%Y%m%d_%H%M%S'
allowed_files = ['.asf', '.jpg', '.jpeg', '.png', '.tiff', '.tif']
named_files = []

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


def renameFile(path, file):
    """ Rename <old_filename> with the using the date/time created or modified for the new file name"""

    old_filename = os.path.join(path,file)

    (name,xtn) = os.path.splitext(file)
    xtn = xtn.lower()

    if is_a_file(path, file, xtn):
        f = open(old_filename, 'rb')
        try:
            tags=exifread.process_file(f)
        except UnboundLocalError:
            tags = {}
        try:
            tags['EXIF DateTimeOriginal']
            exif_time = str(tags['EXIF DateTimeOriginal'])
            
        except (KeyError,ValueError):
            print 'No EXIF DateTimeOriginal for ', file
            f.close()
            return
        f.close()
        date_time_name = exif_time.replace(':','')
        date_time_name = date_time_name.replace(' ','_')
        
        copy_number = named_files.count(date_time_name)
        named_files.append(date_time_name)
        
        new_name = date_time_name + "_" + str(copy_number) + xtn
        
        new_filename = os.path.join(path, new_name)
        if old_filename == new_filename:
            print old_filename, 'already proper name...skipping rename'
        else:
            print 'Renaming:', old_filename, 'to', new_filename
            os.rename(old_filename, new_filename)

if __name__ == '__main__':
    if os.path.isdir(sys.argv[1]):
        """Recursively walk the directory listed as Arg 1 and work each file."""
        print
        for path,dirs,files in os.walk(sys.argv[1]):
            for file in files:
                renameFile(path, file)
    else:
        print sys.argv[1]
        print "\nNo path to rename specified.\n"
        print "Usage:\n\tpython", sys.argv[0], "<path to directory of source files>"
        sys.exit(1)
