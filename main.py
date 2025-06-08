from utils import save_video,read_video
from trackers import PlayerTracker
from drawers import PlayerTracksDrawer,TeamBallDrawer
from drawers import BallTracksDrawer,PassAndInterceptionDrawer,CourtKeypointsDrawer,TacticalViewDrawer,SpeedDistanceDrawer
from trackers import BallTracker
from team_assigner import TeamAssigner
from ball_acquisition import BallAcquisitionDetector
from pass_and_interception import PassAndInterceptionDetector
from court_keypoint_detector import CourtKeypointDetector
from tactical_view_converter import TacticalViewConverter
from speed_and_distance_calculator import SpeedDistanceCalculator
from config import (
    STUBS_DEFAULT_PATH,
    PLAYER_DETECTOR_PATH,
    BALL_DETECTOR_PATH,
    COURT_KEYPOINT_DETECTOR_PATH,
    OUTPUT_VIDEO_PATH
)
import argparse
import os

def parse_args():
    parser = argparse.ArgumentParser(description='Basketball Video Analysis')
    parser.add_argument('input_video', type=str, help='Path to input video file')
    parser.add_argument('--output_video', type=str, default=OUTPUT_VIDEO_PATH, 
                        help='Path to output video file')
    parser.add_argument('--stub_path', type=str, default=STUBS_DEFAULT_PATH,
                        help='Path to stub directory')
    return parser.parse_args()

def main():
    args=parse_args()


    #read frames
    video_frames=read_video(args.input_video)

    #initialise tracker
    player_tracker=PlayerTracker(PLAYER_DETECTOR_PATH)
    ball_tracker=BallTracker(BALL_DETECTOR_PATH)
    team_ball_drawer=TeamBallDrawer()

    #initialise court keypoint detector
    court_keypoint_detector=CourtKeypointDetector(COURT_KEYPOINT_DETECTOR_PATH)
    #run tracker 
    player_tracks=player_tracker.get_object_tracks(video_frames,read_from_stubs=True,stub_path=os.path.join(args.stub_path, 'player_track_stubs.pkl'))
    #ball tracker
    ball_tracks=ball_tracker.get_object_tracks(video_frames,read_from_stubs=True,stub_path=os.path.join(args.stub_path, 'ball_track_stubs.pkl') )

    #get court keypoints
    court_keypoints=court_keypoint_detector.get_court_keypoints(video_frames,read_from_stub=True,stub_path=os.path.join(args.stub_path, 'court_key_points_stub.pkl'))
    # print(court_keypoints)
    #draw output
    #intialize drawer
    player_tracks_drawer=PlayerTracksDrawer()
    ball_tracks_drawer=BallTracksDrawer()
    pass_and_interception_drawer = PassAndInterceptionDrawer()
    court_keypoint_drawer=CourtKeypointsDrawer()
    tactical_view_drawer=TacticalViewDrawer()
    speed_and_distance_drawer=SpeedDistanceDrawer()

    #remove wrong detections
    ball_tracks= ball_tracker.remove_wrong_detections(ball_tracks)
    #interpolate missing ball positions
    ball_tracks = ball_tracker.interpolate_ball_positions(ball_tracks)
    #Assign teams to players
    team_assigner = TeamAssigner()
    player_assignment     = team_assigner.get_player_teams_across_frames(video_frames, player_tracks, read_from_stub=True, stub_path="stubs/player_assignment_stub.pkl")
    
    #ballacquisition detector 
    ball_acquisition_detector = BallAcquisitionDetector()
    ball_acquisition=ball_acquisition_detector.detect_ball_possession(player_tracks,ball_tracks)
    # print(ball_acquisition)
    
    #pass and interception detector
    pass_and_interception_detector = PassAndInterceptionDetector()
    passes = pass_and_interception_detector.detect_pass(ball_acquisition, player_assignment)
    interceptions = pass_and_interception_detector.detect_interceptions(ball_acquisition, player_assignment) 

    
    
    # print("Passes:", passes)
    # print("===========================================================")
    # print("Interceptions:", interceptions)

    #Tactical View 
    tactical_view_coverter=TacticalViewConverter(court_image_path="./images/basketball_court.png")
    court_keypoints=tactical_view_coverter.validate_keypoints(court_keypoints)
    tactical_player_positions=tactical_view_coverter.transform_players_to_tactical_view(court_keypoints,player_tracks)

    #Speed and distance calulator
    speed_and_distance_calculator= SpeedDistanceCalculator(tactical_view_coverter.width,tactical_view_coverter.height,tactical_view_coverter.actual_width_in_meters,tactical_view_coverter.actual_height_in_meters)
    player_distance_per_frame=speed_and_distance_calculator.calculate_distance(tactical_player_positions)
    player_speed_per_frame=speed_and_distance_calculator.calculate_speed(player_distance_per_frame)
    
    # print(player_distance_per_frame)
    # print("===============================")
    # print(player_speed_per_frame)
    
    #draw tracks
    output_video_frames = player_tracks_drawer.draw(video_frames, player_tracks,player_assignment,ball_acquisition)
    output_video_frames = ball_tracks_drawer.draw(output_video_frames, ball_tracks)
    output_video_frames = pass_and_interception_drawer.draw(output_video_frames, passes, interceptions)

    #draw team ball control
    output_video_frames = team_ball_drawer.draw(output_video_frames, player_assignment, ball_acquisition)

    #draw court_keypoint
    output_video_frames =court_keypoint_drawer.draw(output_video_frames,court_keypoints)

    #Tactical View drawer
    output_video_frames=tactical_view_drawer.draw(output_video_frames,tactical_view_coverter.court_image_path,tactical_view_coverter.width,tactical_view_coverter.height,tactical_view_coverter.key_points,tactical_player_positions,player_assignment,ball_acquisition)
    
    #Speed and Distance Drawer
    output_video_frames=speed_and_distance_drawer.draw(output_video_frames,player_tracks,player_distance_per_frame,player_speed_per_frame)


    if not output_video_frames or output_video_frames[0] is None:
        print("Error: No output video frames generated.")
        return  
    #save video
    save_video(output_video_frames,args.output_video)

if __name__=='__main__':
    main()
