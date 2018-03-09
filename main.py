import xml.etree.ElementTree as ET
import copy
from PIL import Image


class PhotoClass:

    def __init__(self, width, height, depth):

        self.width = width
        self.height = height
        self.depth = depth

    def __str__(self):

        return "photo: width=" + str(width) + ", height=" + str(height)


    def segment(self, bndboxClass, sub_width, sub_height):

        # exclude exceptions

        b_toobig = False

        if sub_width < bndboxClass.xmax - bndboxClass.xmin:
            b_toobig = True
            sub_width = bndboxClass.xmax - bndboxClass.xmin + 2

        if sub_height < bndboxClass.ymax - bndboxClass.ymin:
            b_toobig = True
            sub_height = bndboxClass.ymax - bndboxClass.ymin + 2

        if b_toobig:
            return self.segment(bndboxClass, sub_width, sub_height)


        center_x = (bndboxClass.xmax + bndboxClass.xmin) / 2
        center_y = (bndboxClass.ymax + bndboxClass.ymin) / 2

        min_x = int(center_x - sub_width / 2)
        max_x = int(center_x + sub_width / 2)
        min_y = int(center_y - sub_height / 2)
        max_y = int(center_y + sub_height / 2)

        # get drift on x and y

        if min_x < 0:
            drift_x = 0 - min_x
            print "drift right..."
        elif max_x > width:
            drift_x = width - max_x
            print "drift left..."
        else :
            drift_x = 0

        if min_y < 0:
            drift_y = 0 - min_y
            print "drift up...\n"
        elif max_y > height:
            drift_y = height - max_y
            print "drift down...\n"
        else:
            drift_y = 0

        min_x  = min_x + drift_x
        min_y = min_y + drift_y
        max_x = max_x + drift_x
        max_y = max_y + drift_y

        return [min_x, min_y, max_x, max_y]

    def segmentAll(self, bndboxClasses, sub_width, sub_height, frames, bndboxClasses_original):

        if len(bndboxClasses) == 0:
            return

        bndboxClass = bndboxClasses.pop()
        bndboxClasses_original.append(copy.deepcopy(bndboxClass))

        [min_x, min_y, max_x, max_y] = self.segment(bndboxClass, sub_width, sub_height)
        frames.append([min_x, min_y, max_x, max_y])

        while len(bndboxClasses) > 0:

            b_inside = self.IsInsideFrame(bndboxClasses[-1], min_x, min_y, max_x, max_y)

            if b_inside:

                bndboxClass = bndboxClasses.pop()
                bndboxClasses_original.append(bndboxClass)
                continue
            else:

                self.segmentAll(bndboxClasses, sub_width, sub_height, frames, bndboxClasses_original)

        return frames, bndboxClasses_original

    def exportXml(self, frames, bndboxClasses, tree):

        for i in range(len(frames)):

            tree_copy = copy.deepcopy(tree)

            root = tree_copy.getroot()
            #root_copy = copy.deepcopy(root)

            for obj in root.findall('object'):

                bndboxXml = obj.find('bndbox')
                xmin = int(bndboxXml.find('xmin').text)
                ymin = int(bndboxXml.find('ymin').text)
                xmax = int(bndboxXml.find('xmax').text)
                ymax = int(bndboxXml.find('ymax').text)

                if not (xmin > frames[i][0] and ymin > frames[i][1] and xmax < frames[i][2] and ymax < frames[i][3]):

                    root.remove(obj)
                else:

                    xmin = xmin - frames[i][0]
                    ymin = ymin - frames[i][1]
                    xmax = xmax - frames[i][0]
                    ymax = ymax - frames[i][1]

                bndboxXml.find('xmin').text = str(xmin)
                bndboxXml.find('ymin').text = str(ymin)
                bndboxXml.find('xmax').text = str(xmax)
                bndboxXml.find('ymax').text = str(ymax)

                # bndboxXml.set('updated', 'yes')

            root.find('size').find('width').text = str(frames[i][2] - frames[i][0])
            root.find('size').find('height').text = str(frames[i][3] - frames[i][1])

            # root.set('updated', 'yes')


            tree_copy.write('output' + str(i) + ".xml")


    def exportSubImage(self, cropSize, imageName, index):

        img = Image.open(imageName)
        area = cropSize
        cropped_image = img.crop(area)
        cropped_image.save(imageName + str(index) + ".jpg")



    def IsInsideFrame(self, bndboxClass, min_x, min_y, max_x, max_y):

        return min_x <= bndboxClass.xmin and min_y <= bndboxClass.ymin and max_x >= bndboxClass.xmax and max_y >= bndboxClass.ymax




class BndboxClass:

    #xmin, ymin, xmax, ymax = -1, -1, -1, -1

    def __init__(self, xmin, ymin, xmax, ymax):

        self.xmin = int(xmin)
        self.ymin = int(ymin)
        self.xmax = int(xmax)
        self.ymax = int(ymax)

    def __str__(self):

        return "(" + str(self.xmin) + "," + str(self.ymin) + "), (" + str(self.xmax) + "," + str(self.ymax) + ")"



if __name__ == '__main__':

    source = "/home/zhida/Documents/Code/labelImg/labelImg/xml/1.JPGresize.xml"
    tree = ET.parse(source)
    root = tree.getroot()

    print root.tag

    # element array
    bndboxs = root.findall("./object/bndbox")
    bndboxClasses = []


    # fetch bndboxs

    for i in range(len(bndboxs)):

        bndbox = bndboxs[i]

        xmin = bndbox.find("xmin").text
        ymin = bndbox.find("ymin").text
        xmax = bndbox.find("xmax").text
        ymax = bndbox.find("ymax").text

        bndboxClass = BndboxClass(xmin=xmin, ymin=ymin, xmax=xmax, ymax=ymax)

        bndboxClasses.append(copy.deepcopy(bndboxClass))

    for i in range(len(bndboxClasses)):
        print(bndboxClasses[i])


    # fetch photo info

    sizeXml = root.find("size")
    width = int(sizeXml.find("width").text)
    height = int(sizeXml.find("height").text)
    depth = int(sizeXml.find("depth").text)

    photoClass = PhotoClass(width=width, height=height, depth=depth)

    print(photoClass)

    sub_width = width / 2
    sub_height = height / 2

    frames = []
    frames, bndboxClasses = photoClass.segmentAll(bndboxClasses, sub_width, sub_height, frames, [])

    print frames


    # export xml
    photoClass.exportXml(frames, bndboxClasses, tree)

    # export sub images
    imageName = "/home/zhida/Documents/Code/pva-faster-rcnn/data/VOCdevkit2007/VOC2007/JPEGImages/1.JPGresize.jpg"

    for i in range(len(frames)):

        cropsize = (frames[i][0], frames[i][1], frames[i][2], frames[i][3])
        photoClass.exportSubImage(cropsize, imageName, i)





