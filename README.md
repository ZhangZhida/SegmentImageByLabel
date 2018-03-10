# SegmentImageByLabel

Functions:

  This program is an assist tool for caffe network training. Sometimes the image size is too large, while the object to be detect is too small. Therefore, a common solution is to properly crop the image to a smaller size to increase the relative size of the object. This program solves this problem by cropping the original image and creates xml files from the original xml files. 

  Input: imageDirectory, xmlDirectory

  Output: cropped images in newImageDirectory, new xmls in newXmlDirectory
