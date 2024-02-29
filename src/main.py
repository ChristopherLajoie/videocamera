from camera import VideoCamera
import cv2
from multiprocessing import Process, Queue
from app import create_app

def check_camera(index, queue):
    try:
        cap = cv2.VideoCapture(index)
        if cap.isOpened():
            queue.put(index)
            cap.release()
    except Exception as e:
        print(f"Error checking camera index {index}: {e}")

def get_camera_indices():
    indices = []
    max_index_to_check = 5  

    processes = []
    queues = []

    try:
        for i in range(max_index_to_check):
            queue = Queue()
            p = Process(target=check_camera, args=(i, queue))
            p.start()
            processes.append(p)
            queues.append(queue)

        for p, queue in zip(processes, queues):
            p.join(timeout=15)  # adjust the timeout as needed
            if p.is_alive():
                p.terminate()
            else:
                while not queue.empty():
                    indices.append(queue.get())
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        for p in processes:
            if p.is_alive():
                p.terminate()
            p.join()

    return indices 

indices = get_camera_indices()
cameras = [VideoCamera(source_index) for source_index in indices]

app = create_app(cameras)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)
