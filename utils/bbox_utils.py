def get_center_of_bbox(bbox):
    """
    Calculate the center of a bounding box.

    :param bbox: A tuple (x, y, width, height) representing the bounding box.
    :return: A tuple (center_x, center_y) representing the center of the bounding box.
    """
    x1, y1, x2, y2 = bbox
    center_x = int((x1 + x2) / 2)
    center_y = int((y1 + y2) / 2)
    return center_x, center_y

def get_bbox_width(bbox):
    x1, y1, x2, y2 = bbox
    return bbox[2] - bbox[0]

def measure_distance(p1,p2):
    return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5

def get_center_of_bbox(bbox):
    x1, y1, x2, y2 = bbox
    center_x = int((x1 + x2) / 2)
    center_y = int((y1 + y2) / 2)
    return center_x, center_y

def get_foot_positions(bbox):
    x1, y1, x2, y2 = bbox
    return int((x1+x2)/2),y2
