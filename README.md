# LIDARtoolkit
> **Currently in development

A python toolkit  published on pypi for simplifying LIDAR point cloud processing and rapid prototyping.

## Requirements
- Python 3.5+
- Numpy

## Install
`$ pip3 install LiDARtoolkit`  
or  
`$ python3 -m pip install LiDARtoolkit`

Note: This toolkit is not compatible for python versions below 3.5

## Tools
### removeGround(pointcloud, bin\_size = 0.0625, error\_limit = 0.2)
#### Returns: Pointcloud without ground
This function removes the ground points in the point cloud data by binning the points in the x-y plane and removing the lowermost points. Resolution and quality of output can be changed by changing the bin\_size parameter. error\_limit defines the margin to which the points will be removed from the bottom.

### separateObjects(pointcloud, min\_samples = 15, eps = 0.8, dim = 2)
#### Returns: Object array, Color array
This function separates the objects in the point cloud by performing density based clustering on the points either in 3 dimensions or in the x-y plane as specified by the dim parameter (3 for 3d and 2 for 2d). min\_samples define minimum number of points to be called as a cluster while eps defines the maximum distance between these points. The color array is used just for plotting the points with different colors.

### rotateBy(point, theta)
#### Returns: Transformed point
This function returns the point rotated by angle theta in the x-y plane by just multipying by the rotation matrix.

### def findBox(object)
#### Returns: Array of eight points of bounding box, angle of the bounding box in x-y plane
This function returns the minimum bounding box of the object point cloud by rotating the object and finding the rectangle of minimum area that bounds it.

## PyPi
[https://pypi.org/project/LiDARtoolkit/](https://pypi.org/project/LiDARtoolkit/)
