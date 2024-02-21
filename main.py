import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import math

import DFT
import progress_bar
import face_detection_yolo


VIDEO_PATH = 'Filmy_ruch/3/cold.mp4'


def main_func(VIDEO_PATH, wzmocnienie):

    START_FREQ = 1
    STOP_FREQ = 4
    DIM = (1280, 720)
    WINDOW_SIZE = 10
    WINDOW_STRIDE = 1

    amplifier = wzmocnienie


    video_list, face_list, fps, frame_count = face_detection_yolo.read_and_detect_face(VIDEO_PATH)

    video_duration = frame_count/fps
    number_of_sets = max((math.ceil((math.ceil(video_duration) - WINDOW_SIZE) / WINDOW_STRIDE) + 1), 1)
    window_instance_video_list = []
    window_instance_face_list = []

    for k in range(number_of_sets):
        if (k * WINDOW_STRIDE + WINDOW_SIZE) * fps < len(video_list):
            video_list_window = video_list[k * fps * WINDOW_STRIDE : (k * WINDOW_STRIDE + WINDOW_SIZE) * fps]
            face_list_window = face_list[k * fps * WINDOW_STRIDE : (k * WINDOW_STRIDE + WINDOW_SIZE) * fps]
        else:
            video_list_window = video_list[k * WINDOW_STRIDE * fps :]
            face_list_window = face_list[k * WINDOW_STRIDE * fps :]
        window_instance_video_list.append(video_list_window)
        window_instance_face_list.append(face_list_window)

    # print(video_duration)
    # print(number_of_sets)
    # 
    # for inx, item in enumerate(window_instance_face_list):
    #     print(item)


    merged = []

    for k in range(number_of_sets):

        video_list = window_instance_video_list[k]
        face_list = window_instance_face_list[k]

        blue_channel = []
        green_channel = []
        red_channel = []

        blue_channel_mean = []
        green_channel_mean = []
        red_channel_mean = []


        # Liczenie średniej w wykrytym obszarze i podział na kanały
        for index, frane in enumerate(video_list):
            x, y, w, h =  face_list[index]

            b, g, r = cv.split(frane)
            blue_channel.append(b)
            green_channel.append(g)
            red_channel.append(r)

            cropped = video_list[index][y : y + h, x : x + w]
            b, g, r = cv.split(cropped)

            blue_channel_mean.append(np.mean(b))
            green_channel_mean.append(np.mean(g))
            red_channel_mean.append(np.mean(r))


        blue_channel_mean_substr = DFT.substract_mean(blue_channel_mean)
        green_channel_mean_substr = DFT.substract_mean(green_channel_mean)
        red_channel_mean_substr = DFT.substract_mean(red_channel_mean)

        # DFT.display_channels(blue_channel_mean_substr, green_channel_mean_substr, red_channel_mean_substr, frame_count)


        dft_blue = DFT.dft(blue_channel_mean_substr)
        dft_green = DFT.dft(green_channel_mean_substr)
        dft_red = DFT.dft(red_channel_mean_substr)

        # DFT.display_dft(dft_blue, dft_green, dft_red, fps)

        idft_blue, blue_freq = DFT.idft_max(dft_blue, fps, START_FREQ, STOP_FREQ)
        idft_green, green_freq = DFT.idft_max(dft_green, fps, START_FREQ, STOP_FREQ)
        idft_red, red_freq = DFT.idft_max(dft_red, fps, START_FREQ, STOP_FREQ)


        # DFT.display_idft(idft_blue, idft_green, idft_red)

        blue_BPM   = round(blue_freq * 60)
        green_BPM  = round(green_freq * 60)
        red_BPM    = round(red_freq * 60)
        tetno_wiadomosc = f"B, G, R: {blue_BPM}, {green_BPM}, {red_BPM} [BPM]"



        fourcc = cv.VideoWriter_fourcc(*'mp4v')
        out = cv.VideoWriter('GUI_output/output.mp4', fourcc, fps, DIM)


        for i in range(len(blue_channel)):

            blue_channel[i][y : h, x : w] = cv.scaleAdd(blue_channel[i][y : h, x : w], amplifier * idft_blue[i], blue_channel[i][y : h, x : w])
            green_channel[i][y : h, x : w] = cv.scaleAdd(green_channel[i][y : h, x : w], amplifier* idft_green[i], green_channel[i][y : h, x : w])
            red_channel[i][y : h, x : w] = cv.scaleAdd(red_channel[i][y : h, x : w], amplifier * idft_red[i], red_channel[i][y : h, x : w])


            color_image = cv.merge([blue_channel[i], green_channel[i], red_channel[i]])

            x, y, w, h =  face_list[i]
            cv.rectangle(color_image, (x, y), (w,h), (0, 255, 0), 2)
            cv.rectangle(color_image, (x, y-20), (w, y), (0, 255, 0), -1)

            cv.putText(img=color_image,
                text=tetno_wiadomosc, 
                org=(x, y - 4),
                fontFace=cv.FONT_HERSHEY_TRIPLEX,
                fontScale=0.6, 
                color=(0,0,0), 
                thickness=1)

            if i <= fps * WINDOW_STRIDE or k == number_of_sets - 1:
                merged.append(color_image)


    for i in range(len(merged)):
        out.write(merged[i])
    
        # cv.imshow('Video', merged[i])
        # if cv.waitKey(20) & 0xFF==ord('d'):
        #     break

    out.release()
    cv.destroyAllWindows()

if __name__ == "__main__":
    main_func(VIDEO_PATH)
