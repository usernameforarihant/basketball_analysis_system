from ultralytics import YOLO
from utils import read_stubs, save_stubs
import numpy as np
import supervision as sv
import pandas as pd
class BallTracker:
    def __init__(self,modelpath):
        self.model=YOLO(modelpath)
        
    def detect_frames(self,frames): #detect  frames
        batch_size=20
        detections=[]
        for i in range(0,len(frames),batch_size):
            batch_frames=frames[i:i+batch_size]
            batch_detections=self.model.predict(batch_frames,conf=0.5)
            detections+=batch_detections
        return detections
    def get_object_tracks(self,frames,read_from_stubs=False,stub_path=None): #detects objects in frames

        tracks=read_stubs(read_from_stubs,stub_path)
        if tracks is not None:
            if len(tracks) == len(frames):
                return tracks
        
        detections=self.detect_frames(frames)
        tracks=[]
        for frame_num,detection in enumerate(detections):
            cls_names=detection.names
            cls_name_inverse={v:k for k,v in cls_names.items()}
            
            detection_supervision= sv.Detections.from_ultralytics(detection)
            tracks.append({})
            chosen_bbox=None
            max_conf=0

            for frame_detection in detection_supervision:
                bbox=frame_detection[0].tolist()
                cls_id=frame_detection[3]
                conf=frame_detection[2]
                if cls_id==cls_name_inverse["Ball"]:
                    if max_conf < conf:
                        chosen_bbox = bbox
                        max_conf = conf
            if chosen_bbox is not None:
                tracks[frame_num][1] = {"box": chosen_bbox}


        save_stubs(stub_path, tracks)
        return tracks
    
    def remove_wrong_detections(self,ball_positions):
        max_allowed_distance=25
        last_good_frame_index=-1
        for i in range(len(ball_positions)):
            current_bbox=ball_positions[i].get(1,{}).get("box", {})
            if len(current_bbox) == 0:
                continue
            if last_good_frame_index == -1:
                last_good_frame_index = i
                continue
            last_good_box=ball_positions[last_good_frame_index].get(1,{}).get("box", {})
            frame_gap=i-last_good_frame_index
            adjusted_max_distance=max_allowed_distance*frame_gap 

            #calcualte the distance between the last good box and the current box
            if np.linalg.norm(np.array(last_good_box[:2])- np.array(current_bbox[:2])) > adjusted_max_distance:
                ball_positions[i]={}
            else:
                last_good_frame_index=i
        return ball_positions
    
    # def interpolate_ball_positions(self,ball_positions):
    #     # print("Sample ball_positions:", ball_positions[:3])
    #     # print("Type of first element:", type(ball_positions[0]))

    #     ball_positions=[x.get(1,{}).get("box", {}) for x in ball_positions]
    #     df_ball_positions=pd.DataFrame(ball_positions,columns=["x1","y1","x2","y2"])

    #     #interpolate missing values
    #     df_ball_positions=df_ball_positions.interpolate()
    #     df_ball_positions=df_ball_positions.bfill()

    #     ball_positions=[{1:{'box':x}} for x in df_ball_positions.to_numpy().tolist()]
        
    #     return ball_positions

    def interpolate_ball_positions(self, ball_positions):
    # Convert to list of bounding boxes, replacing missing ones with None
        processed_positions = []
        for frame_data in ball_positions:
            if isinstance(frame_data, dict) and 1 in frame_data and "box" in frame_data[1]:
                processed_positions.append(frame_data[1]["box"])
            else:
                processed_positions.append([None, None, None, None])

        # Create DataFrame for interpolation
        df_ball_positions = pd.DataFrame(processed_positions, columns=["x1", "y1", "x2", "y2"])

        # Interpolate and backfill
        df_ball_positions = df_ball_positions.interpolate()
        df_ball_positions = df_ball_positions.bfill()

        # Re-wrap in original dict format
        interpolated_ball_positions = [{1: {'box': row}} for row in df_ball_positions.to_numpy().tolist()]

        return interpolated_ball_positions