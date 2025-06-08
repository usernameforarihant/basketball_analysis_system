import supervision as sv

class CourtKeypointsDrawer:
    def __init__(self):
        self.keypoint_color="#ff2c2c"

    def draw(self,frames,court_keypoints):
        vertex_annotator=sv.VertexAnnotator(color=sv.Color.from_hex(self.keypoint_color),radius=8)
        vertex_label_annotator=sv.VertexLabelAnnotator(color=sv.Color.from_hex(self.keypoint_color),text_color=sv.Color.WHITE,text_scale=0.5,text_thickness=1)
        output_frames=[] 
        for index,frame in enumerate(frames):
            annotate_frame=frame.copy()
            keypoints=court_keypoints[index]
            keypoints_numpy=keypoints.cpu().numpy()
            annotate_frame=vertex_annotator.annotate(scene=annotate_frame,key_points=keypoints)
            annotate_frame=vertex_label_annotator.annotate(scene=annotate_frame,key_points=keypoints_numpy)
            output_frames.append(annotate_frame)

        return output_frames
