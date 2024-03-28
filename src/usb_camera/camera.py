import cv2
import numpy as np
import time

# TODOS
# - Fix blackout data consumption
# - Simplify zoom functionality
# - Resolve `get_camera` bug
# - Implement FPS support

class VideoCamera(object):
    def __init__(self, source):
        print(f"Initializing camera with index {source}")
        self.source = source
        self.error_flag = False
        self.video = cv2.VideoCapture(source) 

        width = int(self.video.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(self.video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.aspect_ratio = width / height

        self.resolution = (width, height)
        self.source_index = source
        
        if not self.video.isOpened():
            print(f"Error: Unable to open camera with index {source}")
    
    def __del__(self):
        self.video.release()

    def stop_feed(self):
        self.video.release()
    
    def set_resolution(self, new_resolution):
        width = int(new_resolution * self.aspect_ratio)
        self.resolution = (width, new_resolution)
    
    def refresh(self):
        self.video.release()
        time.sleep(1)
        self.video = cv2.VideoCapture(self.source)
        if not self.video.isOpened():
            print(f"Error: Unable to open camera with index {self.source}")
    
    def get_placeholder_frame(self):
        return cv2.imencode('.jpg', np.zeros((self.resolution[1], self.resolution[0], 3), dtype=np.uint8))[1].tobytes()
    
    def get_resolution(self):
        return self.video.get(cv2.CAP_PROP_FRAME_WIDTH), self.video.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def get_frame(self):

        success, image = self.video.read()

        if not success or image is None:
            if not self.error_flag:           
                print(f"Error capturing frame from camera {self.source_index}")
                self.error_flag = True

            return self.get_placeholder_frame()  


        image = cv2.resize(image, self.resolution)
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()


