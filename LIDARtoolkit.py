def removeGround(pointcloud, bin_size = 0.0625, error_limit = 0.2):
    #Finding the range of pointcloud
    minx = pointcloud[0][0]
    miny = pointcloud[0][1]
    maxx = pointcloud[0][0]
    maxy = pointcloud[0][1]
    for i in range(len(pointcloud)):
        point = pointcloud[i]
        if point[0] > maxx:
            maxx = point[0]
        if point[0] < minx:
            minx = point[0]
        if point[1] > maxy:
            maxy = point[1]
        if point[1] < miny:
            miny = point[1]
    #Creating bins array
    bins = []
    for i in range(int((maxx-minx)/bin_size)+1):
        temp = []
        for j in range(int((maxy-miny)/bin_size)+1):
            temp.append([])
        bins.append(temp)
    #Hashing points in  bins
    for i in range(len(pointcloud)):
        point = pointcloud[i]
        bins[int((point[0]-minx)/bin_size)][int((point[1]-miny)/bin_size)].append(point)
    #Ground removal in each bin
    for i in range(len(bins)):
        for j in range(len(bins[0])):
            if len(bins[i][j])>0:
                minz = bins[i][j][0][2]
                for point in bins[i][j]:
                    if point[2]<minz:
                        minz=point[2]
                k=0
                while k < len(bins[i][j]):
                    if bins[i][j][k][2] < minz + error_limit:
                        del bins[i][j][k]
                        k-=1
                    k+=1
    #Concatinating all points
    import pandas
    outPointcloud = []
    for row in bins:
        for bin in row:
            outPointcloud += bin
    return pandas.DataFrame(outPointcloud)

def separateObjects(pointcloud, min_samples = 15, eps = 0.8, dim = 2):
    from sklearn.cluster import DBSCAN
    import numpy
    if dim > 3:
        raise Exception('Dimension should be less than or equal to 4. The value of dim was {}'.format(dim))
    cluster = DBSCAN(min_samples = min_samples, eps = eps)
    P = []
    for i in range(len(pointcloud)):
        point = pointcloud[i]
        P.append(point[:dim])
    cluster.fit(P)
    objects = [[] for x in range(max(cluster.labels_)+1)]
    color_map = [numpy.random.rand(3) for x in range(max(cluster.labels_)+1)]
    colors = []
    for i in range(len(pointcloud)):
        if cluster.labels_[i] >= 0:
            objects[cluster.labels_[i]].append(pointcloud[i])
            colors.append(color_map[cluster.labels_[i]])
        else:
            colors.append([0,0,0])
    return objects, colors

def rotateBy(a,theta):
    import math
    cos=math.cos(theta)
    sin=math.sin(theta)
    return [a[0]*cos-a[1]*sin, a[0]*sin+a[1]*cos, a[2]]

def findBox(PointCloud):
    from math import pi
    minArea=float('inf')
    arr = []
    theta = 0
    while theta<90:
        Zero = rotateBy(PointCloud[0], pi*theta/180)
        maxZ = Zero[2]
        minX = Zero[0]
        maxX = Zero[0]
        minY = Zero[1]
        maxY = Zero[1]
        minZ = Zero[2]
        for row in PointCloud:
            point = rotateBy(row, pi*theta/180)
            if point[0]<minX:
                minX = point[0]
            if point[0]>maxX:
                maxX = point[0]
            if point[1]>maxY:
                maxY = point[1]
            if point[1]<minY:
                minY = point[1]
            if point[2]>maxZ:
                maxZ = point[2]
            if point[2]<minZ:
                minZ=point[2]
        area = (maxY-minY)*(maxX-minX)
        if area<minArea:
            minArea = area
            if maxX-minX > maxY-minY:
                mintheta = pi*theta/180
            else:
                mintheta = pi/2+pi*theta/180
            arr = [rotateBy([minX,minY,minZ],-1*pi*theta/180), rotateBy([minX,maxY,minZ],-1*pi*theta/180), rotateBy([maxX,minY,minZ],-1*pi*theta/180), rotateBy([maxX,maxY,minZ],-1*pi*theta/180),rotateBy([minX,minY,maxZ],-1*pi*theta/180), rotateBy([minX,maxY,maxZ],-1*pi*theta/180), rotateBy([maxX,minY,maxZ],-1*pi*theta/180), rotateBy([maxX,maxY,maxZ],-1*pi*theta/180)]
        theta+=0.5
    return arr, mintheta
