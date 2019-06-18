import os
import sys
import EXIF



def process_exif_data():
    f=open('Y:\\My Pictures\\2003-01 Governers Inaguration Ball\\DSC00178.JPG', 'rb')
    tags=EXIF.process_file(f)


    print "Original Date and Time = " , tags['EXIF DateTimeOriginal']    
    f.close()




process_exif_data()

        