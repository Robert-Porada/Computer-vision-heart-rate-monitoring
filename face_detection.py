import cv2 as cv
import matplotlib.pyplot as plt
import math

import progress_bar
import main


VIDEO_PATH = 'Filmy_ruch/3/cold_Trim.mp4'
# VIDEO_PATH = 'Filmy_ruch/4/cold.mp4'

def read_and_detect_face(VIDEO_PATH):

    DIM = (1280, 720)
    video_list = []
    face_list = []

    print(f"\n\nOdczytywanie pliku: {VIDEO_PATH}\n")

    capture = cv.VideoCapture(VIDEO_PATH)
    fps = round(capture.get(cv.CAP_PROP_FPS))
    frame_count = int(capture.get(cv.CAP_PROP_FRAME_COUNT))

    bar = progress_bar.progress_bar(frame_count)
    # gui.zaktualizuj_wiadomosc_konsoli(bar)

    success, img = capture.read()
    count = 0


    face_classifier = cv.CascadeClassifier(
        cv.data.haarcascades + "haarcascade_frontalface_default.xml"
    )

    

    while success:
        
        # resize image
        resized = cv.resize(img, DIM, interpolation = cv.INTER_AREA)

        gray_image = cv.cvtColor(resized, cv.COLOR_BGR2GRAY)

        success, img = capture.read()
        

        face_pre = face_classifier.detectMultiScale(
        gray_image, scaleFactor=1.1, minNeighbors=5, minSize=(100, 100), flags=0
        )

        # Gdy nie wykryto twarzy, użyj poprzedniej lokalizacji 
        if len(face_pre) != 0:
            face = face_pre

        if 'face' not in locals():
            face = [[0,0,1,1]]

        # for (x, y, w, h) in face:
        #     cv.rectangle(resized, (x, y), (x + w, y + h), (0, 255, 0),  4)
        video_list.append(resized)
        face_list.append(face)

        count += 1
        bar.update(count)

    capture.release()


    return video_list, face_list, fps, frame_count
