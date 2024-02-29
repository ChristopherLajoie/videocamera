import json
from flask import Flask, render_template, Response, jsonify, request
import cv2
import time

app = Flask(__name__)

@app.route('/turn_off_feed/<int:index>', methods=['POST'])
def turn_off_feed(index):
    cameras = app.config['cameras']
    
    for camera in cameras:
        if camera.source_index == index:
          
            camera.stop_feed()
            return jsonify({'status': 'success'})
    return jsonify({'status': 'error'}), 404  

@app.route('/')
def index():
    cameras = app.config['cameras']
    resolution = cameras[0].get_resolution() if cameras else (0, 0)
    return render_template('index.html', num_feeds=len(cameras), cameras=cameras, resolution=resolution)

@app.route('/change_resolution', methods=['GET'])
def change_resolution():
    cameras = app.config['cameras']
    selected_camera_id = int(request.args.get('camera'))  # Get the selected camera ID
    selected_resolution = request.args.get('resolution')  # Get the selected resolution

    # Convert the resolution to an integer
    resolution = int(selected_resolution)

    for camera in cameras:
        if camera.source_index == selected_camera_id:
            camera.set_resolution(resolution)
            break
    else:
        return jsonify({'error': 'Selected camera not found'}), 404

    return '', 204

@app.route('/refresh_feed/<int:index>', methods=['POST'])
def refresh_feed(index):
    cameras = app.config['cameras']
    
    for camera in cameras:
        if camera.source_index == index:
            
            camera.refresh()
            break

    return '', 204  

def gen(camera):
    total_bytes = 0
    start_time = time.time()

    while True:
        frame = camera.get_frame()
        frame_size = len(frame)
        total_bytes += frame_size

        elapsed_time = time.time() - start_time
        if elapsed_time >= 5:  
            mbps = total_bytes / elapsed_time / 1048576  
            print(f"Data rate for camera {camera.source_index}: {mbps:.2f} MB/s")
            total_bytes = 0
            start_time = time.time()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def create_route(camera):
    def video_feed():
        return Response(gen(camera),
                        mimetype='multipart/x-mixed-replace; boundary=frame')
    return video_feed

def create_app(cameras):
    app.config['cameras'] = cameras
    for camera in cameras:
        app.add_url_rule(f'/video_feed/{camera.source_index}', f'video_feed_{camera.source_index}', create_route(camera))
    return app