from .utils import draw_triangle
class BallTracksDrawer:
    def __init__(self):
        self.ball_pointer_color=(0,255,0)

    def draw(self,video_frames,tracks):
        output_video_frames=[]
        for framenum ,frame in enumerate(video_frames):
            output_frame=frame.copy()
            ball_dic=tracks[framenum]

            #draw player tracks
            for _,track in ball_dic.items():
                bbox=track['box']
                if bbox is  None:
                    continue
                output_frame=draw_triangle(output_frame,bbox,self.ball_pointer_color)  # Draw player track in red
            output_video_frames.append(output_frame)
        
        return output_video_frames  