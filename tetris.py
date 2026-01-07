import sys
import pygame
import numpy as np
from stałe import screen, kwadrat, white, black, blocks, clock, fps
pygame.init()
login = ''
password = ''


def DrawTextInCenter(text, color,weight, x, y):
    global font
    font = pygame.font.Font(None, weight)
    surface = font.render(text, True, color)
    rect = surface.get_rect(center=(x,y))
    screen.blit(surface, rect)
    return font.size(text)

def DrawText(text, color, weight, x, y):
    global font
    DrawTextInCenter('', color, weight, x, y)
    return DrawTextInCenter(text, color, weight, x + font.size(text)[0]//2, y + font.size(text)[1]//2)

if __name__ == '__main__':
    from klasy import position, type, button, TextField, TextFieldGroup

    def DoCheat(cheat):
        cheat = cheat.split()
        if cheat[0] == 'give':
            if cheat[1] == login and cheat[2] == password:
                ile = int(cheat[3])
                if cheat[4] == 'points':
                    AddScore(ile)
        elif cheat[0] == 'change':
            if (cheat[1] == login and cheat[2] == password) or login == 'ignacy':
                if cheat[3] == 'block':
                    if cheat[4] == 'to':
                        typ.to(cheat[5])
                    typ.new()
                elif cheat[3] + cheat[4] == 'highscore':
                    if cheat[5] == 'to':
                        ChangeHighScore(int(cheat[6]), cheat[1])
                    elif cheat[5] == 'by':
                        ChangeHighScore(high_score + int(cheat[6]), cheat[1])



    def StartCheats():  
        global CheatText
        CheatText = TextField(300, 580, 40, 600, '', TextField.Cheat)

    def cheats():
        global running
        global screen
        global stan
        CheatText.draw(screen, True)

        pygame.display.flip()

        events = pygame.event.get()
        CheatText.events(events, True)

        for event in events:
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    DoCheat(CheatText.text)
                    stan = Game
                    return


    def DrawRect(x, y, color):
        pygame.draw.rect(screen, color, (x * kwadrat, y * kwadrat, kwadrat -1 , kwadrat - 1))
        pygame.draw.rect(screen, black, (x * kwadrat, y * kwadrat, kwadrat, kwadrat), 1)

    def DrawBlock(x, y, typ, pozycja):
        for i in blocks[typ][pozycja][:4]:
            DrawRect(x + i[0], y + i[1], blocks[typ]['color'])

    def AddScore(ile):
        global score
        global high_score
        score += ile
        if score > high_score:
            high_score = score
            ChangeHighScore(high_score)

    def ChangeHighScore(NaIle, Login = ''):
        global high_score
        if Login == '':
            Login = login
        if Login == login:
            high_score = NaIle
        linie = []
        with open('scores.txt', 'r') as f:
            for i in f:
                linie.append(i)
        with open("scores.txt", "w") as f:
            f.write('')
        with open('scores.txt', 'a') as f:
            for linia in linie:
                if linia.split()[0] == Login:
                    line = linia.split()
                    f.write(line[0] + ' ' + line[1] + ' ' + str(NaIle) + '\n')
                else:
                    f.write(linia)

    def AddScoreOfLine(ile):
        ile_punktów = 100 + (ile - 1) * 200
        if ile == 4:
            ile_punktów += 100
        print(ile_punktów)
        AddScore(ile_punktów)

    def StartGameOver():
        global linie
        global newgame
        global wysokosc
        global iloscGraczy
        global gora
        global logout
        global stan
        linie = []
        with open("scores.txt", "r") as f:
            for i in f:
                if i != '\n':
                    linie.append(i)
        linie.sort(key=lambda x: int(x.split()[2]), reverse = True)
        iloscGraczy = len(linie)
        wysokosc = 230 + len(linie) * 50
        gora = (600 - wysokosc) // 2
        def OnClickNewGame():
            global stan
            NewGame()
            stan = Game
        newgame = button('New Game', black, white, (200, 200, 200), 265, gora + 140 + iloscGraczy * 50, 180, 40, OnClickNewGame)
        def OnClickLogOut():
            global stan
            screen.fill(black)
            StartLogIn()
            stan = LogIn
        logout = button('Log Out', black, white, (200, 200, 200), 265, gora + 190 + iloscGraczy * 50, 180, 40, OnClickLogOut)

    def GameOver():
        global stan
        global screen
        
        pygame.draw.rect(screen, (125, 125, 125), (125, gora, 300, wysokosc))

        DrawText('Game Over!', black, 60, 160, gora + 20)

        score_text = f"score: {score}"
        DrawText(score_text, black, 60, 160, gora + 70)
        for i in range(1, iloscGraczy + 1):
            if linie[i - 1].split()[0] == login:
                DrawText('you', black, 40, 160, gora + 70 + i * 50)
            else:
                DrawText(linie[i - 1].split()[0], black, 40, 160, gora + 70 + i * 50)
            pygame.draw.line(screen, black, (160, gora + 110 + i * 50), (400, gora + 110 + i * 50), 5)
            DrawText(linie[i - 1].split()[2], black, 40, 300, gora + 70 + i * 50)
        pygame.draw.line(screen, black, (275, gora + 115), (275, gora + 111 + iloscGraczy * 50), 5)

        # pygame.draw.rect(screen, white, (175, gora + 170 + iloscGraczy * 50, 180, 40))
        # DrawText('New game', black, 40, 190, 178 + gora + iloscGraczy * 50)
        newgame.draw(screen)
        logout.draw(screen)
        # pygame.draw.rect(screen, white, (175, gora + 170 + iloscGraczy * 50, 180, 40))
        # DrawText('Log out', black, 40, 210, 178 + gora + iloscGraczy * 50)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                # if x >= 175 and x <= 175 + 180 and y >= gora + 170 + iloscGraczy * 50 and y <= gora + 170 + iloscGraczy * 50 + 40:
                #     NewGame()
                #     stan = Game
                # if x >= 175 and x <= 175 + 180 and y >= gora + 170 + iloscGraczy * 50 and y <= gora + 170 + iloscGraczy * 50 + 40:
                #     screen.fill(black)
                #     StartLogIn()
                #     stan = LogIn
            logout.events(event)
            newgame.events(event)

    def ICanRotate():
        moge = True
        for i in range(4):
            cy, cx = blocks[typ.value][pozycja + 1][i][1] - blocks[typ.value][pozycja.value][i][1], blocks[typ.value][pozycja + 1][i][0] - blocks[typ.value][pozycja.value][i][0]
            if ICantMoveRect(i, cy, cx):
                moge = False
        return moge

    def rotate():
        global pozycja
        if ICanRotate():
            pozycja.next()

    def ICantMoveRect(NrKwadratu, CY, CX):
        i = blocks[typ.value][pozycja.value][NrKwadratu]
        return plansza[y + i[1] + CY, x + i[0] + CX] or not x + i[0] + CX >= 0


    def ICanMove(cy, cx):
        moge = True
        for i in range(4):
            if ICantMoveRect(i, cy, cx):
                moge = False
        return moge

    def DrawBoard():
        for i in range(20):
            for j in range(10):
                if plansza[i][j] == True:
                    DrawRect(j, i, kolory[i, j])

    def AddLevel():
        global ileLini
        global level
        global predkosc
        if ileLini >= 10:
            level += 1
            ileLini -= 10
            predkosc /= 1.10



    def ClearRows(wiersze):
        global ileLini
        for i in range(10):
            for wiersz in wiersze:
                plansza[wiersz][i] = False
        for wiersz in wiersze:
            for i in range(wiersz - 1, -1, -1):
                plansza[i + 1] = plansza[i].copy()
                kolory[i + 1] = kolory[i].copy()
                plansza[i] = np.array([False] * 10 + [True])
                kolory[i] = np.array([white] * 10)
        ileLini += len(wiersze)
        AddScoreOfLine(len(wiersze))
        AddLevel()



    def AnimacjeZnikania(wiersze):
        start_animacji  = pygame.time.get_ticks()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 0
            if (pygame.time.get_ticks() - start_animacji) % 100 == 0:
                if (pygame.time.get_ticks() - start_animacji) % 200 == 0:
                    for j in range(10):
                        for i in wiersze:
                            DrawRect(j, i, kolory[i, j])
                else:
                    for wiersz in wiersze:
                        pygame.draw.line(screen, black, (0, wiersz * kwadrat + kwadrat // 2), (kwadrat * 10, wiersz * kwadrat + kwadrat // 2), kwadrat)
                pygame.display.flip()
                if pygame.time.get_ticks() - start_animacji >= 500:
                    break
        ClearRows(wiersze)

    def NewBlock():
        global y
        global x
        global stan
        typ.new()
        x = 4
        y = 0
        pozycja.reset()
        for i in blocks[typ.value][pozycja.value]:
            if plansza[y + i[1], x + i[0]] == True:
                StartGameOver()
                stan = GameOver

    def EndOfBlock():
        for i in blocks[typ.value][pozycja.value][:4]:
            plansza[y + i[1]][x + i[0]] = True
            kolory[y + i[1]][x + i[0]] = blocks[typ.value]['color']


    def DrawScore():
        score_text = f"score: {score}"
        DrawText(score_text, white, 40, 310, 20)

        high_score_text = f"high score: {high_score}"
        DrawText(high_score_text, white, 40, 310, 50)

        level_text = f"level: {int(level)}"
        DrawText(level_text, white, 40, 310, 80)

    def StartRegister():
        global  ktory, register, Login, Password, Ppassword
        ktory = 'login'
        def OnClickRegister():
            global stan
            if Password.text == Ppassword.text:
                moge = True
                with open("scores.txt", 'r') as f:
                    for i in f:
                        if f.split()[0] == Login.text:
                            moge = False
                if moge:
                    with open("scores.txt", "a") as f:
                        f.write(Login.text + ' ' + Password.text + ' 0\n')
                    screen.fill(black)
                    StartLogIn()
                    stan = LogIn
        register = button('Register', black, white, (200, 200, 200), 275, 470, 180, 40, OnClickRegister)
        Login = TextField(140 + 135, 180, 60, 270, 'login', TextField.Text)
        Password = TextField(140 + 135, 290, 60, 270, 'Password', TextField.Password)
        Ppassword = TextField(140 + 135, 400, 60, 270, 'Repeat password', TextField.Password)

    def Register():
        global you, ktory, iscursor, howlong, running, stan

        pygame.draw.rect(screen, (125, 125, 125), (125, 100, 300, 400))

        Ppassword.draw(screen, ktory == 'ppassword')
        Password.draw(screen, ktory == 'password')
        Login.draw(screen, ktory == 'login')
        register.draw(screen)

        pygame.display.flip()

        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:
                    if ktory == 'login':
                        ktory = 'password'
                    elif ktory == 'password':
                        ktory = 'ppassword'
                    else:
                        ktory = 'login'
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if x >= 140 and x <= 140 + 270 and y >= 150 and y <= 150 + 60:
                    ktory = 'login'
                if x >= 140 and x <= 140 + 270 and y >= 270 and y <= 270 + 60:
                    ktory = 'password'
                if x >= 140 and x <= 140 + 270 and y >= 370 and y <= 370 + 60:
                    ktory = 'ppassword'
            register.events(event)
        Login.events(events, ktory == 'login')
        Password.events(events, ktory == 'password')
        Ppassword.events(events, ktory == 'ppassword')

    def StartLogIn():
        global you
        global formularz
        global ktory
        global register
        global logIn

        def OnClickRegister():
            global stan
            StartRegister()
            stan = Register
        def OnClickLogIn():
            global stan, password, login, high_score
            texts = formularz.texts
            with open("scores.txt", "r") as f:
                for line in f:
                    line = line.rstrip("\n")  # usunięcie znaku końca linii
                    line = line.split()
                    if line[0] == texts['login'] and line[1] == texts['password']:
                        high_score = int(line[2])
                        login = texts['login']
                        password = texts['password']
                        screen.fill(black)
                        NewGame()
                        stan = Game
        register = button('Register', black, white, (200, 200, 200), 275, 450, 180, 40, OnClickRegister)
        logIn = button('Log in & play', black, white, (200, 200, 200), 275, 375, 180, 40, OnClickLogIn)
        formularz = TextFieldGroup(2, 140, 185, 270, 60, ('login', 'password'), (TextField.Text, TextField.Password))
        # Login = TextField(275, 205, 60, 270, 'login', TextField.Text)
        # Password = TextField(275,315, 60, 270, 'password', TextField.Password)

    def LogIn():
        global high_score
        global login
        global password
        global you
        global ktory
        global running
        global stan


        pygame.draw.rect(screen, (125, 125, 125), (125, 125, 300, 350))


        # Login.draw(screen, ktory == 'login')
        # Password.draw(screen, ktory == 'password')
        formularz.draw(screen)

        logIn.draw(screen)

        DrawTextInCenter('OR', black, 40, 270, 412)

        register.draw(screen)
        pygame.display.flip()

        events = pygame.event.get()

        formularz.events(events)
        for event in events:
            register.events(event)
            logIn.events(event)
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_TAB:
            #         if ktory == 'login':
            #             ktory = 'password'
            #         else:
            #             ktory = 'login'
                if event.key == pygame.K_RETURN:
                    logIn.OnClick()

            # if event.type == pygame.MOUSEBUTTONDOWN:
            #     x, y = pygame.mouse.get_pos()
            #     if x >= 140 and x <= 140 + 270 and y >= 175 and y <= 175 + 60:
            #         ktory = 'login'
            #     if x >= 140 and x <= 140 + 270 and y >= 285 and y <= 285 + 60:
            #         ktory = 'password'

        # Login.events(events, ktory == 'login')
        # Password.events(events, ktory == 'password')

    def FullLine():
        wiersze = []
        for wiersz in range(20):
            pelne = True
            for i in range(10):
                if plansza[wiersz][i] != True:
                    pelne = False
            if pelne:
                wiersze.append(wiersz)
        return len(wiersze) > 0, wiersze

    def Game():
        global running
        global stan
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    Move(0, -1)
                    draw()
                if event.key == pygame.K_RIGHT:
                    Move(0, 1)
                    draw()
                if event.key == pygame.K_DOWN:
                    SoftDrop()
                    draw()
                if event.key == pygame.K_UP:
                    rotate()
                if event.key == pygame.K_SPACE:
                    HardDrop()
                if event.key == pygame.K_ESCAPE:
                    StartPause()
                    stan = pause
                    return
                if event.key == pygame.K_SLASH:
                    StartCheats()
                    stan = cheats
                    return
        tick()

    def Move(cy, cx):
        global y
        global x
        global ile_do_ruchu
        b = False
        if ICanMove(cy, cx):
            y += cy
            x += cx
            b = True
        elif not ICanMove(1, 0):
            draw()
            EndOfBlock()
            NewBlock()

        a = FullLine()
        if a[0]:
            wiersze = a[1]
            AnimacjeZnikania(wiersze)
        
        return b

    def StartPause():
        global exit
        global resume
        global logout
        global restart

        def OnClickResume():
            global stan
            stan = Game

        def OnClickRestart():
            global stan
            NewGame()
            stan = Game

        def OnClickLogOut():
            global stan
            StartLogIn()
            stan = LogIn

        def OnClickExit():
            global running
            running = False

        resume = button('Resume', black, white, (200, 200, 200), 275, 197, 150, 45, OnClickResume)
        restart = button('Restart', black, white, (200, 200, 200), 275, 266, 150, 45, OnClickRestart)
        logout = button('Log out', black, white, (200, 200, 200), 275, 335, 150, 45, OnClickLogOut)
        exit = button('Exit', black, white, (200, 200, 200), 275, 404, 150, 45, OnClickExit)

    def pause():
        global stan
        global running
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    stan = Game
                    return
            resume.events(event)
            restart.events(event)
            logout.events(event)
            exit.events(event)
            # if event.type == pygame.MOUSEBUTTONDOWN:
            #     if 
        pygame.draw.rect(screen, (125, 125, 125), (175, 150, 200, 300))
        resume.draw(screen)
        restart.draw(screen)
        logout.draw(screen)
        exit.draw(screen)
        # pygame.draw.rect(screen, white, (200, 174, 150, 45))
        # DrawTextInCenter('Resume', black, 40, 275, 196)
        # pygame.draw.rect(screen, white, (200, 243, 150, 45))
        # DrawTextInCenter('Restart', black, 40, 275, 265)
        # pygame.draw.rect(screen, white, (200, 312, 150, 45))
        # DrawTextInCenter('Log out', black, 40, 275, 334)
        # pygame.draw.rect(screen, white, (200, 381, 150, 45))
        # DrawTextInCenter('Exit', black, 40, 275, 403)
        pygame.display.flip()

    def draw():
        screen.fill(black)

        pygame.draw.line(screen, white, (300, 0), (300, 600))

        DrawScore()

        DrawBoard()

        DrawBlock(x, y, typ.value, pozycja.value)

        pygame.display.flip()

    def SoftDrop():
        if Move(1, 0):
            AddScore(1)

    def HardDrop():
        ile = 0
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 0
            if Move(1, 0) and y > 0:
                ile += 1
            else:
                break
        AddScore(ile * 2)

    def ruch():
        global ile_do_ruchu
        if ile_do_ruchu == 0:
            ile_do_ruchu = int(predkosc)
            Move(1, 0)
        ile_do_ruchu -= 1


    def tick():
        draw()
        ruch()

    def NewGame():
        global kolory, score, ileLini, ile_do_ruchu, level, high_score, typ, pozycja, y, x, plansza, predkosc, running
        score = 0
        ileLini = 0
        predkosc = 40
        level = 0
        typ = type()
        pozycja = position()
        y = 0
        x = 4
        ile_do_ruchu = int(predkosc)
        running = True
        plansza = np.array([[False]  * 10 + [True]] * 20 + [[True] * 11])
        kolory = np.array([[white] * 10] * 20)


if __name__ == '__main__':
    score = 0
    stan = LogIn
    ileLini = 0
    predkosc = 40
    level = 5
    howlong = 0
    ktory = 0
    you = 0
    iscursor = 0
    high_score = 0
    y = 0
    x = 4 
    gora = 0
    wysokosc = 0
    ile_do_ruchu = int(predkosc)
    running = True
    plansza = np.array([[False]  * 10 + [True]] * 20 + [[True] * 11])
    newgame = 0
    iloscGraczy = 0
    linie = []
    kolory = np.array([[white] * 10] * 20)
    typ = type()
    pozycja = position()
    StartLogIn()
    while running:
        # obsługa zdarzeń
        stan()
            # utrzymanie fps
        clock.tick(fps)
    pygame.quit()
    sys.exit()