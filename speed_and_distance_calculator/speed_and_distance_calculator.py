from utils.bbox_utils import measure_distance
class SpeedDistanceCalculator:
    def __init__(self,width_in_pixels,height_in_pixels,width_in_meters,height_in_meters):
        self.width_in_pixels=width_in_pixels
        self.height_in_pixels=height_in_pixels
        self.width_in_meters=width_in_meters
        self.height_in_meters=height_in_meters

    def calculate_distance_meters(self,prev_pixel_position,current_pixel_position):
        prev_pixel_x,prev_pixel_y=prev_pixel_position
        current_pixel_x,current_pixel_y=current_pixel_position

        prev_meter_x=prev_pixel_x*self.width_in_meters/self.width_in_pixels
        prev_meter_y=prev_pixel_y*self.height_in_meters/self.height_in_pixels

        current_meter_x=current_pixel_x*self.width_in_meters/self.width_in_pixels
        current_meter_y=current_pixel_y*self.height_in_meters/self.height_in_pixels
         
        meter_distance=measure_distance((prev_meter_x,prev_meter_y),(current_meter_x,current_meter_y))
        meter_distance=meter_distance*0.4 #penalising
        return meter_distance




    def calculate_distance(self,tactical_player_positions):
        output_distances=[]
        prev_players_positions={}
        for frame_num,tactical_player_position_frame in enumerate(tactical_player_positions):
            output_distances.append({})
            for player_id,current_player_position in tactical_player_position_frame.items():
                if player_id in prev_players_positions:
                    prev_players_position=prev_players_positions[player_id]
                    distance=self. calculate_distance_meters(current_player_position,prev_players_position) #in pixels
                    output_distances[frame_num][player_id]=(distance)
                prev_players_positions[player_id]=current_player_position

        return output_distances
    
    def calculate_speed(self,distances,fps=30):
        speeds=[]
        window_size=5
        for frame_idx in range(len(distances)):
            speeds.append({})
            for player_id in distances[frame_idx].keys():
                start_frame=max(0,frame_idx-(window_size*3))
                total_distance=0
                frame_present=0
                last_frame_present=None
                for i in range(start_frame,frame_idx+1):
                    if player_id in distances[i]:
                        if last_frame_present is not None:
                            total_distance+=distances[i][player_id]
                            frame_present+=1
                        last_frame_present=i
                if frame_present>window_size:
                    times_in_seconds=frame_present/fps
                    time_in_hours=times_in_seconds/3600
                    if time_in_hours>0:
                        speed_kmh=(total_distance/1000)/time_in_hours
                        speeds[frame_idx][player_id]=speed_kmh
                    else:
                        speeds[frame_idx][player_id]=0
                else:
                    speeds[frame_idx][player_id]=0
        return speeds