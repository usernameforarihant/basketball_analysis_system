import cv2
class PassAndInterceptionDrawer:
    def __init__(self):
        pass

    def draw(self,video_frames,passes,interceptions):
        output_video_frames = []

        for frame_num , frame in enumerate(video_frames):
            # Draw passes
            frame_drawn=self.draw_frame(frame,frame_num,passes,interceptions)
            output_video_frames.append(frame_drawn)
        return output_video_frames
    
    def get_stats(self,passes,interceptions):
        team_1_passes=[]
        team_2_passes=[]
        team_1_interceptions=[]
        team_2_interceptions=[]

        for frame_num in range(len(passes)):
            if passes[frame_num]==1:
                team_1_passes.append(frame_num)
            elif passes[frame_num]==2:
                team_2_passes.append(frame_num)
            if interceptions[frame_num]==1:
                team_1_interceptions.append(frame_num)
            elif interceptions[frame_num]==2:
                team_2_interceptions.append(frame_num)
        return len(team_1_passes), len(team_2_passes), len(team_1_interceptions), len(team_2_interceptions)
    
        
    def draw_frame(self,frame,frame_num,passes,interceptions):
        """
        Draw a semi-transparent overlay of team ball control percentages on a single frame.

        Args:
            frame (numpy.ndarray): The current video frame on which the overlay will be drawn.
            frame_num (int): The index of the current frame.
            team_ball_control (numpy.ndarray): An array indicating which team has ball control for each frame.

        Returns:
            numpy.ndarray: The frame with the semi-transparent overlay and statistics.
        """
        
        # Draw a semi-transparent rectaggle 
        overlay = frame.copy()
        font_scale = 0.7
        font_thickness=2
        
        # Overlay Position
        frame_height, frame_width = overlay.shape[:2]
        rect_x1 = int(frame_width * 0.16) 
        rect_y1 = int(frame_height * 0.75)
        rect_x2 = int(frame_width * 0.55)  
        rect_y2 = int(frame_height * 0.90)
        # Text positions
        text_x = int(frame_width * 0.19 )  
        text_y1 = int(frame_height * 0.80)  
        text_y2 = int(frame_height * 0.88)


        cv2.rectangle(overlay, (rect_x1, rect_y1), (rect_x2, rect_y2), (255,255,255), -1 )
        alpha = 0.8
        cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)

        passes_till_frame=passes[:frame_num+1]
        interceptions_till_frame=interceptions[:frame_num+1]

        team_1_passes,team_2_passes,team_1_interceptions,team_2_interceptions=self.get_stats(passes_till_frame,interceptions_till_frame)

        cv2.putText(frame, f"Team 1 - Passes: {team_1_passes} |Interceptions: {team_1_interceptions}",(text_x, text_y1), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (0,0,0), font_thickness)
        cv2.putText(frame, f"Team 2 - Passes: {team_2_passes} |Interceptions: {team_2_interceptions}",(text_x, text_y2), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (0,0,0), font_thickness)

        return frame