# Perspective transform tool (Birds eye)

## About

Perspective transformation is a technique (geometric transformation) that can be used to generate a top view (birds eye) from a scene. Can be useful by giving more insights into the objects of interest. Usually, to find the right perspective transform much experimentation is needed, this is where this tool can support.

<p align="center"> 
<img src="./info/demo.gif" width="800">
<div align="center">Left: red dots-input tranfom, blue dots-desired transform , Right: Warped image</div>

## Features
- load and save the configuration for input, and output perspectives;
- stores the transformation matrix (direct / inverse) in *.npy format, which can be easily loaded in the desired program;
- input/output point pairs (4x2) are defined with the mouse, and the position of the points is editable, to find accurate / desired values.


## How to use it

1. install requirements (pip install numpy, opencv-python, glob);
2. run python perspective_transform_tool.py, which will load the demo;
3. put your video file in the data folder (for this work the CARLA simulator was used [1]), or edit cfg.json file to point to the right location. In case the input is an image, it can be loaded by editing the ```"files": "*.mp4"``` to ```"files": "*.png"``` in the ```cgf.json``` file. There is a test file in the ```data``` folder for testing. 
4. use the menu to generate the transform, hit 's' to save
5. load in your project the transformation matrices, and use it for something great
```
...
t_mat = numpy.load('transform.npy')
# apply perspective transform
val = cv2.perspectiveTransform (pts, t_mat)
...
```

## Resources

1. [CARLA simulator](https://carla.org/)
2. [Feature Matching + Homography to find Objects](https://docs.opencv.org/3.4/d1/de0/tutorial_py_feature_homography.html)


/Enjoy