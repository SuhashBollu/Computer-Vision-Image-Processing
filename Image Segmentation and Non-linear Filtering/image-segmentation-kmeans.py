import utils
import numpy as np
import json
import time

def combinations(seqnce, r):
    all_elements = tuple(seqnce)
    n = len(all_elements)
    if r > n:
        return
    index_values = list(range(r))
    yield tuple(all_elements[i] for i in index_values)
    while True:
        for i in reversed(range(r)):
            if index_values[i] != i + n - r:
                break
        else:
            return
        index_values[i] += 1
        for j in range(i+1, r):
            index_values[j] = index_values[j-1] + 1
        yield tuple(all_elements[i] for i in index_values)

def kmeans(img,k):
    """
    Implement kmeans clustering on the given image.
    Steps:
    (1) Random initialize the centers.
    (2) Calculate distances and update centers, stop when centers do not change.
    (3) Iterate all initializations and return the best result.
    Arg: Input image;
         Number of K. 
    Return: Clustering center values;
            Clustering labels of all pixels;
            Minimum summation of distance between each pixel and its center.  
    """
    # TODO: implement this function.
    arr = np.asarray(img)
    rows,columns = np.shape(arr)
    labels = [[None for i in range(columns)]for j in range(rows)]
    distinct_intensities = set(arr.flatten())
    rand_points = [ np.random.choice(list(distinct_intensities), replace=False) for i in range(k) ]
    combins = list(combinations(list(distinct_intensities), 2))
    hist, bins = np.histogram(arr,256,[0,256])
    min_centers=[]
    min_sum_dist=float('inf')
    initialization = 1
    finalpoints_centroid1=[]
    finalpoints_centroid2=[]
    for rand_center in combins:
        centroid_1avg=0
        centroid_2avg=0
        diff1=float('-inf')
        diff2=float('-inf')
        iter=0
        centers=[]
        sum_dist=0
        while(diff1!=0 and diff2!=0):
            if iter==0:
                cent1 = rand_center[0]
                cent2 = rand_center[1]
            else:
                cent1 = centroid_1avg
                cent2 = centroid_2avg

            intensity_list_centroid1=[]
            intensity_list_centroid2=[]
            sum1=0
            sum2=0
            for j,val in enumerate(hist):
                if abs(j-cent1)<abs(j-cent2):
                    intensity_list_centroid1.append(val)
                    sum1 = sum1+(j*val)
                else:
                    intensity_list_centroid2.append(val)
                    sum2 = sum2+(j*val)
            if(sum(intensity_list_centroid1)!=0):
                centroid_1avg = int(sum1)/sum(intensity_list_centroid1)
            if(sum(intensity_list_centroid2)!=0):
                centroid_2avg = int(sum2)/sum(intensity_list_centroid2)
            diff1=cent1-centroid_1avg
            diff2=cent2-centroid_2avg
            iter=iter+1
        centers.append(centroid_1avg)
        centers.append(centroid_2avg)
        for j,val in enumerate(hist):
            if abs(j-centers[0])<abs(j-centers[1]):
                sum_dist += val*abs(j-centers[0])
            else:
                sum_dist += val*abs(j-centers[1])
        if sum_dist<min_sum_dist:
            min_sum_dist = sum_dist
            min_centers = centers.copy()
        initialization=initialization+1
    
    for j, val in enumerate(hist):
        if abs(j-min_centers[0])<abs(j-min_centers[1]):
            finalpoints_centroid1.append(j)
        else:
            finalpoints_centroid2.append(j)

    for i in range(rows):
        for j in range(columns):
            if finalpoints_centroid1.__contains__(arr[i][j]):
                labels[i][j]=0
            else:
                labels[i][j]=1
    return min_centers, labels, min_sum_dist


def visualize(centers,labels):
    """
    Convert the image to segmentation map replacing each pixel value with its center.
    Arg: Clustering center values;
         Clustering labels of all pixels. 
    Return: Segmentation map.
    """
    arr = np.asarray(labels)
    rows,columns = arr.shape
    imap=[[None for i in range(rows)]for j in range(columns)]
    for i in range(rows):
        for j in range(columns):
            if labels[i][j] == 0:
                imap[i][j] = centers[0]
            else:
                imap[i][j] = centers[1]
    result = np.asarray(imap)
    result = result.astype(np.uint8)
    return result
    # TODO: implement this function.

     
if __name__ == "__main__":
    img = utils.read_image('lenna.png')
    k = 2

    start_time = time.time()
    centers, labels, sumdistance = kmeans(img,k)
    result = visualize(centers, labels)
    end_time = time.time()

    running_time = end_time - start_time
    print(running_time)

    centers = list(centers)
    with open('results/task1.json', "w") as jsonFile:
        jsonFile.write(json.dumps({"centers":centers, "distance":sumdistance, "time":running_time}))
    utils.write_image(result, 'results/task1_result.jpg')
