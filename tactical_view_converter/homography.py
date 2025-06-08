import numpy as np
import cv2 
class Homography:
    def __init__(self,source :np.ndarray,target:np.ndarray,):
        if source.shape!=target.shape:
            raise ValueError("Source  and target must have same shape")
        if source.shape[1]!=2:
            return ValueError("Spurce and target must be 2d arrays")         
        self.source=source.astype(np.float32)
        self.target=target.astype(np.float32)
        self.m,_=cv2.findHomography(self.source,self.target)
        if self.m is None:
            raise ValueError("Homography matrix is None")
    
    def transform_points(self,points):
        if points.size==0:
            return points
        if points.shape[1]!=2:
            raise ValueError("Points must be 2d array")
        points=points.reshape(-1,1,2).astype(np.float32)
        transformed_points=cv2.perspectiveTransform(points,self.m)
        return transformed_points.reshape(-1,2).astype(np.float32)