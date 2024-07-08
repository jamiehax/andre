from deepface import DeepFace
import threading
import tkinter as tk
import requests
import shutil
# import sys
import cv2
from PIL import Image
import os

"""

fortnite

"""

# dict to store emotion data
em_data = {'Anger': 0, 'Disgust': 0, 'Fear': 0,
           'Happy': 0, 'Sad': 0, 'Surprise': 0, 'Neutral': 0}

# dict with emotion color codes
em_col = {'Neutral': '#ffffff',
          'Anger': '#ff0000',
          'Disgust': '#48ff00',
          'Fear': '#ae00ff',
          'Happy': '#ffe400',
          'Sad': '#2a00ff',
          'Surprise': '#ff8400'}

current_emotion = None

# display dimensions (pixels)
height = 1600
width = 2560

# set up window
root = tk.Tk()
root.title('How are you feeling?')
root.geometry(str(height)+'x'+str(width))
root.configure(background='black')
canva = tk.Canvas(root, bg=em_col['Neutral'], height=height, width=width)


# generate and download image from DeepAI's text-to-image api
api_key = ''
def get_image(text):
    r = requests.post(
        "https://api.deepai.org/api/text2img",
        data={
            'text': text,
        },
        headers={'api-key': api_key}
    )
    url = r.json().get('output_url')
    filename = "./a2/art/generated/" + url.split("/")[-1]
    im = requests.get(url, stream=True)

    if im.status_code == 200:
        im.raw.decode_content = True
        with open(filename, 'wb') as f:
            shutil.copyfileobj(im.raw, f)
        print('Image sucessfully Downloaded: ', filename)
    else:
        print('Image couldn\'t be retreived')


# display window
def display_window():
    canva.pack()
    root.mainloop()


# change the windows color
def change_canvas_color(emotion):
    canva.configure(bg=em_col[emotion])


# check data from video
def stream_data():
    while True:
        global current_emotion
        vid_emotion = max(em_data, key=em_data.get)
        if vid_emotion != current_emotion:
            change_canvas_color(vid_emotion)
            print("emotion detected: "+vid_emotion)
            get_image(vid_emotion)
            # os.system('python3 art/generated/img_disp.py')
            current_emotion = vid_emotion


# DeepFace analysis
def face_analysis():
    DeepFace.stream(em_data)


threading.Thread(target=face_analysis).start()
threading.Thread(target=stream_data).start()
display_window()
