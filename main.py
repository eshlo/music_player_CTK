import shutil
import time
from customtkinter import *
import pygame
import music_tag
from CTkListbox import *
from PIL import Image
from tkinter.messagebox import showerror, showinfo, showwarning
from tkinter.filedialog import askopenfilename

window = CTk()
window.title("Eshlo Music Player")
window.geometry("1100x600")
window.resizable(0, 0)
pygame.mixer.init()


#### funcs
def volume_set(volume):
    value = v_slider_state_var.get()
    if volume.delta == 120:
        v_slider_state_var.set(value + 0.1)
        pygame.mixer.music.set_volume(value + 0.1)
    elif volume.delta == -120:
        v_slider_state_var.set(value - 0.1)
        pygame.mixer.music.set_volume(value - 0.1)


window.bind("<MouseWheel>", func=volume_set)


def ap_mode():
    if state_var.get() == "dark":
        set_appearance_mode("dark")
    else:
        set_appearance_mode("light")


def show_play_list():
    playlist.delete(0, "end")
    music_list = os.listdir("assets/play_list")
    for music in music_list:
        playlist.insert("end", music)


def add_play_list():
    try:
        music_path = askopenfilename(title="Select Music", filetypes=[("Music File", "*.mp3")])
        shutil.copy(music_path, "assets/play_list")
        show_play_list()
    except:
        showerror("Error!", "Select a Music!")


def remove_play_list():
    try:
        index = playlist.curselection()
        music_name = playlist.get(index)
        os.remove(f"assets/play_list/{music_name}")
        show_play_list()
    except FileNotFoundError:
        showerror("Not Selected", "Select a music for romove from playlist")


endtime_state_var = IntVar(value=0)
corent_state_var = IntVar(value=0)


def curent_time():
    curent = corent_state_var.get() + int((pygame.mixer_music.get_pos() + 1) / 1000)
    state_var_time.set(curent)
    convert_curent = time.strftime("%M:%S", time.gmtime(curent))
    time_lapse.configure(text=str(convert_curent))
    index = playlist.curselection()
    if curent + 1 == endtime_state_var.get():
        stop_music()
        try:
            playlist.activate(index + 1)
            play_pause()
            corent_state_var.set(0)
            textvariable.set(1)
        except IndexError:
            playlist.activate(0)
            play_pause()
            corent_state_var.set(0)
            textvariable.set(1)

    time_lapse.after(1000, curent_time)


def music_len():
    index = playlist.curselection()
    music_name = playlist.get(index)
    mp3 = music_tag.load_file(f"assets/play_list/{music_name}")
    len_mp3 = int(mp3["#length"])
    endtime_state_var.set(value=len_mp3)
    time_slider.configure(to=len_mp3)
    convert_mp3 = time.strftime("%M:%S", time.gmtime(len_mp3))
    music_time.configure(text=convert_mp3)


def play_pause():
    try:
        if textvariable.get() == 1:
            textvariable.set(value=2)
            play_puase_btn.configure(image=pause_image)
            index = playlist.curselection()
            music_name = playlist.get(index)
            musicname = music_name.replace(".mp3", "")
            musicname = musicname.replace("-", " ")
            music_name_lable.configure(text=musicname.replace("_", " "), font=CTkFont(size=24))
            pygame.mixer.music.load(f"assets/play_list/{music_name}")
            curent_time()
            music_len()
            pygame.mixer.music.play()
            try:
                mp3 = music_tag.load_file(f"assets/play_list/{music_name}")
                music_atwork = mp3["artwork"].first.data
                with open("assets/cover.jpg", "wb") as f: \
                        f.write(music_atwork)

                music_cover = CTkImage(Image.open("assets/cover.jpg"), size=(350, 350))
                image_label.configure(image=music_cover)
            except Exception:
                image_label.configure(image=music_image)

        elif textvariable.get() == 2:
            play_puase_btn.configure(image=play_image)
            textvariable.set(value=3)
            pygame.mixer.music.pause()
        elif textvariable.get() == 3:
            textvariable.set(value=2)
            play_puase_btn.configure(image=pause_image)
            pygame.mixer.music.unpause()

    except Exception:
        showwarning("Not Select Music", "Select a music")
        play_puase_btn.configure(image=play_image)
        textvariable.set(value=1)


