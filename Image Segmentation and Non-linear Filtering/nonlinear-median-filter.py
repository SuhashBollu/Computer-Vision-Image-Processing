import utils
import numpy as np
import json


def crop(img, xmin, xmax, ymin, ymax):
    if len(img) < xmax:
        print('WARNING')
    patch = img[xmin: xmax]
    patch = [row[ymin: ymax] for row in patch]
    return patch

def median_filter(img):
    """
    Implement median filter on the given image.
    Steps:
    (1) Pad the image with zero to ensure that the output is of the same size as the input image.
    (2) Calculate the filtered image.
    Arg: Input image. 
    Return: Filtered image.
    """
    # TODO: implement this function.
    pad_img = utils.zero_pad(img,1,1)
    output_img = np.zeros_like(img)
    lenth = 3
    img = [list(row) for row in img]
    for x, row in enumerate(img):
        for y, num in enumerate(row):
            if(x<len(img[0])-1 or y<len(img)-1):
                output_img[x][y] = np.median(crop(pad_img, x, x+lenth, y, y+lenth))
    return output_img


def mse(img1, img2):
    """
    Calculate mean square error of two images.
    Arg: Two images to be compared.
    Return: Mean square error.
    """  
    return np.square(np.subtract(img1, img2)).mean()
    # TODO: implement this function.
    

if __name__ == "__main__":
    img = utils.read_image('lenna-noise.png')
    gt = utils.read_image('lenna-denoise.png')

    result = median_filter(img)
    error = mse(gt, result)

    with open('results/task2.json', "w") as file:
        json.dump(error, file)
    utils.write_image(result,'results/task2_result.jpg')


