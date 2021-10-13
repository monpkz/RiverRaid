import pygame
import random
from pygame.locals import *
import colores
import objetos
import lugares
import disparo

# variables globales
vel_y = 2
velocidad = 0
vidas = 1
puntos = 0
delay_y = 2
enemy_box = 96
n_enemigos = 5
mover = False
choco = False
game = False
intro = False
screen_height = 480
width, height = 800, 600
terminar = False
helice = False
# inicializacion
pygame.init()
win = pygame.display.set_mode((width, height))

# objetos
col = colores.col
base = lugares.Lugar(win, width, 8, -100)
avion = objetos.Obj(win, 370, 420, 49, 42, 0, 0, 0)
enemigos = [n_enemigos]
data_enemigos = [n_enemigos]
tiro = disparo.Disparo(win, 1, 0, 1)

for i in range(n_enemigos):
    enemigos.append(i)
    enemigos[i] = objetos.Obj(win, 0, 0, 0, 0, 0, 0, 0)
    data_enemigos.append(i)


def reiniciar():
    global puntos, vidas, mover, choco, data_enemigos

    vidas = 3
    puntos = 0
    base.y = -100
    mover = False
    avion.out = True

    for i in range(n_enemigos):
        data_enemigos[i] = [
            100, i * enemy_box - screen_height, 42, 30, 6, 1, 0
        ]
    data_enemigos[4] = [350, -96, 81, 24, 8, 0]
    data_enemigos[3] = [450, -192, 42, 30, 6, 0]
    data_enemigos[1] = [500, -384, 37, 72, 11, 0]


# funcion para verificar si la persona quiere terminar el juego
def terminar_juego():
    global game, intro, vidas

    if base.y < 238 and not game:
        intro = True
        base.y += 1
        for i in range(n_enemigos):
            enemigos[i].y += 1

    if base.y == -100 and avion.out:
        leer_pos()

    if base.y < 238 and game and intro:
        base.y += 1
        for i in range(n_enemigos):
            if enemigos[i].y > base.y + 4:
                enemigos[i].out = True
            enemigos[i].y += 1

    if avion.out and not avion.t_expl and game and vidas > 0 and not intro:
        intro = True
        avion.x = 370
        avion.ty = 0
        base.y = -100
        vidas -= 1

    if base.y == 238 and game and intro:
        avion.out = False

    for e in pygame.event.get():
        if e.type == QUIT or e.type == KEYDOWN and e.key == K_ESCAPE:
            return True
        if (e.type == KEYDOWN) and e.key == K_s:
            reiniciar()
            game = True
        if base.y == 238 and game and intro and (e.type == KEYDOWN):
            intro = False

    return False


def leer_pos():
    global game, data_enemigos
    if vidas < 0:
        game = False

    for i in range(n_enemigos):
        enemigos[i].x = data_enemigos[i][0]
        enemigos[i].y = data_enemigos[i][1]
        enemigos[i].w = data_enemigos[i][2]
        enemigos[i].h = data_enemigos[i][3]
        enemigos[i].ty = data_enemigos[i][4]
        enemigos[i].out = data_enemigos[i][5]


# funcion para determinar si hubo choque con algun color particular
def hit_color_test(obj, col):
    col = hex(col)
    col = col.lstrip('0x')
    col = tuple(
        int(col[i:i + int(6 / 3)], 16) for i in range(0, 6, int(6 / 3)))

    if obj.x >= 0 and obj.x + obj.w <= width and obj.y >= 0 and obj.y + obj.h <= height:
        for i in range(int(obj.w)):
            for j in range(int(obj.h)):
                if (not i and
                    (not j
                     or j == int(obj.h) - 1)) or not j and i == int(obj.w) - 1:
                    if win.get_at((int(obj.x + i), int(obj.y + j))) == col:
                        return True
    return False


def colisionan(a, b):
    return a.x + a.w > b.x and a.x < b.x + b.w and a.y + a.h > b.y and a.y < b.y + b.h


