#@author:flavia ninsiima delmira
#@contact:delmira91@gmail.com
"""This program loops through image files in a folder.
    It then extracts metadata from the images
    And stores the metadata in a csv file
"""

import os                               #for splitting off filename from path name
import csv                              #for writing metadata to csv file
import glob                             #for iteration through image files in a folder path
from PIL import Image                   #download pillow (python imaging library) from www.pythonware.com and install it!
from PIL.ExifTags import TAGS, GPSTAGS  #imports TAGS module, GPSTAGS module from PIL.ExifTags


#getcoordinates() returns geographical coordinates in degrees
#reference http://lonelycode.com/2008/12/04/google-maps-and-django/
def getcoordinates(d, m, s, ind):
    sec = float((m * 60) + s)
    frac = float(sec / 3600)
    deg = float(d + frac)
    if ind == 'W' or ind == 'S':
        deg = deg * -1
    return float(deg)



#get_exif_data() extracts exchangeable image file format(exif)
#reference http://www.exiv2.org/tags.html 
def get_exif_data(image):                                  #function takes in image object
    
    exif_data_dic, gps_data = {}, {}                              #initializing dictionaries to store exif data and gps data
    timestamp, datestamp, resolution = 'None', 'None', 'None'     #initialized as 'None' incase incase these values are not present as metadata
    altitude, latitude, longitude = 'None', 'None', 'None'
    
    #extracting metadata...
    exif_data_dic = {TAGS[k]: v for k, v in image._getexif().iteritems() if k in TAGS}
    #imageObject._getxif() gets exif data dictionary from image object
    #as shown in the reference, tags are decimals or hexadecimels. the above statement converts tags to keys making indexing operations easier
    #e.g. dictionary_name['DateTime'] is easy to understand instead of dictionary_name[---some hexadecimal value here---]
    
    if exif_data_dic: #if exif data for image is present
        
        datetime = exif_data_dic['DateTimeOriginal'].split(" ") #split this into date and time
        datestamp, timestamp = datetime[0], datetime[1]
        resolution = str(exif_data_dic['ExifImageWidth']) + 'x' + str(exif_data_dic['ExifImageHeight'])
        
        if 'GPSInfo' in exif_data_dic.keys(): #if 'GPSInfo' is present in exif dat

            #extracting GPS info...
            gps_data = {GPSTAGS[k]: v for k, v in exif_data_dic['GPSInfo'].iteritems() if k in GPSTAGS} #extract GPSTags e.g GPSAltitude and its value

            #extracting altitude...
            altitude = gps_data['GPSAltitude'][0] / float(gps_data['GPSAltitude'][1])           # altitude extracted as e.g. (0,1)... float division 0/1

            #extracting latitude...
            degrees = gps_data['GPSLatitude'][0][0] / float(gps_data['GPSLatitude'][0][1])      # latitude extracted as e.g. ((0,1)(3,7)(9,0)) degrees,minutes,seconds
            minutes = gps_data['GPSLatitude'][1][0] / float(gps_data['GPSLatitude'][1][1])
            seconds = gps_data['GPSLatitude'][2][0] / float(gps_data['GPSLatitude'][2][1])
            index = gps_data['GPSLatitudeRef']
            latitude = getcoordinates(degrees, minutes, seconds, index)

            #extracting longitude...
            degrees = gps_data['GPSLongitude'][0][0] / float(gps_data['GPSLongitude'][0][1]) 
            minutes = gps_data['GPSLongitude'][1][0] / float(gps_data['GPSLongitude'][1][1])
            seconds = gps_data['GPSLongitude'][2][0] / float(gps_data['GPSLongitude'][2][1])
            index = gps_data['GPSLongitudeRef']
            longitude = getcoordinates(degrees, minutes, seconds, index)

    return resolution, timestamp, datestamp, altitude, latitude, longitude


#the main 
def main():

    #...opening my ImageMetadata.csv file in append|binary mode
    #reference https://docs.python.org/2/library/csv.html
    with open('ImageMetadata.csv', 'ab') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['FILENAME','RESOLUTION','TIMESTAMP','DATESTAMP','ALTITUDE','LATITUDE','LONGITUDE'])
        csvfile.close()

    #listing possible types of formats we might find in the folder with our image files
    # *.jpg is a regular expression pattern meaning all file names with .jpg in them
    extensions = ["*.jpg", "*.png"]

    #looping through all files.extensions in the folder
    for ext in extensions:

        #...
        directory = "E:\Documents\Mobile Crops Surveillance Project\Field Survey\Apac_Image_Data/" + ext
        #this path can be specified implicitly in our code...
        #or we can ask user for path using raw_input() function

        #reference https://docs.python.org/2/library/glob.html
        for pathname in glob.glob(directory):
            try:
                image = Image.open(pathname)
                filename = os.path.split(pathname)[-1]
                resolution, timestamp, datestamp, altitude, latitude, longitude = get_exif_data(image)

                #...writing to csv file in append mode 'ab'
                with open('ImageMetadata.csv', 'ab') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow([filename, resolution, timestamp, datestamp, altitude, latitude, longitude])
                    csvfile.close()
                    
            except:
                print 'Unable to load ' +filename


#calling main module
if __name__ == '__main__':
    main()
