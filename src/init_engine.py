import os
import datetime
import platform
import cv2
import face_recognition
import geocoder
from geopy.geocoders import Nominatim


def find_encodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList


"""
OS Check for path to save video footage
"""
save_path = ""
if platform.system() == 'Linux':
    save_path = "/home/smv1999/Documents/Surveillance_System_Video_Footages/"
elif platform.system() == 'Windows':
    save_path = "V:\\Surveillance_System_Video_Footages\\"

path = '../images'
images = []
classNames = []
myList = os.listdir(path)


for cl in myList:
    cur_img = cv2.imread(f'{path}/{cl}')
    images.append(cur_img)
    classNames.append(os.path.splitext(cl)[0])


encodeListKnown = find_encodings(images)

cap = cv2.VideoCapture(0)

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
body_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_fullbody.xml")

frame_size = (1080, 720)

fourcc = cv2.VideoWriter_fourcc(*"mp4v")

current_time = datetime.datetime.now().strftime("%d-%m-%Y-%H-%M-%S")

record_path = f"{save_path}audio_{current_time}.mp3"

video_record_path = f"{save_path}video_{current_time}.mp4"

final_video_record_path = f"{save_path}{current_time}.mp4"

out = cv2.VideoWriter(
    video_record_path, fourcc, cv2.CAP_PROP_FPS, frame_size)


voice_file_path = save_path + "voice.mp3"

intro_file_path = "../music/intro.mp3"


geolocator = Nominatim(user_agent="geoapiExercises")

g = geocoder.ip('me')
coordinates = g.latlng
location_data = str(geolocator.geocode(
    str(coordinates[0])+","+str(coordinates[1])))
current_location = str(location_data.split(
    ',')[-4]) + str(location_data.split(',')[-3]) + str(location_data.split(',')[-1])
