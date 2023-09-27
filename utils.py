import platform
import os
import uuid
from pynput.mouse import Controller

def take_picture():
    my_uuid = str(uuid.uuid4())
    file_path = f"/tmp/intruder_{my_uuid}.jpg"
    os.system(f"imagesnap {file_path}")
    return file_path

def sleepnow():
    if platform.system() == 'Darwin':
        os.system("pmset displaysleepnow")
        image_path = take_picture()
        return image_path
    else:
        return None

# def dont_move():
#     mouse = Controller()
#     init_x ,init_y = mouse.position
#     while True:
#         current_x, current_y = mouse.position
#         if current_x != init_x or current_y != init_y:
#             return 1
