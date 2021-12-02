#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame, random
from menu import Menu
import mysql.connector

db_connection = mysql.connector.connect(
    host="mysql.agh.edu.pl",
    user="user",
    password="pass")

db_cursor = db_connection.cursor(buffered=True)

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0,128,0)
RED = (255, 0, 0)


class Game2(object):
    def __init__(self):
        self.font = pygame.font.Font(None, 65)
        self.score_font = pygame.font.Font("Jiczyn.ttf", 30)
        self.problem = {"num1": 0, "num2": 0, "result": 0}
        self.operation = ""
        self.symbols = self.get_symbols()
        self.button_list = self.get_button_list()
        self.reset_problem = False
        items = ("Dodawanie", "Odejmowanie", "Mnozenie", "Dzielenie", "- Wyjscie -")
        self.menu = Menu(items, ttf_font="Jiczyn.ttf", font_size=50)
        self.show_menu = True
        self.score = 0
        self.count = 0
        self.background_image = pygame.image.load("math.jpg").convert()
        self.sound_1 = pygame.mixer.Sound("item1.ogg")
        self.sound_2 = pygame.mixer.Sound("item2.ogg")

    def get_button_list(self):
        """ Return a list with four buttons """
        button_list = []
        choice = random.randint(1, 4)
        width = 140
        height = 120
        t_w = width * 2 + 50
        posX = (SCREEN_WIDTH / 2) - (t_w / 2)
        posY = 150
        if choice == 1:
            btn = Button(posX, posY, width, height, self.problem["result"])
            button_list.append(btn)
        else:
            btn = Button(posX, posY, width, height, random.randint(0, 30))
            button_list.append(btn)

        posX = (SCREEN_WIDTH / 2) - (t_w / 2) + 150

        if choice == 2:
            btn = Button(posX, posY, width, height, self.problem["result"])
            button_list.append(btn)
        else:
            btn = Button(posX, posY, width, height, random.randint(0, 30))  # !!!!! losuje zakres złych odpowiedzi
            button_list.append(btn)

        posX = (SCREEN_WIDTH / 2) - (t_w / 2)
        posY = 300

        if choice == 3:
            btn = Button(posX, posY, width, height, self.problem["result"])
            button_list.append(btn)
        else:
            btn = Button(posX, posY, width, height, random.randint(0, 30))
            button_list.append(btn)

        posX = (SCREEN_WIDTH / 2) - (t_w / 2) + 150

        if choice == 4:
            btn = Button(posX, posY, width, height, self.problem["result"])
            button_list.append(btn)
        else:
            btn = Button(posX, posY, width, height, random.randint(0, 30))
            button_list.append(btn)

        return button_list

    def get_symbols(self):
        """ Return a dictionary with all the operation symbols """
        symbols = {}
        sprite_sheet = pygame.image.load("symbols.png").convert()
        image = self.get_image(sprite_sheet, 0, 0, 64, 64)
        symbols["addition"] = image
        image = self.get_image(sprite_sheet, 64, 0, 64, 64)
        symbols["subtraction"] = image
        image = self.get_image(sprite_sheet, 128, 0, 64, 64)
        symbols["multiplication"] = image
        image = self.get_image(sprite_sheet, 192, 0, 64, 64)
        symbols["division"] = image

        return symbols

    def get_image(self, sprite_sheet, x, y, width, height):
        """ This method will cut an image and return it """
        image = pygame.Surface([width, height]).convert()
        image.blit(sprite_sheet, (0, 0), (x, y, width, height))
        return image

    def addition(self):
        """ These will set num1,num2,result for addition """
        a = random.randint(0, 10)
        b = random.randint(0, 10)
        self.problem["num1"] = a
        self.problem["num2"] = b
        self.problem["result"] = a + b
        self.operation = "addition"

    def subtraction(self):
        """ These will set num1,num2,result for subtraction """
        a = random.randint(0, 20)
        b = random.randint(0, 20)
        if a > b:
            self.problem["num1"] = a
            self.problem["num2"] = b
            self.problem["result"] = a - b
        else:
            self.problem["num1"] = b
            self.problem["num2"] = a
            self.problem["result"] = b - a
        self.operation = "subtraction"

    def multiplication(self):
        """ These will set num1,num2,result for multiplication """
        a = random.randint(0, 5)
        b = random.randint(0, 10)
        self.problem["num1"] = a
        self.problem["num2"] = b
        self.problem["result"] = a * b
        self.operation = "multiplication"

    def division(self):
        """ These will set num1,num2,result for division """
        divisor = random.randint(1, 10)
        dividend = divisor * random.randint(1, 5)
        quotient = dividend / divisor
        self.problem["num1"] = dividend
        self.problem["num2"] = divisor
        self.problem["result"] = quotient
        self.operation = "division"

    def check_result(self):
        """ Check the result """
        for button in self.button_list:
            if button.isPressed():
                if button.get_number() == self.problem["result"]:
                    button.set_color(GREEN)
                    self.score += 1
                    self.sound_1.play()
                else:
                    button.set_color(RED)
                    self.sound_2.play()
                self.reset_problem = True

    def set_problem(self):
        global game_id
        """ do another problem again """
        if self.operation == "addition":
            game_id = '2.1'
            self.addition()
        elif self.operation == "subtraction":
            game_id = '2.2'
            self.subtraction()
        elif self.operation == "multiplication":
            game_id = '2.3'
            self.multiplication()
        elif self.operation == "division":
            game_id = '2.4'
            self.division()
        self.button_list = self.get_button_list()

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # If user clicked close to wtedy zwraca true i przerywa sie petla
                return True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.show_menu:
                    if self.menu.state == 0:
                        self.operation = "addition"
                        self.set_problem()
                        self.show_menu = False
                    elif self.menu.state == 1:
                        self.operation = "subtraction"
                        self.set_problem()
                        self.show_menu = False
                    elif self.menu.state == 2:
                        self.operation = "multiplication"
                        self.set_problem()
                        self.show_menu = False
                    elif self.menu.state == 3:
                        self.operation = "division"
                        self.set_problem()
                        self.show_menu = False
                    elif self.menu.state == 4:
                        pygame.QUIT
                        return True
                else:
                    self.check_result()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.show_menu = True
                    self.score = 0
                    self.count = 0

        return False

    def run_logic(self):
        self.menu.update()

    def display_message(self, screen, items):
        """ display every string that is inside of a tuple(args) """
        for index, message in enumerate(items):
            label = self.font.render(message, True, BLACK)
            width = label.get_width()
            height = label.get_height()

            posX = (SCREEN_WIDTH / 2) - (width / 2)
            t_h = len(items) * height
            posY = (SCREEN_HEIGHT / 2) - (t_h / 2) + (index * height)

            screen.blit(label, (posX, posY))

    def display_frame(self, screen):
        screen.blit(self.background_image, (0, 0))
        time_wait = False
        if self.show_menu:
            self.menu.display_frame(screen)
        elif self.count == 10 :  # ilosc pytan !!!!!!!!!!!!!!!!!!!!
            msg_1 = "Poprawne odpowiedzi: " + str(self.score)
            msg_2 = "Ilość Twoich punktów to: " + str(self.score)
            self.display_message(screen, (msg_1, msg_2))
            self.show_menu = True
            # zapis do bazy
            db_cursor.execute("use user")
            query = "INSERT INTO games(login,game_id,score) VALUES ('%s','%s','%s')" % ("kris12", game_id, self.score)
            try:
                db_cursor.execute(query)
                print("Data inserted Successfully :) ")

                db_connection.commit()
            except:
                print("Data insertion failed!!! :( ")

                db_connection.rollback()

                db_connection.close()

            self.score = 0
            self.count = 0
            time_wait = True
        else:
            label_1 = self.font.render(str(self.problem["num1"]), True, BLACK)
            label_2 = self.font.render(str(self.problem["num2"]) + " = ...", True, BLACK)
            t_w = label_1.get_width() + label_2.get_width() + 64  # 64: length of symbol
            posX = (SCREEN_WIDTH / 2) - (t_w / 2)
            screen.blit(label_1, (posX, 50))
            screen.blit(self.symbols[self.operation], (posX + label_1.get_width(), 40))

            screen.blit(label_2, (posX + label_1.get_width() + 64, 50))
            for btn in self.button_list:
                btn.draw(screen)
            score_label = self.score_font.render("Punkty: " + str(self.score), True, BLACK)
            screen.blit(score_label, (430, 10))
            score_label1 = self.score_font.render("Ile to jest?", True, BLACK)
            screen.blit(score_label1, (110, 10))

        pygame.display.flip()

        if self.reset_problem:
            pygame.time.wait(1000)
            self.set_problem()
            self.count += 1
            self.reset_problem = False
        elif time_wait:
            pygame.time.wait(3000)


class Button(object):
    def __init__(self, x, y, width, height, number):
        self.rect = pygame.Rect(x, y, width, height)
        self.font = pygame.font.Font(None, 60)
        self.text = self.font.render(str(number), True, BLACK)
        self.number = number
        self.background_color = "#00BFFF"

    def draw(self, screen):
        """ This method will draw the button to the screen """
        pygame.draw.rect(screen, self.background_color, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 5)
        width = self.text.get_width()
        height = self.text.get_height()
        posX = self.rect.centerx - (width / 2)
        posY = self.rect.centery - (height / 2)
        screen.blit(self.text, (posX, posY))

    def isPressed(self):
        """ Return true if the mouse is on the button """
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            return True
        else:
            return False

    def set_color(self, color):
        """ Set the background color """
        self.background_color = color

    def get_number(self):
        """ Return the number of the button."""
        return self.number