def next_music():
    try:
        index = playlist.curselection()
        playlist.activate(index + 1)
        textvariable.set(1)
        play_pause()
    except IndexError:
        playlist.activate(0)
        textvariable.set(1)
        play_pause()


def prev_music():
    try:
        index = playlist.curselection()
        playlist.activate(index - 1)
        textvariable.set(1)
        play_pause()
    except IndexError:
        playlist.activate(END)
        textvariable.set(1)
        play_pause()


def stop_music():
    try:
        pygame.mixer.music.stop()
        index = playlist.curselection()
        playlist.deactivate(index)
        music_name_lable.configure(text=" ")
        image_label.configure(image=music_image)
        textvariable.set(value=1)
        play_puase_btn.configure(image=play_image)
        music_time.configure(text="00:00")
    except TypeError:
        showwarning("No Play", "No Play Any Music")


def move_slider(time):
    corent_state_var.set(value=time)
    index = playlist.curselection()
    music_name = playlist.get(index)
    pygame.mixer_music.load(f"assets/play_list/{music_name}")
    pygame.mixer_music.play(start=time)


def set_volume(volume):
    pygame.mixer_music.set_volume(volume)


##### grid of frames

window.grid_columnconfigure(1, weight=8)
window.grid_columnconfigure(3, weight=2)
window.grid_rowconfigure(0, weight=4)

# frames

ap_mode_frame = CTkFrame(window, fg_color="transparent", width=80)
cover_frame = CTkFrame(window, fg_color="transparent", height=450)
control_frame = CTkFrame(window, fg_color="transparent", height=150)
volume_frame = CTkFrame(window, fg_color="transparent", width=80)
play_list_frame = CTkFrame(window, fg_color="transparent", width=300)

ap_mode_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
cover_frame.grid(row=0, column=1, sticky="nsew")
control_frame.grid(row=1, column=1, sticky="ew")
volume_frame.grid(row=0, column=2, rowspan=4, padx=(0, 20), sticky="nsew")
play_list_frame.grid(row=0, column=3, sticky="nsew", rowspan=4)

##### widgets of ap mode

ap_lable = CTkLabel(ap_mode_frame, fg_color="transparent", bg_color="transparent", text="Theme:",
                    font=CTkFont(family="Times New Roman (Headings CS)", size=15, weight="bold"), justify="center")

state_var = StringVar(value="dark")
ap_switch = CTkSwitch(ap_mode_frame, switch_width=40, width=40, text="", onvalue="dark", offvalue="light",
                      variable=state_var, command=ap_mode, corner_radius=50)

ap_lable.pack(padx=8, pady=8)
ap_switch.pack()

##### widgets of cover and music name

music_name_lable = CTkLabel(cover_frame, text=" ", font=CTkFont(family="Georgia", size=27), justify="center")

music_image = CTkImage(Image.open("assets/album.png"), Image.open("assets/album.png"), size=(350, 350), )
image_label = CTkLabel(cover_frame, text="", image=music_image, corner_radius=150, width=350, height=350)

music_name_lable.grid(row=0, column=0, sticky="ew", pady=25, padx=(60, 20))
image_label.grid(row=1, column=0, sticky="nsew", pady=(0, 20), padx=(40, 0))

##### widgets of controllers

# load images Btn
play_image = CTkImage(Image.open("assets/play_light.png"), Image.open("assets/play_dark.png"), size=(60, 60))
pause_image = CTkImage(Image.open("assets/pause_light.png"), Image.open("assets/pause_dark.png"), size=(60, 60))
stop_image = CTkImage(Image.open("assets/stop_light.png"), Image.open("assets/stop_dark.png"), size=(50, 50))
right_image = CTkImage(Image.open("assets/right_light.png"), Image.open("assets/right_dark.png"), size=(40, 40))
left_image = CTkImage(Image.open("assets/left_light.png"), Image.open("assets/left_dark.png"), size=(40, 40))

