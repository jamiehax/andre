import cv2
from deepface import DeepFace
import requests
import shutil


# take picture using webcam
def take_picture():
    cam = cv2.VideoCapture(0)
    cv2.namedWindow("take your picture")

    while True:
        ret, frame = cam.read()

        if not ret:
            print("failed to grab frame")
            break

        cv2.imshow("take your picture", frame)

        k = cv2.waitKey(1)
        # if they hit escape, close window
        if k % 256 == 27:
            break

        # if they hit space, take picture and save
        elif k % 256 == 32:
            img_name = "a1/face.png"
            cv2.imwrite(img_name, frame)
            break

    cam.release()
    cv2.destroyAllWindows()


# analyze facial attributes
def analyze_picture(path):
    att = DeepFace.analyze(img_path=path, actions=[
                           'age', 'gender', 'race', 'emotion'])
    return att


# create descriptive string based on image attributes
def describe(att):
    emotion = att['dominant_emotion']
    gender = att['dominant_gender']
    race = att['dominant_race']
    age = att['age']
    description = emotion+" "+str(age)+" year old "+race+" "+gender
    return description


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
    filename = "a1/" + url.split("/")[-1]
    im = requests.get(url, stream=True)

    if im.status_code == 200:
        im.raw.decode_content = True
        with open(filename, 'wb') as f:
            shutil.copyfileobj(im.raw, f)
        print('sucessfully downloaded: ', filename)
    else:
        print('Image couldn\'t be retreived')


def display_image(path):
    img = cv2.imread(path)
    cv2.imshow('you', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


# loop to run program
while True:
    take_picture()
    print("analyzing picture")
    att = analyze_picture("a1/face.png")
    description = describe(att)
    print("generating image of "+description)
    get_image(description)
    display_image("a1/output.jpg")
