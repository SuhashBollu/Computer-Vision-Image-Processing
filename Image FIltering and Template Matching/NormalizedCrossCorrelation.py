import argparse
import json
import os

import utils
import Covolution
from Convolution import *


def parse_args():
    parser = argparse.ArgumentParser(description="cse 473/573 project 1.")
    parser.add_argument(
        "--img-path",
        type=str,
        default="./data/proj1-task2.jpg",
        help="path to the image")
    parser.add_argument(
        "--template-path",
        type=str,
        default="./data/proj1-task2-template.jpg",
        help="path to the template"
    )
    parser.add_argument(
        "--result-saving-path",
        dest="rs_path",
        type=str,
        default="./results/task2.json",
        help="path to file which results are saved (do not change this arg)"
    )
    args = parser.parse_args()
    return args
#%%
def norm_xcorr2d(patch, template):
    """Computes the NCC value between a image patch and a template.

    The image patch and the template are of the same size. The formula used to compute the NCC value is:
    sum_{i,j}(x_{i,j} - x^{m}_{i,j})(y_{i,j} - y^{m}_{i,j}) / (sum_{i,j}(x_{i,j} - x^{m}_{i,j}) ** 2 * sum_{i,j}(y_{i,j} - y^{m}_{i,j})) ** 0.5
    This equation is the one shown in Prof. Yuan's ppt.
    
    Args:
        patch: nested list (int), image patch.
        template: nested list (int), template.

    Returns:
        value (float): the NCC value between a image patch and a template.

    """

    numsum = 0
    tempsum = 0
    patchsum = 0
    densum1 = 0
    densum2 = 0
    for i in range(len(template)):
        for j in range(len(template[0])):
            tempsum  += template[i][j]
            patchsum += patch[i][j]
    tempavg = tempsum/(len(template)*len(template[0]))
    patchavg = patchsum/(len(patch)*len(patch[0]))

    for i in range(len(template)):
        for j in range(len(template[0])):
            numsum += (template[i][j]-tempavg)*(patch[i][j]-patchavg)
            densum1 += (template[i][j]-tempavg)**2
            densum2 += (patch[i][j]-patchavg)**2
    if(densum1*densum2 == 0):
        return 0
    else:
        return numsum/((densum1*densum2)**0.5)
    raise NotImplementedError
#%%
def match(img, template):
    """Locates the template, i.e., a image patch, in a large image using template matching techniques, i.e., NCC.

    Args:
        img: nested list (int), image that contains character to be detected.
        template: nested list (int), template image.

    Returns:
        x (int): row that the character appears (starts from 0).
        y (int): column that the character appears (starts from 0).
        max_value (float): maximum NCC value.
    """
    # TODO: implement this function.
    # raise NotImplementedError
    final_x_cor = -1
    final_y_cor = -1
    final_max = -1
    for i, row in enumerate(img):
        for j, num in enumerate(row):
            if i > len(img)-len(template) or j > len(img[0])-len(template[0]) : 
                continue
            imgfoc = utils.crop(img,i,i+ len(template) , j , j+len(template[0]))
            ncc = norm_xcorr2d(imgfoc, template)
            if ncc > final_max :
                final_x_cor = i
                final_y_cor = j
                final_max = ncc
    return final_x_cor, final_y_cor, final_max
    raise NotImplementedError

#%%
def save_results(coordinates, template, template_name, rs_directory):
    results = {}
    results["coordinates"] = sorted(coordinates, key=lambda x: x[0])
    results["templat_size"] = (len(template), len(template[0]))
    with open(os.path.join(rs_directory, template_name), "w") as file:
        json.dump(results, file)


def main():
    args = parse_args()
    img = read_image(args.img_path)
    #template = utils.crop(img, xmin=10, xmax=30, ymin=10, ymax=30)
    # template = np.asarray(template, dtype=np.uint8)
    # cv2.imwrite("./data/proj1-task2-template.jpg", template)
    template = read_image(args.template_path)
    x, y, max_value = match(img, template)
    # The correct results are: x: 17, y: 129, max_value: 0.994
    with open(args.rs_path, "w") as file:
        json.dump({"x": x, "y": y, "value": max_value}, file)


if __name__ == "__main__":
    main()
