from PIL import Image
import os
import ntpath


if __name__ == '__main__':

    # the ratio of sub image to original image. If the ratio is 3, the original image will be cropped to 3*3 = 9 images.
    ratio_x = 1
    ratio_y = 3

    imageDirectory = "/home/zhida/Documents/Code/pva-faster-rcnn/data/VOCdevkit2007/VOC2007/JPEGImages-for-test"
    croppedDirectory = "/home/zhida/Documents/Code/pva-faster-rcnn/data/VOCdevkit2007/VOC2007/JPEGImages-for-test-cropped"

    for file in os.listdir(imageDirectory):

        img = Image.open(imageDirectory + "/" + file)

        size = img.size
        num_x = ratio_x + 1
        num_y = ratio_y + 1
        unit_x = int(size[0] / num_x)
        unit_y = int(size[1] / num_y)
        #sub_width = int(size[0] / ratio_x)
        #sub_height = int(size[1] / ratio_y)

        for i in range(ratio_x):

            for j in range(ratio_y):

                min_x = i * unit_x + 0
                min_y = j * unit_y + 0
                max_x = i * unit_x + 2 * unit_x
                max_y = j * unit_y + 2 * unit_y

                sub_size = (min_x, min_y, max_x, max_y)

                cropped_image = img.crop(sub_size)
                save_name = croppedDirectory + "/" + file + str(9 + i + j*(ratio_x)) + ".jpg"
                cropped_image.save(save_name, 'JPEG')
                print save_name


