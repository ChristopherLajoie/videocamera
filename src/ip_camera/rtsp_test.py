import cv2
import subprocess

rtmp_url = "rtmp://192.168.226.1/live/test"

camera = cv2.VideoCapture("/dev/video0")
status, frame = camera.read()

#gather video info to ffmpeg
fps = int(15) 
height = frame.shape[0] 
width = frame.shape[1]

#command and params for ffmpeg
command = ['ffmpeg', '-y', '-f', 'rawvideo', '-vcodec', 'rawvideo', '-pix_fmt', 'bgr24', '-s', "{}x{}".format(width, height), '-r', str(fps), '-vsync', '2', '-i', '-', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-preset', 'ultrafast', '-f', 'flv', rtmp_url]

#using subprocess and pipe to fetch frame data
p = subprocess.Popen(command, stdin=subprocess.PIPE)

while 1:
    status, frame = camera.read()
    ## DO STUFF ##
    # write to pipe
    p.stdin.write(frame.tobytes())