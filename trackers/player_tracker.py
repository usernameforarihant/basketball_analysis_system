from ultralytics import YOLO
import supervision as sv
import sys
# sys.path.append("../")  # Adjust the path as necessary to import from the parent directory
from utils import read_stubs, save_stubs

class PlayerTracker:
    def __init__(self,model_path):
        self.model=YOLO(model_path)
        self.tracker=sv.ByteTrack()
    
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
            detection_with_tracks=self.tracker.update_with_detections(detection_supervision)
            tracks.append({})
        
            for frame_detection in detection_with_tracks:
                bbox=frame_detection[0].tolist()  #extracting bounding box
                cls_id=frame_detection[3]
                track_id=int(frame_detection[4])

                if cls_id==cls_name_inverse["Player"]:
                    tracks[frame_num][track_id] = {"id": track_id, "box": bbox}

        save_stubs(stub_path, tracks)
        return tracks
