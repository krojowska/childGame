# -*- coding: utf-8
import pygame
import os
import time
import speech_recognition as sr
from pygame import mixer

import mysql.connector

db_connection = mysql.connector.connect(
    host="mysql.agh.edu.pl",
    user="user",
    password="pass")

db_cursor = db_connection.cursor(buffered=True)

mixer.init()
# toy.db -> animals_pl
x = 110
y = 30
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d, %d" % (x, y)
gameDisplay = pygame.display.set_mode((600, 450))

pngs = [x for x in os.listdir(r"C:\Users\Dzban\Desktop\Math-games-master\Math-games-master\animals-eng")]
names = [x.split(".")[0] for x in os.listdir(r"C:\Users\Dzban\Desktop\Math-games-master\Math-games-master\animals-eng")]

animals = {k: v for k, v in zip(pngs, names)}
print(animals)
print(pngs)
print(names)

pygame.init()
WHITE = (255,255,255)
good_answers = 0

for n, animals in enumerate(pngs):

    font = pygame.font.Font(None, 65)
    score_font = pygame.font.Font("Jiczyn.ttf", 20)
    general_font = pygame.font.Font("chunkfive.ttf", 30)
    score_label = score_font.render("Points: " + str(good_answers), True, WHITE)
    animal_label = general_font.render("What is this animal?", True, WHITE)
    gameDisplay.blit(score_label, (10, 10))
    gameDisplay.blit(animal_label, (180, 10))

    background_image = pygame.image.load("background1.jpg").convert()

    response_counter = 0
    animalImg = pygame.image.load(os.path.join(r"C:\Users\Dzban\Desktop\Math-games-master\Math-games-master\animals-eng\\", animals))
    gameDisplay.blit(animalImg, (0, 40))
    pygame.display.update()
    # pygame.mixer.Sound.play(Tiger)
    # pygame.mixer.music.stop()
    # time.sleep(1)
    for j in range(1, 4):
        gameDisplay.blit(background_image,(0,0))
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print('What kind of pet is this?')
            audio = r.listen(source)
            try:
                text = r.recognize_google(audio)
                print(text)
            except:
                print('I dont understand, speak more clearly')
                text = ''
            if text == names[n]:
                print('Very good!!!')
                good_answers = good_answers + 1
                mixer.music.load('dobrze.mp3')
                #mixer.music.set_volume(0.7)
                mixer.music.play()
                while mixer.music.get_busy():
                    continue
                mixer.music.stop()
                break
            else:
                if response_counter < 3:
                    print('Wrong answer, please try again')
                    pygame.mixer.music.load('zle.mp3')
                    pygame.mixer.music.play()
                    while mixer.music.get_busy():
                        continue
                    pygame.mixer.music.stop()
                    time.sleep(1)
                    response_counter += 1 # 3 razy mozna sprobowac odgadnac, potem sie zmienia obrazek
    time.sleep(1)

pygame.display.update()
gameDisplay.blit(background_image, (0, 0))


result_label = general_font.render("Your number of points: " + str(good_answers), True, WHITE)
gameDisplay.blit(result_label, (180, 330))
db_cursor.execute("use user")
game_id = '4.2'
query = "INSERT INTO games(login,game_id,score) VALUES ('%s','%s','%s')" % ("kris12", game_id, good_answers)
try:
    db_cursor.execute(query)
    print("Data inserted Successfully :) ")

    db_connection.commit()
except:
    print("Data insertion failed!!! :( ")

    db_connection.rollback()

    db_connection.close()
pygame.display.update()
time.sleep(5)

print(good_answers)
pygame.quit()