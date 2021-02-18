import cv2
import pyAprilTag
import numpy as np
import matplotlib.pyplot as plt
def box_drawing(_image_, _corners_, _imagepoints_):
    for i in range(0,15):
        _image_ = cv2.line(_image_, (_imagepoints_[i,0,0],_imagepoints_[i,0,1]),(_imagepoints_[i+1,0,0],_imagepoints_[i+1,0,1]),(255),3)      
    return _image_
distortion=np.array([[ -0.12572225], [0.23407207],  [0.00346949],  [0.00183746],[  0]])
K=np.float32([[788.53833244,0,641.3123704 ],[0,788.48461472,358.01028946],[  0, 0, 1]])
capture_store = cv2.VideoCapture(0)
box_axis = np.float32([[0,0,0], [0,160,0], [160,160,0], [160,0,0], [0,0,0],
                   [0,0,-160],[0,160,-160],[0,160,0],[0,160,-160],[160,160,-160],
                   [160,160,0],[160,160,-160],[160,0,-160],[160,0,0],[160,0,-160],[0,0,-160]])
image_base=cv2.imread('calib_pattern_Tag36h11.png')
if not capture_store.isOpened():
    capture_store = cv2.VideoCapture(camid+cv2.CAP_DSHOW)
capture_store.set(cv2.CAP_PROP_FPS, 60)
capture_store.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
capture_store.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
print('{:d}x{:d} Pixel ratio @ {:d} Frequency (Hz)'.format(
    int(capture_store.get(cv2.CAP_PROP_FRAME_WIDTH)),
    int(capture_store.get(cv2.CAP_PROP_FRAME_HEIGHT)),
    int(capture_store.get(cv2.CAP_PROP_FPS))))
if not capture_store.isOpened():
    print("Camera not working")
    exit(0)
while capture_store.isOpened():
    RET, frame_read = capture_store.read()
    frame_copy=frame_read.copy()
    if not RET:
        break
    if frame_read.shape[0]>640:
        frame_read = cv2.resize(frame_read, (640, 480))
    ID, corners, centers, _hs_ = pyAprilTag.find(frame_read)
    if(corners.size!=0):
        points_src=np.float64((5,3))
        points_dist=np.float32((5,3))
        x = 0
        for i in range(ID.shape[0]):
            if ID[i]==2:
                x = i
                points_dist = np.float64([[[corners[x,0,0]],[corners[x,0,1]]],[[corners[x,1,0]],[corners[x,1,1]]],[[corners[x,2,0]],[corners[x,2,1]]],[[corners[x,3,0]],[corners[x,3,1]]],[[centers[x,0]],[centers[x,1]]]]) 
                points_src = np.float32([[[0],[160],[0]],[[160],[160],[0]],[[160], [0],[0]],[[0], [0],[0]],[[80],[80],[0]]])
                RET, R, T = cv2.solvePnP(points_src, points_dist, K, distortion)
                image_points, JAC = cv2.projectPoints(box_axis, R, T, K, distortion)
                img = box_drawing(frame_copy,points_src,image_points)       
                window=cv2.namedWindow("Cube", cv2.WINDOW_NORMAL)
                cv2.resizeWindow("Cube", 1080,720)
                cv2.imshow("Cube",img)
        if cv2.waitKey(10) == 27:
            break
capture_store.release()
cv2.destroyAllWindows()