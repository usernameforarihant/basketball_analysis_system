from .utils import draw_ellipse,draw_triangle
class PlayerTracksDrawer:
    def __init__(self,team1_color=[255,245,238],team2_color=[128,0,0]):
        self.default_player_team_id=1
        self.team1_color = team1_color
        self.team2_color = team2_color

    def draw(self,video_frames,tracks,player_assignment=None,ball_acquisition=None):

        output_video_frames=[]
        for framenum ,frame in enumerate(video_frames):
            output_frame=frame.copy()
            player_dic=tracks[framenum]
            player_assignment_for_frame=player_assignment[framenum] 
            player_id_has_ball=ball_acquisition[framenum]
            #draw player tracks
            for track_id ,player_bbox in player_dic.items():
                team_id=player_assignment_for_frame.get(track_id,self.default_player_team_id)
                if team_id==1:
                    color=self.team1_color
                else:
                    color=self.team2_color
                if track_id==player_id_has_ball:
                    output_frame=draw_triangle(output_frame,player_bbox['box'],(0,0,255))  # Draw player with ball in triangle
                output_frame=draw_ellipse(output_frame,player_bbox['box'],color,track_id)  # Draw player track in red
            output_video_frames.append(output_frame)
        
        return output_video_frames