def hit_test():
    global choco, mover

    if (hit_color_test(avion, col[2]) or choco) and not avion.out:
        mover = False
        choco = False
        avion.out = True
        avion.t_expl = 80

    for i in range(n_enemigos):
        if enemigos[i].ty == 5 or enemigos[i].ty == 6 or enemigos[
                i].ty == 8 or enemigos[i].ty == 9:
            enemigos[i].dir = -1
        else:
            enemigos[i].dir = 1

        hit = enemigos[i].w
        enemigos[i].w = hit / 2
        if hit_color_test(enemigos[i], col[2]):
            if enemigos[i].ty == 5 or enemigos[i].ty == 6:
                enemigos[i].ty = 4
                enemigos[i].x += 2
            if enemigos[i].ty == 8:
                enemigos[i].x += 2
                enemigos[i].ty = 7

        enemigos[i].x += hit / 2
        if hit_color_test(enemigos[i], col[2]):
            if enemigos[i].ty == 4 or enemigos[i].ty == 3:
                enemigos[i].x -= 2
                enemigos[i].ty = 6
            if enemigos[i].ty == 7:
                enemigos[i].x -= 2
                enemigos[i].ty = 8
        enemigos[i].x -= hit / 2
        enemigos[i].w = hit

        if colisionan(tiro,
                      enemigos[i]) and not enemigos[i].out and tiro.y >= 0:
            enemigos[i].t_expl = 40
            enemigos[i].out = True
            tiro.y = -tiro.h

        if colisionan(
                avion,
                enemigos[i]) and enemigos[i].ty < 11 and not enemigos[i].out:
            enemigos[i].t_expl = 40
            enemigos[i].out = True
            choco = True


def check_enemigos():
    global helice

    helice = not helice

    hit_test()

    for i in range(n_enemigos):
        if helice and enemigos[i].ty == 3 or enemigos[i].ty == 5:
            enemigos[i].ty += 1
        elif enemigos[i].ty == 4 or enemigos[i].ty == 6:
            enemigos[i].ty -= 1

        if game and not intro:
            enemigos[i].y += mover * vel_y

            if 2 < enemigos[i].ty < 9 and enemigos[i].y > 200 and not enemigos[
                    i].out:
                enemigos[i].x += enemigos[i].dir

            if enemigos[i].ty == 10 or enemigos[i].ty == 9:
                if enemigos[i].x > width and enemigos[i].ty == 10:
                    enemigos[i].x = 0
                if enemigos[i].x < 0 and enemigos[i].ty == 9:
                    enemigos[i].x = width
                if not enemigos[i].out and not avion.out:
                    enemigos[i].x += enemigos[i].dir

            if enemigos[i].y == screen_height - enemy_box / 3:
                enemigos[i].y = 0
                if base.y < enemigos[i].y < base.y + 400:
                    enemigos[i].out = True
                else:
                    enemigos[i].out = False

                tipos_enemigos = [4, 6, 7, 8, 9, 10, 11]
                rnd = random.randint(0, 6)
                enemigos[i].ty = tipos_enemigos[rnd]
                if rnd == 0 or rnd == 1:
                    enemigos[i].w = 42
                    enemigos[i].h = 30
                elif rnd == 2 or rnd == 3:
                    enemigos[i].w = 81
                    enemigos[i].h = 24
                elif rnd == 4 or rnd == 5:
                    enemigos[i].w = 48
                    enemigos[i].h = 18
                elif rnd == 6:
                    enemigos[i].w = 37
                    enemigos[i].h = 72

                pos = True
                while pos:
                    enemigos[i].x = random.randint(0, 8) * 84 + 23
                    pos = hit_color_test(enemigos[i], col[2])

                enemigos[i].y = -enemy_box / 3

        enemigos[i].mostrar()


def pintar():
    pygame.display.update()
    # agua
    win.fill(col[3])

    # verificando los controles
    if not avion.out and not intro:
        control()

    tiro.show(avion.x + avion.w / 2, avion.y + avion.h / 2)

    # fondo
    win.fill(col[2], rect=[0, 0, 20, height])
    win.fill(col[2], rect=[width - 20, 0, 20, height])

    if -screen_height < base.y < screen_height:
        base.show()

        # mover a base
        base.y += mover * vel_y

    check_enemigos()
    avion.mostrar()

    # panel
    win.fill(col[7], rect=[0, screen_height, width, 130])
    win.fill(col[14], rect=[0, height - 117, width, 112])

    # medidor
    pygame.draw.rect(win, col[7], [320, 515, 204, 44], 4)
    pygame.draw.rect(win, col[7], [335, 515, 11, 13])
    pygame.draw.rect(win, col[7], [422, 515, 5, 13])
    pygame.draw.rect(win, col[7], [500, 515, 11, 13])


def control():
    global delay_y, velocidad, mover

    if game and not intro:
        velocidad += 1
        if velocidad > delay_y:
            mover = True
            velocidad = 0
        else:
            mover = False

    # movimiento del avion
    avion.ty = 0
    key = pygame.key.get_pressed()
    if key[K_LEFT] and avion.x > 10:
        avion.x -= 1
        avion.ty = 2
    if key[K_RIGHT] and avion.x < 734:
        avion.x += 1
        avion.ty = 1

    if key[K_SPACE]:
        tiro.shoting = True


reiniciar()

while not terminar:
    pintar()
    terminar = terminar_juego()
