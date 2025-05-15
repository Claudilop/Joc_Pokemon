import random
import time
from pygame.locals import *
import pygame

# Tamany finestra
VIEW_WIDTH = 1024
VIEW_HEIGHT = 900

# pantalla
# pantalla 1 = Menu
# pantalla 2 = credits
# pantalla 3 = Joc
# pantalla 4 = Game over
pantalla_actual = 1
pokemon = -1

WHITE = (255, 255, 255)
MAGENTA = (207, 52, 118)
MARRON = (128, 64, 0)

tortuga_vida = 100
pokemon_vida = 100

torn_tortuga = True  # Alterna torns

castor_image = pygame.image.load('assets1/castor.png')
shark_image = pygame.image.load('assets1/tiburon.png')
delfin_image = pygame.image.load('assets1/delfin.png')
pirana_image = pygame.image.load('assets1/pirana.png')
escarabajo_image = pygame.image.load('assets1/escarabajo.png')
tortuga_image = pygame.image.load('assets1/tortuga.png')

# iniciem pygame3
pygame.init()

pygame.mixer.music.load('assets1/musica.mp3')
pygame.mixer.music.play(-1)  # -1 fa que soni en bucle
pygame.mixer.music.set_volume(0.3)

pantalla = pygame.display.set_mode((VIEW_WIDTH, VIEW_HEIGHT))
pygame.display.set_caption("Arcade")

# Carreguem imatge de fons
background_image = 'assets1/fons.png'
background_width = pygame.image.load(background_image).convert().get_width()
background_height = pygame.image.load(background_image).convert().get_height()

# Límits per moure el fons enlloc del personatge
MARGIN_X, MARGIN_Y = VIEW_WIDTH // 2, VIEW_HEIGHT // 2

# Carreguem imatge inicial personatge
player_image = pygame.image.load('assets1/down0.png')
protagonist_speed = 8

