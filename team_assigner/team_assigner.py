# Load model directly
from transformers import CLIPProcessor, CLIPModel
import cv2 
from PIL import Image
import sys
sys.path.append("../")
from utils import read_stubs,save_stubs
class TeamAssigner:
    def __init__(self,team1_class_name="white_shirt",team2_class_name="dark_red_shirt"):
        self.team1_class_name = team1_class_name
        self.team2_class_name = team2_class_name
        self.player_team_dict={}
    def load_model(self):
        self.model = CLIPModel.from_pretrained("patrickjohncyh/fashion-clip")
        self.processor = CLIPProcessor.from_pretrained("patrickjohncyh/fashion-clip")
    
    def get_player_color(self,frame,bbox):
        #bbox-> [x1, y1, x2, y2]
        image=frame[int(bbox[1]):int(bbox[3]),int(bbox[0]):int(bbox[2])]
        
        #bgr to rgb image cause clip model,PIL expects rgb image in pytorch and bgr image in opencv
        rgb_image=cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        pil_image= Image.fromarray(rgb_image)
        classes=[self.team1_class_name,self.team2_class_name]
        inputs = self.processor(text=classes, images=pil_image, return_tensors="pt", padding=True)
        outputs = self.model(**inputs)
        logits_per_image = outputs.logits_per_image # this is the image-text similarity score
        probs = logits_per_image.softmax(dim=1) # we can take the softmax to get the label probabilities
        classname=classes[probs.argmax(dim=1)[0].item()]# return the index of the class with the highest probability
        return  classname
    
    def get_player_teams(self,frame,bbox,player_id):
        #
        if player_id in self.player_team_dict:
            return self.player_team_dict[player_id] 
        player_color=self.get_player_color(frame,bbox)
        team_id=2
        if  player_color==self.team1_class_name:
            team_id=1
        self.player_team_dict[player_id]=team_id
        return team_id
    
    def  get_player_teams_across_frames(self,video_frames,player_tracks,read_from_stub=False,stub_path=None):
        player_assignment=read_stubs(read_from_stub,stub_path)
        if player_assignment is not None:
            if len(player_assignment) == len(video_frames):
                return player_assignment
        self.load_model()
        player_assignment=[]
        for frame_num,player_track in enumerate(player_tracks):
            player_assignment.append({})  
            if frame_num%50==0:
                self.player_team_dict={}
            for player_id,track in player_track.items():
                team=self.get_player_teams(video_frames[frame_num],track['box'],player_id)
                player_assignment[frame_num][player_id]=team     
        save_stubs(stub_path,player_assignment)
        return player_assignment
