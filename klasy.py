import random
import pygame
pygame.init()
from tetris import DrawText
from stałe import black
typy_bloków = ['o', 'i', 't', 'l', 'j', 's', 'z']
ZnakiSpecjalne = ['', '\t', '\x1b', '\r']
class type:
    def __init__(self):
        self.typ = random.choice(typy_bloków)
    
    def new(self):
        self.typ = random.choice(typy_bloków)
    def to(self, towhat):
        if towhat in typy_bloków:
            self.typ = towhat
    @property
    def value(self):
        return self.typ

class position:
    def __init__(self):
        self.pozycja = "p1"
    def __add__(self, other):
        return ('p' + str(max(((int(self.pozycja[1]) + other) % 5, 1))))
    def next(self):
        self.pozycja = ('p' + str(max(((int(self.pozycja[1]) + 1) % 5, 1))))
    def reset(self):
        self.pozycja = "p1"
    @property
    def value(self):
        return self.pozycja




class button:
    def __init__(self, text, TextColor, NormalColor, ColorOnHover, x, y, witdh, height, OnClick):
        self.text = text
        self.color = NormalColor
        self.NormalColor = NormalColor
        self.x = x
        self.y = y
        self.witdh = witdh
        self.height = height
        self.OnClick = OnClick
        self.ColorOnHover = ColorOnHover
        self.TextColor = TextColor
    
    def events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            if x >= self.x - self.witdh // 2 and x <= self.x + self.witdh // 2 and y >= self.y - self.height // 2 and y <= self.y + self.height // 2:
                self.OnClick()
        elif event.type == pygame.MOUSEMOTION:
            x, y = pygame.mouse.get_pos()
            if x >= self.x - self.witdh // 2 and x <= self.x + self.witdh // 2 and y >= self.y - self.height // 2 and y <= self.y + self.height // 2:
                self.color = self.ColorOnHover
            else:
                self.color = self.NormalColor
    
    def draw(self, screen):

        pygame.draw.rect(screen, self.color, (self.x - self.witdh // 2, self.y - self.height // 2, self.witdh, self.height))
        font = pygame.font.Font(None, self.height)
        surface = font.render(self.text, True, self.TextColor)
        rect = surface.get_rect(center=(self.x, self.y))
        screen.blit(surface, rect)



class TextField:
    def __init__(self, x, y,height, width, TextUp, type):
        self.x = x
        self.y = y
        self.texxt = ''
        self.iscursor = True
        self.howlong = 20
        self.TextUp = TextUp
        self.width = width
        self.height = height
        self.type = type

    def events(self,events, YesOrNo):
        for event in events:
            if event.type == pygame.KEYDOWN and YesOrNo:
                if event.key == pygame.K_BACKSPACE:
                    self.texxt = self.texxt[:-1]
                elif event.unicode not in ZnakiSpecjalne:
                    print(list(event.unicode))
                    self.texxt += event.unicode
                self.howlong = 20
                self.iscursor = True
        self.howlong -= 1
        if self.howlong == 0:
            if self.iscursor == True:
                self.iscursor = False
            else:
                self.iscursor = True
            self.howlong = 20
                
    def draw(self, screen, YesOrNO):
        DrawText(self.TextUp, black, 50 ,self.x - self.width // 2,  self.y - self.height // 2 - 40)
        pygame.draw.rect(screen, (125, 125, 125), (self.x - self.width // 2, self.y - self.height // 2, self.width, self.height))
        pygame.draw.rect(screen, black, (self.x - self.width // 2, self.y - self.height // 2, self.width, self.height), 1)
        size = DrawText(self.type(self.texxt), black, self.height, self.x - self.width // 2 + 10, self.y - self.height // 2 + 10)
        if YesOrNO and self.iscursor:
            pygame.draw.line(screen, black, ((self.x - self.width // 2) + 10 + size[0], self.y - size[1] // 2), ((self.x - self.width // 2) + 10 + size[0], self.y + size[1] // 2))

    
    def Text(texxt): return texxt
    def Password(texxt): return '*' * len(texxt)
    def Cheat(texxt): return '/' + texxt

    @property
    def text(self): return self.texxt




class TextFieldGroup:
    def __init__(self, liczba, x, y, width, height, teksty, typy): 
        self.TextsFields = []
        for i in range(liczba):
            self.TextsFields.append(TextField(x + width // 2, y + height // 2 + i * (height + 50), height, width, teksty[i], typy[i]))
        
        self.liczba = liczba
        self.ktory = 0
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.teksty = teksty
    
    def draw(self, screen):
        for i in range(self.liczba):
            self.TextsFields[i].draw(screen, self.ktory == i)
    
    def events(self, events):
        for i in range(self.liczba):
            self.TextsFields[i].events(events, self.ktory == i)
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:
                    self.ktory = (self.ktory + 1) % self.liczba
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if x > self.x and x < self.x + self.width:
                    for numberoftextfield in range(self.liczba):
                        if y > self.y + numberoftextfield * (self.height + 50)and y < self.y + (numberoftextfield + 1) * (self.height + 50):
                            self.ktory = numberoftextfield
    @property
    def texts(self):
        wynik = {}
        for i in range(self.liczba):
            wynik[self.teksty[i]] = self.TextsFields[i].text
        return wynik