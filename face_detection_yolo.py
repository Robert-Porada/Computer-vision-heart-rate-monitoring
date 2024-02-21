import cv2 as cv
import matplotlib.pyplot as plt
from ultralytics import YOLO

import progress_bar


def read_and_detect_face(VIDEO_PATH):

    video_list = []
    face_list = []

    print(f"\n\nOdczytywanie pliku: {VIDEO_PATH}\n")

    capture = cv.VideoCapture(VIDEO_PATH)

    fps = round(capture.get(cv.CAP_PROP_FPS))
    frame_count = int(capture.get(cv.CAP_PROP_FRAME_COUNT))

    bar = progress_bar.progress_bar(frame_count)

    success, img = capture.read()
    count = 0

    model = YOLO("best.pt")
    
    while success:
        
        # resize image
        resized = cv.resize(img, (1280, 720), interpolation = cv.INTER_AREA)

        face_pre = model.predict(
            source=resized,
            imgsz=(224, 352),
            max_det=1,
            verbose=False
            )

        success, img = capture.read()

        boxes = face_pre[0].boxes

        # Gdy nie wykryto twarzy, użyj poprzedniej lokalizacji 
        if boxes.xyxy.tolist():
            face = boxes

        if 'face' not in locals():
            face = [[0,0,1,1]]

        x = int(face.xyxy.tolist()[0][0])
        y = int(face.xyxy.tolist()[0][1])
        w = int(face.xyxy.tolist()[0][2])
        h = int(face.xyxy.tolist()[0][3])

        face_list.append([x, y, w, h])
        video_list.append(resized)

        count += 1
        bar.update(count)

    capture.release()


    return video_list, face_list, fps, frame_count