import random
import sys
def find_line_params(points):
    eps = sys.float_info.epsilon
    m = (points[1][1]-points[0][1])/(points[1][0]-points[0][0]+eps)
    c = points[1][1]-m*points[0][1]
    return m,c

def find_intercept(m,c,x,y):
    x = (x + m*y - m*c)/(1 + m**2)
    y = (m*x + (m**2)*y - (m**2)*c)/(1 + m**2) + c
    return x, y

def solution(input_points, t, d, k):
    """
    :param input_points:
           t: t is the perpendicular distance threshold from a point to a line
           d: d is the number of nearby points required to assert a model fits well, you may not need this parameter
           k: k is the number of iteration times
           Note that, n for line should be 2
           (more information can be found on the page 90 of slides "Image Features and Matching")
    :return: inlier_points_name, outlier_points_name
    inlier_points_name and outlier_points_name is two list, each element of them is str type.
    For example: If 'a','b' is inlier_points and 'c' is outlier_point.
    the output should be two lists of ['a', 'b'], ['c'].
    Note that, these two lists should be non-empty.
    """
    n=2
    fin_liers=[]
    best_error = 10000
    for i in range(k):
        in_liers  = []
        out_liers = []
        rd_points = random.sample(input_points,n)
        rem_points = input_points.copy()
        for i in range(len(rd_points)):
            rem_points.remove(rd_points[i])
        rd_in_points=[]
        best_fit_points=[]
        dists=[]
        for x in range(len(rd_points)):
            #print("rds")
            #print(rd_points[0]['name'])
            #print(rd_points[1]['name'])
            #print("rde")
            rd_in_points.append(rd_points[x]['value'])
        if(rd_in_points[1][0]-rd_in_points[0][0]!=0):
            a,b = find_line_params(rd_in_points)
            in_liers.append(rd_points[0])
            in_liers.append(rd_points[1])
            rem_in_points=[]
            for x in range(len(rem_points)):
                rem_in_points.append(rem_points[x]['value'])
            for i in range(len(rem_in_points)):
                x0 = rem_in_points[i][0]
                y0 = rem_in_points[i][1]
                x1, y1 = find_intercept(a,b,x0,y0)
                dist = ((x1 - x0)**2 + (y1 - y0)**2)**0.5
                if dist < t:
                    dists.append(dist**2)
                    #print(dist)
                    in_liers.append(rem_points[i])
            #print("\n")
        if(len(in_liers)>=d+2):
            #print("inliers")
            #for i in in_liers:
            #    print(i['name'])
            #print("\n")
            #print(len(in_liers))
            total=0
            for i in dists:
                total = total+i
            error = total/len(dists)-2
            #print(error)
            if(error<best_error):
                #print(rd_in_points)
                #for i in in_liers:
                #    print(i['name'])
                #print(len(in_liers))
                #print("error",error)
                best_error=error
                best_fit_points =rd_points
                #print("bestfit",best_fit_points)
                fin_liers=in_liers.copy()
            #break
    #print("finliers",fin_liers)
    out_liers = input_points.copy()
    for i in range(len(fin_liers)):
        out_liers.remove(fin_liers[i])
    finl=[]
    fotl=[]

    for i in fin_liers:
        finl.append(i['name'])

    for i in out_liers:
        fotl.append(i['name'])

    #print(finl)
    #print(fotl)
    return finl, fotl
    # TODO: implement this function.
    raise NotImplementedError


if __name__ == "__main__":
    input_points = [{'name': 'a', 'value': (0.0, 1.0)}, {'name': 'b', 'value': (2.0, 1.0)},
                    {'name': 'c', 'value': (3.0, 1.0)}, {'name': 'd', 'value': (0.0, 3.0)},
                    {'name': 'e', 'value': (1.0, 2.0)}, {'name': 'f', 'value': (1.5, 1.5)},
                    {'name': 'g', 'value': (1.0, 1.0)}, {'name': 'h', 'value': (1.5, 2.0)}]
    t = 0.5
    d = 3
    k = 100
    inlier_points_name, outlier_points_name = solution(input_points, t, d, k)  # TODO
    assert len(inlier_points_name) + len(outlier_points_name) == 8  
    f = open('./results/task1_result.txt', 'w')
    f.write('inlier points: ')
    for inliers in inlier_points_name:
        f.write(inliers + ',')
    f.write('\n')
    f.write('outlier points: ')
    for outliers in outlier_points_name:
        f.write(outliers + ',')
    f.close()