# Posicions inicials del personatge i del fons
player_rect = player_image.get_rect(midbottom=(VIEW_WIDTH // 2, VIEW_HEIGHT // 2))
bg_x, bg_y = 0, 0

# Control de FPS
clock = pygame.time.Clock()
fps = 30

# Control de l'animació del personatge
# 1 up. 2 down. 3 right. 4 left
sprite_direction = "down"
sprite_index = 0
animation_protagonist_speed = 200
sprite_frame_number = 1
last_change_frame_time = 0
idle = False

# rectangles
rectangle1 = pygame.draw.rect(pantalla, (0, 0, 0), (bg_x + 250, bg_y + 370, 60, 60))  # escarbat?
rectangle2 = pygame.draw.rect(pantalla, (0, 0, 0), (bg_x + 670, bg_y + 355, 60, 60))
rectangle3 = pygame.draw.rect(pantalla, (0, 0, 0), (bg_x + 140, bg_y + 790, 70, 60))
rectangle4 = pygame.draw.rect(pantalla, (0, 0, 0), (bg_x + 120, bg_y + 170, 70, 60))
rectangle5 = pygame.draw.rect(pantalla, (0, 0, 0), (bg_x + 920, bg_y + 630, 70, 60))

tots_els_rectangles = [rectangle1, rectangle2, rectangle3, rectangle4, rectangle5]

enemics_derrotats = [False, False, False, False, False]  # Un per cada rectangle

def imprimir_pantalla_fons(image, x, y):
    # Imprimeixo imatge de fons:
    background = pygame.image.load(image).convert()
    pantalla.blit(background, (x, y))


def mostrar_menu():
    # mostrar imatge de fons del menu
    imprimir_pantalla_fons('assets1/inici.png', 0, 0)
    font1 = pygame.font.SysFont(None, 100)
    font2 = pygame.font.SysFont(None, 80)
    img1 = font1.render("SAFARI ZONE", True, (255, 0, 0))

    pantalla.blit(img1, (250, 30))


def mostrar_credits():
    imprimir_pantalla_fons('assets1/creditos.png', 0, 0)
    font1 = pygame.font.SysFont(None, 100)
    font2 = pygame.font.SysFont(None, 80)
    img1 = font1.render("SAFARI ZONE", True, MAGENTA)
    img2 = font2.render("Programacio: Claudi ", True, MARRON)
    img3 = font2.render("Grafics: Claudi i Felipe", True, MARRON)
    img4 = font2.render("Musica: Pixabay", True, MARRON)

    pantalla.blit(img1, (250, 30))
    pantalla.blit(img2, (40, 130))
    pantalla.blit(img3, (40, 230))
    pantalla.blit(img4, (40, 330))


def mostrar_pelea(num_pokemon):
    global tortuga_vida, pokemon_vida, torn_tortuga, pantalla_actual
    p = 4

    imprimir_pantalla_fons('assets1/pelea.png', 0, 0)

    # Mostrem el Pokémon enemic
    if num_pokemon == 1:
        pantalla.blit(pygame.transform.scale(escarabajo_image, (250, 250)), (550, 200))
    elif num_pokemon == 2:
        pantalla.blit(pygame.transform.scale(castor_image, (250, 250)), (600, 250))
    elif num_pokemon == 3:
        pantalla.blit(pygame.transform.scale(pirana_image, (250, 250)), (550, 100))
    elif num_pokemon == 4:
        pantalla.blit(pygame.transform.scale(delfin_image, (300, 300)), (580, 80))
    elif num_pokemon == 5:
        pantalla.blit(pygame.transform.scale(shark_image, (250, 250)), (580, 200))

    # Mostrem la tortuga (jugador)
    pantalla.blit(pygame.transform.scale(tortuga_image, (650, 650)), (90, 600))

    # Barres de vida
    dibuixar_barra_vida(100, 70, tortuga_vida, 100)
    dibuixar_barra_vida(750, 70, pokemon_vida, 100)

    # Noms
    font = pygame.font.SysFont(None, 40)
    pantalla.blit(font.render("TORTUGA", True, (255, 255, 255)), (100, 40))
    pantalla.blit(font.render("ENEMIC", True, (255, 255, 255)), (750, 40))

    # Diàleg a baix (tipus Pokémon)
    pygame.draw.rect(pantalla, (255, 255, 255), (50, 750, 920, 120))
    pygame.draw.rect(pantalla, (0, 0, 0), (50, 750, 920, 120), 4)

    if pokemon_vida <= 0:
        text = "Has guanyat! pressiona espai."

    elif tortuga_vida <= 0:
        text = "Has perdut! pressiona espai."
    else:
        text = "Prem 'A' per atacar!"

    pantalla.blit(font.render(text, True, (0, 0, 0)), (70, 780))
    # Control d'atacs a la batalla
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == KEYDOWN:
            if event.key == K_a:
                if torn_tortuga:
                    if pokemon_vida > 0 and tortuga_vida > 0:
                        pokemon_vida -= random.randint(10, 20)
                else:
                    if pokemon_vida > 0 and tortuga_vida > 0:
                        tortuga_vida -= random.randint(10, 15)
                torn_tortuga = not torn_tortuga
            if event.key == K_SPACE:
                print("espai")
                if tortuga_vida <= 0:
                    p = 1
                if pokemon_vida <= 0:
                    p = 3
    return p


def dibuixar_barra_vida(x, y, vida_actual, vida_maxima, ample=200, alt=20):
    percentatge = max(vida_actual / vida_maxima, 0)
    llargada = int(ample * percentatge)
    color = (0, 255, 0) if percentatge > 0.5 else (255, 255, 0) if percentatge > 0.2 else (255, 0, 0)

    # Marc de la barra
    pygame.draw.rect(pantalla, (0, 0, 0), (x - 2, y - 2, ample + 4, alt + 4))
    # Fons de la barra
    pygame.draw.rect(pantalla, (100, 100, 100), (x, y, ample, alt))
    # Vida actual
    pygame.draw.rect(pantalla, color, (x, y, llargada, alt))


def pantalla_inicial():
    imprimir_pantalla_fons('assets1/logo.png', 0, 0)
    pygame.display.update()
    pygame.time.delay(2000)


pantalla_inicial()

while True:
    current_time = pygame.time.get_ticks()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    if pantalla_actual == 1:
        mostrar_menu()
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_1:
                    pantalla_actual = 3
                if event.key == K_2:
                    pantalla_actual = 2
                if event.key == K_3:
                    pygame.quit()

    if pantalla_actual == 2:
        mostrar_credits()
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    pantalla_actual = 1

    if pantalla_actual == 3:
        # Moviment del jugador
        idle = True
        keys = pygame.key.get_pressed()
        if keys[K_UP]:
            idle = False
            sprite_direction = "up"
            if player_rect.y > MARGIN_Y or bg_y >= 0:
                player_rect.y = max(player_rect.y - protagonist_speed, player_rect.height // 2)
            else:
                bg_y = min(bg_y + protagonist_speed, 0)

        if keys[K_DOWN]:
            idle = False
            sprite_direction = "down"
            if player_rect.y < VIEW_HEIGHT - MARGIN_Y or bg_y <= VIEW_HEIGHT - background_height:
                player_rect.y = min(player_rect.y + protagonist_speed, VIEW_HEIGHT - player_rect.height // 2)
            else:
                bg_y = max(bg_y - protagonist_speed, VIEW_HEIGHT - background_height)
        if keys[K_RIGHT]:
            idle = False
            sprite_direction = "right"
            if player_rect.x < VIEW_WIDTH - MARGIN_X or bg_x <= VIEW_WIDTH - background_width:
                player_rect.x = min(player_rect.x + protagonist_speed, VIEW_WIDTH - player_rect.width // 2)
            else:
                bg_x = max(bg_x - protagonist_speed, VIEW_WIDTH - background_width)

        if keys[K_LEFT]:
            idle = False
            sprite_direction = "left"
            if player_rect.x > MARGIN_X or bg_x >= 0:
                player_rect.x = max(player_rect.x - protagonist_speed, player_rect.width // 2)
            else:
                bg_x = min(bg_x + protagonist_speed, 0)

        # Dibuixar el fons
        imprimir_pantalla_fons(background_image, bg_x, bg_y)

        contador = 0
        for obstacle in tots_els_rectangles:
            contador += 1
            if player_rect.colliderect(obstacle) and not enemics_derrotats[contador - 1]:
                pokemon = contador
                pantalla_actual = 4
                break

        # frame number: (there are 3 frames only)
        # selccionem la imatge a mostrar
        if not idle:
            if current_time - last_change_frame_time >= animation_protagonist_speed:
                last_change_frame_time = current_time
                sprite_index = sprite_index + 1
                sprite_index = sprite_index % sprite_frame_number
        else:
            sprite_index = 0
        # dibuixar el jugador
        player_image = pygame.image.load('assets1/' + sprite_direction + str(sprite_index) + '.png')
        pantalla.blit(player_image, player_rect)

        if not enemics_derrotats[1]:
            castor_image = pygame.transform.scale(castor_image, (128, 128))
            pantalla.blit(castor_image, (650, 350))

        if not enemics_derrotats[4]:
            shark_image = pygame.transform.scale(shark_image, (128, 128))
            pantalla.blit(shark_image, (900, 600))

        if not enemics_derrotats[3]:
            delfin_image = pygame.transform.scale(delfin_image, (128, 128))
            pantalla.blit(delfin_image, (100, 100))

        if not enemics_derrotats[2]:
            pirana_image = pygame.transform.scale(pirana_image, (128, 128))
            pantalla.blit(pirana_image, (100, 700))

        if not enemics_derrotats[0]:
            escarabajo_image = pygame.transform.scale(escarabajo_image, (128, 128))
            pantalla.blit(escarabajo_image, (200, 350))

        if all(enemics_derrotats):
            pantalla_actual = 5

        # mantenir el jugador dins la finestra

        player_rect.clamp_ip(pantalla.get_rect())
    #
    #    pygame.draw.rect(pantalla,(255,255,0),(bg_x+350,bg_y+10,100,100))

    if pantalla_actual == 4:
        p = mostrar_pelea(pokemon)
        if p == 3:  # Guanyat
            if not enemics_derrotats[pokemon - 1]:  # marques que està derrotat
                enemics_derrotats[pokemon - 1] = True
            # Reiniciar vides per a la pròxima batalla
            tortuga_vida = 100
            pokemon_vida = 100
            torn_tortuga = True
            player_rect = player_image.get_rect(midbottom=(VIEW_WIDTH // 2, VIEW_HEIGHT // 2))
            pantalla.blit(player_image, player_rect)
            pantalla_actual = 3
        if p == 1:  # Perdut
            # Reiniciar vides
            tortuga_vida = 100
            pokemon_vida = 100
            torn_tortuga = True
            player_rect = player_image.get_rect(midbottom=(VIEW_WIDTH // 2, VIEW_HEIGHT // 2))
            pantalla.blit(player_image, player_rect)
            pantalla_actual = 1

    if pantalla_actual == 5:
        imprimir_pantalla_fons('assets1/game_over.png', 0, 0)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == KEYDOWN and event.key == K_SPACE:
                pantalla_actual = 1
                enemics_derrotats = [False] * 5

    pygame.display.update()
    clock.tick(fps)

