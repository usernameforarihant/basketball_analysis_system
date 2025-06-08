import cv2
import sys
import numpy as np
sys.path.append("../")  # Adjust the path to import utils from the parent directory
from utils import get_center_of_bbox,get_bbox_width

def draw_ellipse(frame, bbox, color,track_id=None):
    """
    Draws an ellipse on the given frame based on the bounding box.

    :param frame: The video frame on which to draw.
    :param bbox: A tuple (x, y, width, height) representing the bounding box.
    :param color: A tuple (B, G, R) representing the color of the ellipse.
    :return: The modified frame with the ellipse drawn.
    """
    y2=int(bbox[3])
    x_center,_ = get_center_of_bbox(bbox)
    width = get_bbox_width(bbox)
    cv2.ellipse(
    frame,
    center=(int(x_center), int(y2)),  # Make sure coordinates are integers
    axes=(int(width), int(0.35 * width)),  # axes: (major, minor)
    angle=0.0,       # angle of rotation
    startAngle=-45,     # startAngle
    endAngle=235,     # endAngle
    color=color,   # color
    thickness=2,       # thickness
    lineType=cv2.LINE_4  )

    
    rectagle_width=40
    rectagle_height=20
    x1_rect = x_center - rectagle_width // 2
    x2_rect = x_center + rectagle_width // 2
    y1_rect = (y2 - rectagle_height//2)+15
    y2_rect = (y2+rectagle_height//2)+15

    if track_id is not None:
        cv2.rectangle(frame, (int(x1_rect), int(y1_rect)), (int(x2_rect), int(y2_rect)), color, cv2.FILLED)
        x1_text=x1_rect+12
        if track_id>99:
            x1_text-=10 
        cv2.putText(frame, f"{track_id}", (int(x1_text), int(y1_rect +15) ), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0,0),2)
    
    return frame

def draw_triangle(frame, bbox, color):
    y=int(bbox[1])
    x, _ = get_center_of_bbox(bbox)
    triangle_points = np.array([
        [x, y],
        [x - 10, y - 10],
        [x + 10, y - 10]
    ], dtype=np.int32)

    triangle_points = triangle_points.reshape((-1, 1, 2)) 
    cv2.drawContours(frame, [triangle_points], 0, color, cv2.FILLED)
    cv2.drawContours(frame, [triangle_points], 0,(0,0,0), 2)
    return frame
   