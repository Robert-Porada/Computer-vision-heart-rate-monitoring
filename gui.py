import customtkinter
import tkinter
from tkinter import filedialog
from tkVideoPlayer import TkinterVideo

import main

def open_video():
    vid_player.stop()
    if video_file:
        try:
            vid_player.load(video_file)
            vid_player.play()
            play_pause_btn.configure(text="Pause ||")
        except:
            print("Unable to load the file")

def update_duration(event):
    try:
        duration = int(vid_player.video_info()["duration"])
    except:
        pass
    
def seek(value):
    if video_file:
        try:
            vid_player.seek(int(value))
            vid_player.play()
            vid_player.after(50,vid_player.pause)
            play_pause_btn.configure(text="Play ►")
        except:
            pass

    
def play_pause():
    if video_file:
        if vid_player.is_paused():
            vid_player.play()
            play_pause_btn.configure(text="Pause ||")

        else:
            vid_player.pause()
            play_pause_btn.configure(text="Play ►")


def video_ended(event):
    play_pause_btn.configure(text="Play ►")


def zmien_przyklad(choise):
    global wybrany_przyklad
    global autorski_czy_dolaczony
    autorski_czy_dolaczony = "przykładowe"
    label_plik.configure(text=f"Wybrano nagranie {autorski_czy_dolaczony}")
    wybrany_przyklad = choise


def zaktualizuj_wartosc_label_wzmocnienie(value):
    global wzmocnienie
    wzmocnienie = value
    label_wzmocnienie.configure(text=f"Wybrano wzmocnienie:{wzmocnienie}")


def analizuj_video():
    global wybrany_przyklad
    global video_input_path

    if autorski_czy_dolaczony == "przykładowe":
        sciezka = "GUI_input/" + wybrany_przyklad
        main.main_func(sciezka, wzmocnienie)
        open_video()
    elif autorski_czy_dolaczony == "własne":
        sciezka = video_input_path
        main.main_func(sciezka, wzmocnienie)
        open_video()


def wybierz_wlasny_przyklad():
    global video_input_path
    global autorski_czy_dolaczony
    GRAPH_PATH_new = tkinter.filedialog.askopenfilename(filetypes =[('video', ['*.mp4']), ('wszystkie pliki', ['*.*'])])
    video_input_path = GRAPH_PATH_new
    autorski_czy_dolaczony = "własne"
    label_plik.configure(text=f"Wybrano nagranie {autorski_czy_dolaczony}")



autorski_czy_dolaczony = "przykładowe"
video_input_path = ""
video_file = 'GUI_output/output.mp4'
przyklady = ["Przykład 1.MP4", "Przykład 2.MP4", "Przykład 3.MP4", "Przykład 4.MP4"]
wybrany_przyklad = "Przykład 1.MP4"
wzmocnienie = 0.4

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")


# ROOT
root = customtkinter.CTk()
root.geometry("1600x800")
root.title("ANALIZA TĘTNA")

# Główny frame 
frame = customtkinter.CTkFrame(master=root)
frame.pack(pady=20, padx=60, fill="both", expand=True)

# Lewy frame
frame_left = customtkinter.CTkFrame(master=frame)
frame_left.pack(pady=10, padx=10, fill="both", expand=False, side="left")

label1 = customtkinter.CTkLabel(master=frame_left, text="Pomiar tętna", font=("Helvetica", 40))
label1.pack(pady=12, padx=10)

label2 = customtkinter.CTkLabel(master=frame_left, text="Wybierz nagranie z dysku:", font=("Helvetica", 30))
label2.pack(pady=5, padx=10)

button_model_autorski = customtkinter.CTkButton(master=frame_left, text="WYBIERZ", command=wybierz_wlasny_przyklad)
button_model_autorski.pack(pady=12, padx=10)


label_plik = customtkinter.CTkLabel(master=frame_left, text=f"Wybrano nagranie {autorski_czy_dolaczony}", font=("Helvetica", 20))
label_plik.pack(pady=10, padx=10)

label_wybierz_przyklad = customtkinter.CTkLabel(master=frame_left, text="Wybierz przykład", font=("Helvetica", 30))
label_wybierz_przyklad.pack(pady=10, padx=10)

dropdown_menu_przyklad = customtkinter.CTkComboBox(master=frame_left, values=przyklady, command=zmien_przyklad)
dropdown_menu_przyklad.pack()


# wybierz wzmocnienie
label_wybierz_wzmocnienie = customtkinter.CTkLabel(master=frame_left, text="Wybierz wzmocnienie [0, 1]", font=("Helvetica", 30))
label_wybierz_wzmocnienie.pack(pady=10, padx=10)


slider = customtkinter.CTkSlider(master=frame_left, from_=0, to=1, command=zaktualizuj_wartosc_label_wzmocnienie)
slider.pack(pady=10, padx=10)


label_wzmocnienie = customtkinter.CTkLabel(master=frame_left, text=f"Wybrano wzmocnienie:{wzmocnienie}", font=("Helvetica", 20))
label_wzmocnienie.pack(pady=10, padx=10)


# Guzik Analizuj video
button_analizuj = customtkinter.CTkButton(master=frame_left, text="ANALIZUJ", command=analizuj_video)
button_analizuj.pack(pady=20, padx=10)


# Prawy frame
frame_right = customtkinter.CTkFrame(master=frame)
frame_right.pack(pady=10, padx=10, fill="both", expand=True, side="right")

label_prawo = customtkinter.CTkLabel(master=frame_right, text="Video:", font=("Helvetica", 30))
label_prawo.pack(pady=10, padx=30)

vid_player = TkinterVideo(master=frame_right, scaled=True, keep_aspect=True, consistant_frame_rate=True, bg="black")
vid_player.set_resampling_method(1)
vid_player.pack(expand=True, fill="both", padx=10, pady=10)
vid_player.bind("<<Duration>>", update_duration)
vid_player.bind("<<Ended>>", video_ended)

play_pause_btn = customtkinter.CTkButton(master=frame_right, text="Play ►", command=play_pause)
play_pause_btn.pack(pady=10)


root.mainloop()