# Btns
time_lapse = CTkLabel(control_frame, text="00:00", width=10)
time_lapse.grid(column=1, row=1, )

textvariable = IntVar(value=1)

play_puase_btn = CTkButton(control_frame, image=play_image, text="", fg_color="transparent", width=60, height=60,
                           command=play_pause)
stop_btn = CTkButton(control_frame, image=stop_image, text="", fg_color="transparent", width=50, height=50,
                     command=stop_music)
left_btn = CTkButton(control_frame, image=left_image, text="", fg_color="transparent", width=40, height=40,
                     command=prev_music)
right_btn = CTkButton(control_frame, image=right_image, text="", fg_color="transparent", width=1, height=1,
                      corner_radius=25, command=next_music)

left_btn.grid(column=3, row=0, sticky="nsew", padx=(110, 0))
stop_btn.grid(column=4, row=0, sticky="nsew")
play_puase_btn.grid(column=5, row=0, sticky="nsew")
right_btn.grid(column=6, row=0, sticky="nsew", padx=(0, 90))

state_var_time = IntVar(value=0)
time_slider = CTkSlider(control_frame, width=600, fg_color=("#98FB98", "#DDA0DD"),
                        progress_color=("#228B22", "#8B008B"), variable=state_var_time, command=move_slider, )
time_slider.grid(column=2, row=1, columnspan=5, pady=30)

music_time = CTkLabel(control_frame, text="00:00", width=10)
music_time.grid(column=8, row=1, )

##### widget of volume controll

volume_up_img = CTkImage(Image.open("assets/volume_up_light.png"),
                         Image.open("assets/volume_up_dark.png"), size=(25, 25))
volume_down_img = CTkImage(Image.open("assets/volume_down_light.png"),
                           Image.open("assets/volume_down_dark.png"), size=(25, 25))

v_up_btn = CTkButton(master=volume_frame, image=volume_up_img,
                     width=25, height=25, text="", fg_color="transparent")
v_up_btn.grid(row=0, column=0, pady=(130, 0))

v_slider_state_var = DoubleVar(value=1)
v_slider = CTkSlider(volume_frame, orientation="vertical", fg_color=("#98FB98", "#DDA0DD"),
                     progress_color=("#228B22", "#8B008B"), from_=0, to=1, variable=v_slider_state_var,
                     command=set_volume)
v_slider.grid(column=0, row=1)

v_down_btn = CTkButton(master=volume_frame, image=volume_down_img,
                       width=25, height=25, text="", fg_color="transparent")
v_down_btn.grid(row=2, column=0)

##### widgets of play list

playlist_name = CTkLabel(play_list_frame, text="Play List",
                         font=CTkFont(family="Georgia", size=25), justify="center")
playlist_name.grid(row=0, column=0, sticky="ew", pady=25, padx=(15))

playlist = CTkListbox(play_list_frame, height=380, corner_radius=15, width=190)
playlist.grid(row=1, column=0, sticky="nsew", padx=(13, 0))

plylistbtns_frame = CTkFrame(play_list_frame, fg_color="transparent")
plylistbtns_frame.grid(row=3, column=0, sticky="nsew", padx=(15), pady=(25, 15))

add_playlist_img = CTkImage(Image.open("assets/add_light.png"), Image.open("assets/add_dark.png"),
                            size=(45, 45))
remove_playlist_img = CTkImage(Image.open("assets/remove_light.png"),
                               Image.open("assets/remove_dark.png"), size=(40, 40))

add_btn = CTkButton(master=plylistbtns_frame, image=add_playlist_img, width=40, height=40,
                    text="", fg_color="transparent", command=add_play_list)
add_btn.grid(row=0, column=0, padx=(40, 25))

remove_btn = CTkButton(master=plylistbtns_frame, image=remove_playlist_img, width=40,
                       height=40, text="", fg_color="transparent", command=remove_play_list)
remove_btn.grid(row=0, column=1, padx=(0, 20))
show_play_list()
if __name__ == "__main__":
    window.mainloop()
