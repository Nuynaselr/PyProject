from math import sqrt, inf
from skimage import color, io
import time
import numpy
from ImageList import ImageList
from tqdm import tqdm

# getting current directory

min_row = int()
min_color = int()


def search_vector(array_point_image, array_color):
    distance = 0.0
    min = inf
    for i in range(7):
        for j in range(7):
            distance = numpy.linalg.norm(numpy.array(array_point_image) - numpy.array(array_color[i][j]), ord=2)
            if min > distance:
                min = distance
                min_color = j
                min_row = i

    return min_row, min_color


def search(array_point_image, array_color):
    distance = 0.0
    min = inf
    for i in range(7):
        for j in range(7):
            distance = sqrt((array_point_image[0] - float(array_color[i][j][0])) * (
                        array_point_image[0] - float(array_color[i][j][0])) + (
                                        array_point_image[1] - float(array_color[i][j][1])) * (
                                        array_point_image[1] - float(array_color[i][j][1])) + (
                                        array_point_image[2] - float(array_color[i][j][2])) * (
                                        array_point_image[2] - float(array_color[i][j][2])))
            if min > distance:
                min = distance
                min_color = j
                min_row = i

    return min_row, min_color


if __name__ == "__main__":
    # class with directory image
    array_files_name = ImageList()
    counter = 1

    # open image
    color_map = io.imread("colour_map.png")

    # convert rpg in lab, lab - format that is closer to human
    color_map = color.rgb2lab(color_map)

    # enter in directory
    # getting list files in directory and  walk for each

    file_path = input('Enter file path: ')

    # send path on treatment
    array_files_name.set_path(file_path)

    # print current directory
    print(array_files_name.get_file_path())

    # print list image
    print('List files: ', array_files_name.get_image_list())

    # start timer
    start_time = time.time()

    for image in array_files_name.get_image_list():

        print(image)

        # open image
        image_rgb = io.imread(image)

        # getting size image
        height_image = len(image_rgb)
        width_image = len(image_rgb[0])

        # convert rpg in lab, lab - format that is closer to human
        image_lab = color.rgb2lab(image_rgb)
        for bar in tqdm(range(height_image * width_image)):
            for i in range(0, height_image):
                for j in range(0, width_image):
                    # search nearest color
                    min_row, min_color = search(image_lab[i][j], color_map)
                    # print('min_row: ', min_row, 'min_color: ', min_color)

                    # replacement color
                    image_lab[i][j] = color_map[min_row][min_color]

        # treatment lab into rgb
        image_rgb = color.lab2rgb(image_lab)

        # name for treatment image
        file_name = "treat_" + str(counter) + ".jpg"
        counter += 1

        # save treatment
        io.imsave(file_name, image_rgb)

        print("Success ", file_name)

    print(time.time() - start_time)
    # 3 minutes 53 seconds = 212 seconds
