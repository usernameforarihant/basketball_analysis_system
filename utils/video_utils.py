import cv2
import os
def read_video(video_path):
    """
    Reads a video file and returns a list of frames.
    
    Args:
        video_path (str): Path to the video file.
        
    Returns:
        list: List of frames in the video.
    """
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Video file {video_path} not found.")
    
    cap = cv2.VideoCapture(video_path)
    frames = []
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frames.append(frame)
    
    cap.release()
    return frames

def save_video(output_video_frames, output_path, fps=30):
    if not os.path.exists(output_path):
        os.makedirs(os.path.dirname(output_path),exist_ok=True)
    
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out=cv2.VideoWriter(output_path,fourcc,24.0,(output_video_frames[0].shape[1],output_video_frames[0].shape[0]))  #24 frames per sec , (w,h)
    for frame in output_video_frames:
        out.write(frame)
    out.release()