import cv2
import numpy as np
import random
def getHomography(kpsA, kpsB, featuresA, featuresB, matches, reprojThresh):
    # convert the keypoints to numpy arrays
    kpsA = np.float32([kp.pt for kp in kpsA])
    kpsB = np.float32([kp.pt for kp in kpsB])
    if len(matches) > 4:
        # construct the two sets of points
        ptsA = np.float32([kpsA[m.queryIdx] for m in matches])
        ptsB = np.float32([kpsB[m.trainIdx] for m in matches])
        # estimate the homography between the sets of points
        (H, status) = cv2.findHomography(ptsA, ptsB, cv2.RANSAC,reprojThresh)
        return (matches, H, status)
    else:
        return None

def solution(left_img, right_img):
    """
    :param left_img:
    :param right_img:
    :return: you need to return the result image which is stitched by left_img and right_img
    """
    sift = cv2.ORB_create()
    kp1, des1 = sift.detectAndCompute(right_img,None)
    kp2, des2 = sift.detectAndCompute(left_img,None)
    bf = cv2.BFMatcher(cv2.NORM_HAMMING)
    matches = bf.knnMatch(des1, des2,2)
    good = []
    for m,n in matches:
        if m.distance < 0.75*n.distance:
            good.append(m)
    #draw_params = dict(matchColor=(0,255,0),singlePointColor=None,flags=2)
    #img3 = cv2.drawMatches(left_img,kp1,left_img,kp2,good,None,**draw_params)
    #cv2.imshow("original_image_drawMatches.jpg", img3)
    #cv2.waitKey(0)

    M = getHomography(kp1, kp2, des1, des2, good, reprojThresh=4)
    if M is None:
        print("Error!")
    (matches, H, status) = M
    #print(H)

    width = right_img.shape[1] + left_img.shape[1]
    height = right_img.shape[0] + left_img.shape[0]

    result = cv2.warpPerspective(right_img, H, (width, height))
    #cv2.imshow("abc",result)
    #cv2.waitKey(0)
    result[0:left_img.shape[0], 0:left_img.shape[1]] = left_img
    crop_img = result[0:left_img.shape[0], 0:left_img.shape[1]+right_img.shape[1]]
    #cv2.imshow("abc1",crop_img)
    #cv2.waitKey(0)

    #l = 0
    #print(result.shape[0])
    #print(result.shape[1])
    #for i in range(result.shape[1]):
    #    #print(crop_img[0][i][0])
    #    if (result[0][i][0]==0 and result[0][i][1]==0 and result[0][i][2]==0): 
    #        break
    #    else:
    #        l=l+1
    #print(l)
    #crop_img = result[0:left_img.shape[0], 0:l]
    #cv2.imshow("result.jpg", crop_img)
    #cv2.waitKey(0)

    return crop_img

    raise NotImplementedError

if __name__ == "__main__":
    left_img = cv2.imread('left.jpg')
    right_img = cv2.imread('right.jpg')
    result_image = solution(left_img, right_img)
    cv2.imwrite('results/task2_result.jpg',result_image)


