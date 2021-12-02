import hashlib
import tkinter as tk
import tkinter.messagebox as mb
import random
import tkinter.ttk

import bcrypt as bcrypt
import mysql.connector
import os
from pygame import mixer
from tkinter import *
from PIL import Image, ImageTk

import playsound
from gtts import gTTS
import speech_recognition as sr
listener = sr.Recognizer()

import sounddevice as sd
from scipy.io.wavfile import write
import wavio as wv

from PIL import Image, ImageTk


import pygame
from game import Game
from game2 import Game2
from game3 import Game3
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 450

db_connection = mysql.connector.connect(
    host="mysql.agh.edu.pl",
    user="user",
    password="pass")

db_cursor = db_connection.cursor(buffered=True)

global flag

class Login_Success_Window(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.original_frame = parent
        self.geometry("800x450+100+0")
        self.title("Strona główna")
        self.configure(background="#1B2127")
        self.lbl_Login_success = tk.Label(self, text="Witaj w grze", font=("Source Serif Pro Semibold", 26, "bold"),
                                          bg="#1B2127", fg="#2AB3D2")
        self.lbl_Login_success.place(relx=0.220, rely=0.050, height=50, width=300)

        # create OK button
        self.btn_animal_pl = tk.Button(self, text="Zwierzęta", font=("Source Serif Pro Semibold", 17, "bold"), bg="#CDCD13",
                                      fg="white", command=self.zwierzeta)
        self.btn_math = tk.Button(self, text="Matematyka", font=("Source Serif Pro Semibold", 17, "bold"), bg="#13CD13", fg="white",
                                      command=self.matematyka)
        self.btn_talk = tk.Button(self, text="Rozmowa \nz misiem", font=("Source Serif Pro Semibold", 17, "bold"), bg="#70CD13",
                                  fg="white",
                                  command=self.rozmowa)
        self.btn_song = tk.Button(self, text="Piosenki", font=("Source Serif Pro Semibold", 17, "bold"), bg="#13CD70",
                                  fg="white", command=self.songs)
        self.btn_stat = tk.Button(self, text="Statystyki", font=("Source Serif Pro Semibold", 14, "bold"), bg="#262B30",
                                  fg="white", command=self.statystyki)
        self.btn_register = tk.Button(self, text="Wyloguj", font=("Source Serif Pro Semibold", 14, "bold"), bg="#2AB3D2",
                                      fg="white", command=self.logout)
        # self.btn_register.pack(side = tk.BOTTOM)
        self.btn_animal_pl.place(relx=0.150, rely=0.300, height=70, width=200)
        self.btn_math.place(relx=0.550, rely=0.300, height=70, width=200)
        self.btn_talk.place(relx=0.150, rely=0.480, height=70, width=200)
        self.btn_song.place(relx=0.550, rely=0.480, height=70, width=200)
        self.btn_stat.place(relx=0.150, rely=0.800, height=56, width=200)

        self.btn_register.place(relx=0.550, rely=0.800, height=56, width=200)
        flag == 2
        print("KROK DRUGI: " + flag)


    def logout(self):  # to zrobie przycisk wyloguj
        self.destroy()
        self.original_frame.show()

    def show(self):
        self.update()
        self.deiconify()

    def rozmowa(self):
        self.withdraw()
        window = jarvan_win(self)
        window.grab_set()

    def statystyki(self):
        self.withdraw()
        window = statystyki_win(self)
        window.grab_set()

    def songs(self):
        self.withdraw()
        window = Play_songs(self)
        window.grab_set()

    def matematyka(self):
        self.withdraw()
        window = matematykaPoziomy(self)
        window.grab_set()

    def zwierzeta(self):
        self.withdraw()
        window = zwierzetaJezyk(self)
        window.grab_set()

class RegisterWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.original_frame = parent
        self.geometry("600x450+100+0")
        self.title("Strona rejestracji")
        self.configure(background="#1B2127")

        self.lblRegister = tk.Label(self, text="Rejestracja", font=("Source Serif Pro Semibold", 28, "bold"), bg="#1B2127",
                                    fg="#2AB3D2")
        self.lblFName = tk.Label(self, text="Imię dziecka:", font=("Source Serif Pro Semibold", 17, "bold"), bg="#1B2127",
                                 fg="white")
        self.lblUId = tk.Label(self, text="Login:", font=("Source Serif Pro Semibold", 17, "bold"), bg="#1B2127", fg="white")
        self.lblPwd = tk.Label(self, text="Hasło:", font=("Source Serif Pro Semibold", 17, "bold"), bg="#1B2127", fg="white")

        self.txtFName = tk.Entry(self, width=60, font=("Helvetica", 20))
        self.txtUId = tk.Entry(self, width=60, font=("Helvetica", 20))
        self.txtPwd = tk.Entry(self, show="*", width=60, font=("Helvetica", 20))


        self.btn_register = tk.Button(self, text="Stwórz konto", font=("Source Serif Pro Semibold", 14, "bold"), bg="red",
                                      fg="white", command=self.register)
        self.btn_cancel = tk.Button(self, text="Cofnij", font=("Source Serif Pro Semibold", 14, "bold"), bg="#262B30", fg="white",
                                    command=self.onClose)

        self.lblRegister.place(relx=0.300, rely=0.111, height=40, width=250)
        self.lblFName.place(relx=0.179, rely=0.306, height=30, width=145)
        self.lblUId.place(relx=0.290, rely=0.401, height=30, width=78)
        self.lblPwd.place(relx=0.275, rely=0.496, height=30, width=100)
        self.txtFName.place(relx=0.460, rely=0.296, height=33, relwidth=0.383)
        self.txtFName.focus_set()
        self.txtUId.place(relx=0.460, rely=0.391, height=33, relwidth=0.383)
        self.txtPwd.place(relx=0.460, rely=0.486, height=33, relwidth=0.383)
        self.btn_register.place(relx=0.240, rely=0.791, height=56, width=150)
        self.btn_cancel.place(relx=0.525, rely=0.791, height=56, width=150)

    def register(self):

        if db_connection.is_connected() == False:
            db_connection.connect()

        db_cursor.execute("use user")
        db_connection.commit()

        fname = self.txtFName.get()
        uid = self.txtUId.get()
        pwd = self.txtPwd.get()
        pwd_utf = pwd.encode('utf-8')
        pwd_encrypt = hashlib.md5(pwd_utf).hexdigest()

        if fname == "":
            mb.showinfo('Informacja', "Wpisz imię")
            self.txtFName.focus_set()
            return
        if uid == "":
            mb.showinfo('Informacja', "Wpisz nazwę użytkownika")
            self.txtUId.focus_set()
            return
        if pwd == "":
            mb.showinfo('Informacja', "Wpisz hasło")
            self.txtPwd.focus_set()
            return


        query = "INSERT INTO users(login,pass,child_name) VALUES ('%s','%s','%s')" % (uid, pwd_encrypt, fname)

        try:
            db_cursor.execute(query)
            mb.showinfo('Informacja', "Data inserted Successfully :) ")

            db_connection.commit()
        except:
            mb.showinfo('Information', "Data insertion failed!!! :( ")

            db_connection.rollback()

            db_connection.close()

    def onClose(self):

        self.destroy()
        self.original_frame.show()


class LoginApp(tk.Tk):
    def __init__(self):
        super().__init__()
        # icon = pygame.image.load('icon.png')
        # pygame.display.set_icon(icon)
        self.title("Strona logowania")
        self.geometry("600x450+100+0")
        self.configure(bg="#1B2127")
        self.lblHeading = tk.Label(self, text="Zaloguj się do gry", font=("Source Serif Pro Semibold", 26, "bold"), bg="#1B2127",
                                   fg="#2AB3D2")
        self.lbluname = tk.Label(self, text="Nazwa użytkownika:", font=("Source Serif Pro Semibold", 15, "bold"), bg="#1B2127",
                                 fg="white")
        self.lblpsswd = tk.Label(self, text="Hasło:", font=("Source Serif Pro Semibold", 15, "bold"), bg="#1B2127", fg="white")
        self.txtuname = tk.Entry(self, width=60, font=("Helvetica", 20))
        self.txtpasswd = tk.Entry(self, width=60, font=("Helvetica", 20), show="*")
        self.btn_login = tk.Button(self, text="Logowanie", font=("Source Serif Pro Semibold", 14, "bold"), bg="#262B30",
                                   fg="white", command=self.login)
        self.btn_clear = tk.Button(self, text="Wyczyść", font=("Source Serif Pro Semibold", 14, "bold"), bg="#262B30", fg="white",
                                   command=self.clear_form)
        self.btn_register = tk.Button(self, text="Rejestracja", font=("Source Serif Pro Semibold", 14, "bold"), bg="#262B30",
                                      fg="white", command=self.open_registration_window)
        self.btn_exit = tk.Button(self, text="Wyjście", font=("Source Serif Pro Semibold", 14, "bold"), bg="#2AB3D2", fg="white",
                                  command=self.exit)
        self.btn_prawa_autorskie = tk.Button(self, text="Prawa autorskie", font=("Source Serif Pro Semibold", 10, "bold"), bg="red",
                                  fg="white", command=self.prawa)

        self.lblHeading.place(relx=0.25, rely=0.089, height=41, width=300)  # x,y w oknie; wys szer calego napisu z tłem
        self.lbluname.place(relx=0.105, rely=0.289, height=21, width=200)
        self.lblpsswd.place(relx=0.292, rely=0.378, height=21, width=102)
        self.txtuname.place(relx=0.450, rely=0.289, height=30, relwidth=0.473)
        self.txtuname.focus_set()
        self.txtpasswd.place(relx=0.450, rely=0.378, height=30, relwidth=0.473)
        self.btn_login.place(relx=0.070, rely=0.550, height=56, width=150)
        self.btn_clear.place(relx=0.385, rely=0.550, height=56, width=150)
        self.btn_register.place(relx=0.695, rely=0.550, height=56, width=150)
        self.btn_exit.place(relx=0.550, rely=0.800, height=56, width=200)
        self.btn_prawa_autorskie.place(relx=0.03, rely=0.90, height=30, width=120)


    def prawa(self):
        self.withdraw()
        window = PrawaWindow(self)
        window.grab_set()

    def open_registration_window(self):
        self.withdraw()
        window = RegisterWindow(self)
        window.grab_set()

    def open_login_success_window(self):  # tu bedzie sie otwieralo okno z wyborem gier
        self.withdraw()
        window = Login_Success_Window(self)
        window.grab_set()

    def show(self):
        self.update()
        self.deiconify()

    def login(self):
        if db_connection.is_connected() == False:
            db_connection.connect()
        db_cursor.execute("use user")
        db_connection.commit()
        try:
            global username
            username = str(self.txtuname.get())
            passwd = str(self.txtpasswd.get())
            if username == "":
                mb.showinfo('Information', "Wpisz nazwę użytkownika")
                self.txtuname.focus_set()
                return
            if passwd == "":
                mb.showinfo('Information', "Wpisz hasło")
                self.txtpasswd.focus_set()
                return
            print(username)
            print(passwd)
            pwd_utf = passwd.encode('utf-8')
            passwd_hash = hashlib.md5(pwd_utf).hexdigest()
            print(passwd_hash)
            query = "SELECT * FROM users WHERE login = '" + username + "' AND pass = '" + passwd_hash + "'"
            print(query)
            db_cursor.execute(query)
            rowcount = db_cursor.rowcount
            print(rowcount)
            if db_cursor.rowcount == 1:
                self.open_login_success_window()
            else:
                mb.showinfo('Informacja', "Logowanie nie powiodło się. Niewłaściwa nazwa użytkownika lub hasło. Spróbuj ponownie :) ")
        except:
            db_connection.disconnect()
        self.clear_form()

    def clear_form(self):
        self.txtuname.delete(0, tk.END)
        self.txtpasswd.delete(0, tk.END)
        self.txtuname.focus_set()

    def exit(self):
        MsgBox = mb.askquestion('Exit Application', 'Are you sure you want to exit the application', icon='warning')
        if MsgBox == 'yes':
            self.destroy()

class PrawaWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.original_frame = parent
        self.geometry("600x450+100+0")
        self.title("Prawa autorskie")
        self.configure(background="#1B2127")

        self.lblPrawa = tk.Label(self, text="Prawa autorskie", font=("Source Serif Pro Semibold", 15, "bold"), bg="#1B2127",
                                    fg="red")
        self.btn_exit = tk.Button(self, text="Menu", font=("Source Serif Pro Semibold", 14, "bold"), bg="#262B30",fg="white",command=self.menu)

        self.lblLinki = tk.Label(self, text="Piosenki:\n\n"
                                            "https://www.youtube.com/watch?v=bc2fcIA11QI&t=8s\n"
                                            "https://www.youtube.com/watch?v=JdcGTOAAuKg&t=11s\n"
                                            "https://www.youtube.com/watch?v=vQbS0Dm0CjA&t=126s\n"
                                            "https://www.youtube.com/watch?v=38QNVaK7a-s&t=84s\n\n"
                                            "Grafiki:\n\n", font=("Source Serif Pro Semibold", 12, "bold"),bg="#1B2127",fg="white")

        self.lblLinki.place(relx=0.05, rely=0.1, height=200, width=570)
        self.lblPrawa.place(relx=0.25, rely=0.005, height=20, width=300)
        self.btn_exit.place(relx=0.75, rely=0.850, height=56, width=120)

    def menu(self):
        self.destroy()
        self.original_frame.show()


class jarvan_win(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.original_frame = parent
        self.geometry("600x450+100+0")
        self.title("Rozmowa z misiem")
        #self.configure(background="#EC1C5B")

        load = Image.open(r"mis.jpg")
        render = ImageTk.PhotoImage(load)
        img = Label(self, image=render)
        img.image = render
        img.place(x=0, y=0)

        self.lbl_Login_success = tk.Label(self, text="Rozmowa z misiem", font=("Source Serif Pro Semibold", 26, "bold"),
                                          bg="#EC1C5B", fg="white")

        self.btn_rozmawiaj = tk.Button(self, text="Rozmawiaj", font=("Source Serif Pro Semibold", 14, "bold",),
                                      bg="#262B30", fg="white", command=self.rozmowa)
        self.lbl_wyjscie = tk.Label(self, text="Pożegnaj misia, aby wyjść",
                                    font=("Source Serif Pro Semibold", 13, "bold"),
                                    bg="white", fg="black")

        self.btn_rozmawiaj.place(relx=0.350, rely=0.04, height=56, width=200)
        self.lbl_wyjscie.place(relx=0.270, rely=0.165, height=30, width=300)

    def rozmowa(self):
        from subprocess import call
        call(["python", "jarvan.py"])
        mixer.init()
        mixer.music.stop()
        self.destroy()
        self.original_frame.show()


class Play_songs(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.original_frame = parent
        self.geometry("600x450+100+0")
        self.title("Piosenki")
        self.configure(background="#1B2127")
        self.lbl_Login_success = tk.Label(self, text="Piosenki", font=("Source Serif Pro Semibold", 26, "bold"),
                                          bg="#1B2127", fg="#2AB3D2")
        self.lbl_Login_success.place(relx=0.220, rely=0.050, height=50, width=300)

        # create OK button
        self.btn_numer1 = tk.Button(self, text="Alfabet", font=("Source Serif Pro Semibold", 14, "bold"), bg="#2F09DC",
                                      fg="white", command=self.numer1)
        self.btn_numer2 = tk.Button(self, text="Cyferki", font=("Source Serif Pro Semibold", 14, "bold"),
                                       bg="#9909DC",fg="white", command=self.numer2)
        self.btn_numer3 = tk.Button(self, text="Odgłosy zwierząt", font=("Source Serif Pro Semibold", 14, "bold"), bg="#DC09B5", fg="white", command=self.numer3)
        self.btn_numer4 = tk.Button(self, text="Owoce i warzywa", font=("Source Serif Pro Semibold", 14, "bold"), bg="#DC094C", fg="white", command=self.numer4)
        self.btn_nagraj = tk.Button(self, text="Nagraj", font=("Source Serif Pro Semibold", 14, "bold"), bg="red",
                                    fg="white", command=self.nagraj)
        self.btn_odtworz = tk.Button(self, text="Odtwórz", font=("Source Serif Pro Semibold", 14, "bold"), bg="#262B30",
                                    fg="white", command=self.odtworz)
        self.btn_register = tk.Button(self, text="Menu", font=("Source Serif Pro Semibold", 14, "bold", ),
                                      bg="#2AB3D2",fg="white",command=self.logout)

        self.btn_numer1.place(relx=0.150, rely=0.200, height=56, width=200)
        self.btn_numer2.place(relx=0.150, rely=0.350, height=56, width=200)
        self.btn_numer3.place(relx=0.150, rely=0.500, height=56, width=200)
        self.btn_numer4.place(relx=0.150, rely=0.650, height=56, width=200)
        self.btn_nagraj.place(relx=0.550, rely=0.200, height=56, width=200)
        self.btn_odtworz.place(relx=0.550, rely=0.350, height=56, width=200)
        self.btn_register.place(relx=0.550, rely=0.800, height=56, width=200)

    def logout(self):  # to zrobie przycisk wyloguj
        mixer.init()
        mixer.music.stop()
        self.destroy()
        self.original_frame.show()

    def numer1(self):
        mixer.init()
        mixer.music.load("piosenki/alfabet.mp3")
        mixer.music.set_volume(1)
        mixer.music.play()

    def numer2(self):
        mixer.init()
        mixer.music.load("piosenki/cyferki.mp3")
        mixer.music.set_volume(0.7)
        mixer.music.play()

    def numer3(self):
        mixer.init()
        mixer.music.load("piosenki/odglosy-zwierzat.mp3")
        mixer.music.set_volume(0.7)
        mixer.music.play()

    def numer4(self):
        mixer.init()
        mixer.music.load("piosenki/na-straganie.mp3")
        mixer.music.set_volume(0.7)
        mixer.music.play()

    def nagraj(self):
        mixer.init()
        mixer.music.stop()
        freq = 44100
        duration = 5
        recording = sd.rec(int(duration * freq), samplerate=freq, channels=2)
        sd.wait()
        os.remove("recording1.wav")
        wv.write("recording1.wav", recording, freq, sampwidth=2)

    def odtworz(self):
        mixer.init()
        mixer.music.load("recording1.wav")
        mixer.music.set_volume(0.7)
        mixer.music.play()
        while mixer.music.get_busy():
            continue
        mixer.music.stop()

class matematykaPoziomy(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.original_frame = parent
        self.geometry("600x450+100+0")
        self.title("Matematyka")
        self.configure(background="#1B2127")
        self.lbl_Login_success = tk.Label(self, text="Matematyka - poziomy", font=("Source Serif Pro Semibold", 20, "bold"),
                                          bg="#1B2127", fg="#2AB3D2")
        self.lbl_Login_success.place(relx=0.220, rely=0.050, height=50, width=350)

        # create OK button
        self.btn_numer1 = tk.Button(self, text="Poziom 1", font=("Source Serif Pro Semibold", 14, "bold"), bg="#13CDCD",
                                      fg="white", command=lambda: self.wyborPoziomu(1))
        self.btn_numer2 = tk.Button(self, text="Poziom 2", font=("Source Serif Pro Semibold", 14, "bold"),
                                       bg="#1370CD",fg="white", command=lambda: self.wyborPoziomu(2))
        self.btn_numer3 = tk.Button(self, text="Poziom 3", font=("Source Serif Pro Semibold", 14, "bold"), bg="#1313CD", fg="white", command=lambda: self.wyborPoziomu(3))

        self.btn_register = tk.Button(self, text="Menu", font=("Source Serif Pro Semibold", 14, "bold", ),
                                      bg="#2AB3D2",fg="white",command=self.logout)

        self.btn_numer1.place(relx=0.350, rely=0.250, height=56, width=200)
        self.btn_numer2.place(relx=0.350, rely=0.400, height=56, width=200)
        self.btn_numer3.place(relx=0.350, rely=0.550, height=56, width=200)
        self.btn_register.place(relx=0.550, rely=0.800, height=56, width=200)

    def logout(self):  # to zrobie przycisk wyloguj
        self.destroy()
        self.original_frame.show()
    def wyborPoziomu(self, poziom):
        x = 100
        y = 40
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d, %d" % (x, y)
        pygame.init()
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Matematyka")
        # Loop until the user clicks the close button.
        done = False
        # Used to manage how fast the screen updates
        clock = pygame.time.Clock()
        if poziom == 1:
            game = Game()
        elif poziom == 2:
            game = Game2()
        elif poziom == 3:
            game = Game3()

        # -------- Main Program Loop -----------
        while not done:
            # --- Process events (keystrokes, mouse clicks, etc)
            done = game.process_events()
            # --- Game logic should go here
            game.run_logic()
            # --- Draw the current frame
            game.display_frame(screen)
            # --- Limit to 30 frames per second
            clock.tick(30)
        pygame.quit()

class zwierzetaJezyk(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.original_frame = parent
        self.geometry("600x450+100+0")
        self.title("Zwierzęta")
        self.configure(background="#1B2127")
        self.lbl_Login_success = tk.Label(self, text="Zwierzęta", font=("Source Serif Pro Semibold", 26, "bold"),
                                          bg="#1B2127", fg="#2AB3D2")
        self.lbl_Login_success.place(relx=0.220, rely=0.050, height=50, width=350)

        self.btn_zwierzetaPL = tk.Button(self, text="Zwierzęta PL", font=("Source Serif Pro Semibold", 14, "bold"), bg="#EF1AEF",
                                      fg="white",command=self.zwierzetaPL)
        self.btn_zwierzetaANG = tk.Button(self, text="Zwierzęta ANG", font=("Source Serif Pro Semibold", 14, "bold"),
                                       bg="#EF1A84",fg="white",command=self.zwierzetaANG)

        self.btn_menu = tk.Button(self, text="Menu", font=("Source Serif Pro Semibold", 14, "bold", ),
                                      bg="#2AB3D2",fg="white",command=self.menu)

        self.btn_zwierzetaPL.place(relx=0.350, rely=0.250, height=56, width=200)
        self.btn_zwierzetaANG.place(relx=0.350, rely=0.400, height=56, width=200)
        self.btn_menu.place(relx=0.550, rely=0.800, height=56, width=200)

    def menu(self):
        self.destroy()
        self.original_frame.show()
    def show(self):
        self.update()
        self.deiconify()
    def zwierzetaPL(self):
        from subprocess import call
        call(["python", "speech-animal-pl.py"])
    def zwierzetaANG(self):
        from subprocess import call
        call(["python", "speech-animal-eng.py"])


class statystyki_win(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.original_frame = parent
        self.geometry("600x450+100+0")
        self.title("Statystyki")
        self.configure(background="#1B2127")
        self.lbl_Login_success = tk.Label(self, text="Statystyki z gier", font=("Source Serif Pro Semibold", 26, "bold"),
                                          bg="#1B2127", fg="#2AB3D2")
        self.lbl_Login_success.place(relx=0.220, rely=0.050, height=50, width=350)

        self.btn_zwierzeta = tk.Button(self, text="Zwierzęta", font=("Source Serif Pro Semibold", 14, "bold"), bg="#1AEF1A",
                                      fg="white",command=self.zwierzeta)
        self.btn_matematyka = tk.Button(self, text="Matematyka", font=("Source Serif Pro Semibold", 14, "bold"),
                                       bg="#1AEF84",fg="white",command=self.matematyka)

        self.btn_menu = tk.Button(self, text="Menu", font=("Source Serif Pro Semibold", 14, "bold", ),
                                      bg="#2AB3D2",fg="white",command=self.menu)

        self.btn_zwierzeta.place(relx=0.350, rely=0.250, height=56, width=200)
        self.btn_matematyka.place(relx=0.350, rely=0.400, height=56, width=200)
        self.btn_menu.place(relx=0.550, rely=0.800, height=56, width=200)

    def menu(self):  # to zrobie przycisk wyloguj
        self.destroy()
        self.original_frame.show()
    def show(self):
        self.update()
        self.deiconify()
    def zwierzeta(self):
        self.withdraw()
        window = ZwierzetaStat(self)
        window.grab_set()
    def matematyka(self):
        self.withdraw()
        window = MatematykaStat(self)
        window.grab_set()

class MatematykaStat(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.original_frame = parent
        self.geometry("600x450+100+0")
        self.title("Matematyka Statystyki")
        self.configure(background="#1B2127")
        self.lbl_Login_success1 = tk.Label(self, text="Poziom 1", font=("Source Serif Pro Semibold", 15, "bold"), bg="#1B2127", fg="#2AB3D2")
        self.lbl_Login_success1.place(relx=0.650, rely=0.003, height=50, width=150)
        self.lbl_Login_success2 = tk.Label(self, text="Poziom 2", font=("Source Serif Pro Semibold", 15, "bold"), bg="#1B2127", fg="#2AB3D2")
        self.lbl_Login_success2.place(relx=0.650, rely=0.233, height=50, width=150)
        self.lbl_Login_success3 = tk.Label(self, text="Poziom 3", font=("Source Serif Pro Semibold", 15, "bold"), bg="#1B2127", fg="#2AB3D2")
        self.lbl_Login_success3.place(relx=0.650, rely=0.463, height=50, width=150)

        self.btn_dodawanie1 = tk.Button(self, text="+", font=("Source Serif Pro Semibold", 25, "bold"), bg="#262B30", fg="white", command=lambda: self.wyniki(1.1))
        self.btn_odejmowanie1 = tk.Button(self, text="-", font=("Source Serif Pro Semibold", 25, "bold"), bg="#262B30",fg="white", command=lambda: self.wyniki(1.2))
        self.btn_mnozenie1 = tk.Button(self, text="*", font=("Source Serif Pro Semibold", 25, "bold"), bg="#262B30", fg="white", command=lambda: self.wyniki(1.3))
        self.btn_dzielenie1 = tk.Button(self, text="/", font=("Source Serif Pro Semibold", 25, "bold"), bg="#262B30", fg="white", command=lambda: self.wyniki(1.4))

        self.btn_dodawanie1.place(relx=0.610, rely=0.1, height=50, width=50)
        self.btn_odejmowanie1.place(relx=0.700, rely=0.1, height=50, width=50)
        self.btn_mnozenie1.place(relx=0.790, rely=0.1, height=50, width=50)
        self.btn_dzielenie1.place(relx=0.880, rely=0.1, height=50, width=50)

        self.btn_dodawanie2 = tk.Button(self, text="+", font=("Source Serif Pro Semibold", 25, "bold"),bg="#262B30", fg="white", command=lambda: self.wyniki(2.1))
        self.btn_odejmowanie2 = tk.Button(self, text="-", font=("Source Serif Pro Semibold", 25, "bold"), bg="#262B30", fg="white", command=lambda: self.wyniki(2.2))
        self.btn_mnozenie2 = tk.Button(self, text="*", font=("Source Serif Pro Semibold", 25, "bold"),bg="#262B30", fg="white", command=lambda: self.wyniki(2.3))
        self.btn_dzielenie2 = tk.Button(self, text="/", font=("Source Serif Pro Semibold", 25, "bold"), bg="#262B30", fg="white", command=lambda: self.wyniki(2.4))

        self.btn_dodawanie2.place(relx=0.610, rely=0.33, height=50, width=50)
        self.btn_odejmowanie2.place(relx=0.700, rely=0.33, height=50, width=50)
        self.btn_mnozenie2.place(relx=0.790, rely=0.33, height=50, width=50)
        self.btn_dzielenie2.place(relx=0.880, rely=0.33, height=50, width=50)

        self.btn_dodawanie3 = tk.Button(self, text="+", font=("Source Serif Pro Semibold", 25, "bold"), bg="#262B30", fg="white", command=lambda: self.wyniki(3.1))
        self.btn_odejmowanie3 = tk.Button(self, text="-", font=("Source Serif Pro Semibold", 25, "bold"),bg="#262B30", fg="white", command=lambda: self.wyniki(3.2))
        self.btn_mnozenie3 = tk.Button(self, text="*", font=("Source Serif Pro Semibold", 25, "bold"), bg="#262B30", fg="white", command=lambda: self.wyniki(3.3))
        self.btn_dzielenie3 = tk.Button(self, text="/", font=("Source Serif Pro Semibold", 25, "bold"),bg="#262B30", fg="white", command=lambda: self.wyniki(3.4))

        self.btn_dodawanie3.place(relx=0.610, rely=0.56, height=50, width=50)
        self.btn_odejmowanie3.place(relx=0.700, rely=0.56, height=50, width=50)
        self.btn_mnozenie3.place(relx=0.790, rely=0.56, height=50, width=50)
        self.btn_dzielenie3.place(relx=0.880, rely=0.56, height=50, width=50)

        self.btn_menu = tk.Button(self, text="Cofnij", font=("Source Serif Pro Semibold", 14, "bold",), bg="#2AB3D2", fg="white", command=self.menu)
        self.btn_menu.place(relx=0.550, rely=0.800, height=56, width=200)


    def menu(self):  # to zrobie przycisk wyloguj
        self.destroy()
        self.original_frame.show()

    def wyniki(self, a):
        a=str(a)
        my_conn=db_connection.cursor()
        query = "SELECT score, game_date FROM games WHERE game_id = ('%s') ORDER BY id DESC LIMIT 10" % (a)
        my_conn.execute(query)
        i = 1
        for student in my_conn:
            for j in range(len(student)): #ile kolumn
                a = Label(self, text="Punkty", font=("Source Serif Pro Semibold", 13, "bold"), bg="#1B2127", fg="#2AB3D2")
                b = Label(self, text="Data", font=("Source Serif Pro Semibold", 13, "bold"), bg="#1B2127", fg="#2AB3D2")
                a.grid(row=0, column=0)
                b.grid(row=0, column=1)
                e = Entry(self, width=10, fg='white', bd=1, justify=CENTER, bg="#262B30", font=("Source Serif Pro Semibold", 11, "bold"))
                e.grid(row=i, column=j, ipadx=36, ipady=7)
                e.insert(END, student[j])
            i = i + 1

class ZwierzetaStat(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.original_frame = parent
        self.geometry("600x450+100+0")
        self.title("Matematyka Statystyki")
        self.configure(background="#1B2127")
        self.btn_zwierzetapl = tk.Button(self, text="Zwierzęta PL", font=("Source Serif Pro Semibold", 14, "bold"), bg="#262B30",
                                      fg="white", command=lambda: self.wyniki(4.1))
        self.btn_zwierzetaang = tk.Button(self, text="Zwierzęta ANG", font=("Source Serif Pro Semibold", 14, "bold"),
                                       bg="#262B30",fg="white", command=lambda: self.wyniki(4.2))

        self.btn_menu = tk.Button(self, text="Cofnij", font=("Source Serif Pro Semibold", 14, "bold", ),
                                      bg="#2AB3D2",fg="white",command=self.menu)

        self.btn_zwierzetapl.place(relx=0.610, rely=0.1, height=56, width=200)
        self.btn_zwierzetaang.place(relx=0.610, rely=0.3, height=56, width=200)
        self.btn_menu.place(relx=0.550, rely=0.800, height=56, width=200)

    def menu(self):  # to zrobie przycisk wyloguj
        self.destroy()
        self.original_frame.show()
    def wyniki(self, a):
        a=str(a)
        my_conn=db_connection.cursor()
        query = "SELECT score, game_date FROM games WHERE game_id = ('%s') ORDER BY id DESC LIMIT 10" % (a)
        my_conn.execute(query)
        i = 1
        for student in my_conn:
            for j in range(len(student)): #ile kolumn
                a = Label(self, text="Punkty", font=("Source Serif Pro Semibold", 13, "bold"), bg="#1B2127", fg="#2AB3D2")
                b = Label(self, text="Data", font=("Source Serif Pro Semibold", 13, "bold"), bg="#1B2127", fg="#2AB3D2")
                a.grid(row=0, column=0)
                b.grid(row=0, column=1)
                e = Entry(self, width=10, fg='white', bd=1, justify=CENTER, bg="#262B30", font=("Source Serif Pro Semibold", 11, "bold"))
                e.grid(row=i, column=j, ipadx=36, ipady=7)
                e.insert(END, student[j])
            i = i + 1

if __name__ == "__main__":
    app = LoginApp()
    app.mainloop()
