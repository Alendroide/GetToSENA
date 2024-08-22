import pygame
from sys import exit
from random import randint

def display_score():
    current_time = (pygame.time.get_ticks() - start_time)//1000
    score_surf = font.render(f"Puntos: {current_time}",False,"Black")
    score_rect = score_surf.get_rect(topleft = (30,30))
    screen.blit(score_surf,score_rect)
    return current_time

def obstacle_movement(obstacle_list):
    global vel_enemies
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= vel_enemies
            if obstacle_rect.bottom == 330:
                screen.blit(rat_surf,obstacle_rect)
            else:
                screen.blit(dengue_surf,obstacle_rect)

        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]
        return obstacle_list
    else: return []

def collisions(player,obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect): return False
    return True

def player_animation():
    global player_surf, player_index, player_xspeed, player_walk_index,player_walki_index
    if player_rect.bottom < 330:
        if player_xspeed > 0:
            player_surf = player_jump
        elif player_xspeed < 0:
            player_surf = pygame.transform.flip(player_jump,True,False)
        else:
            player_surf = player_jump
    else:
        if player_xspeed == 0:
            player_index += 0.02
            if player_index >= len(player_idle):
                player_index = 0
            player_surf = player_idle[int(player_index)]
        elif player_xspeed > 0:
            player_walk_index += 0.2
            if player_walk_index >= len(player_walk):
                player_walk_index = 0
            player_surf = player_walk[int(player_walk_index)]
        elif player_xspeed < 0:
            player_walki_index += 0.2
            if player_walki_index >= len(player_walki):
                player_walki_index = 0
            player_surf = player_walki[int(player_walki_index)]

pygame.init()

screen = pygame.display.set_mode((720,480))
pygame.display.set_caption("Llega al SENA!")
#contador de iteraciones
clock = pygame.time.Clock()

font = pygame.font.Font("font/Minecraft.ttf",40)
#Cielo
sky = pygame.image.load("images/bg/sky.png").convert()
sky_rect = sky.get_rect(topleft=(0,0))
#Suelo
ground = pygame.image.load("images/bg/ground.png").convert()
ground_rect = ground.get_rect(topleft=(0,300))

#rat
rat_frame1 = pygame.image.load("images/enemies/rat1.png").convert_alpha()
rat_frame2 = pygame.image.load("images/enemies/rat2.png").convert_alpha()
rat_frame3 = pygame.image.load("images/enemies/rat3.png").convert_alpha()
rat_frames = [rat_frame1,rat_frame2,rat_frame3,rat_frame2]
rat_index = 0
rat_surf = rat_frames[rat_index]

#dengue
dengue_frame1 = pygame.image.load("images/enemies/dengue_x1.png").convert_alpha()
dengue_frame2 = pygame.image.load("images/enemies/dengue_x1_2.png").convert_alpha()
dengue_frames = [dengue_frame1,dengue_frame2]
dengue_index = 0
dengue_surf = dengue_frames[dengue_index]

#lista de enemigos
obstacle_rect_list = []

#player
player_idle_1 = pygame.image.load("images/player/player1.png").convert_alpha()
player_idle_2 = pygame.image.load("images/player/player2.png").convert_alpha()
player_idle = [player_idle_1,player_idle_2]
player_index = 0

player_walk_1 = pygame.image.load("images/player/player_walk.png").convert_alpha()
player_walk_2 = pygame.image.load("images/player/player_walk2.png").convert_alpha()
player_walk_3 = pygame.image.load("images/player/player_walk3.png").convert_alpha()
player_walk_4 = pygame.image.load("images/player/player_walk4.png").convert_alpha()
player_walk = [player_walk_1,player_walk_2,player_walk_3,player_walk_4]
player_walk_index = 0

player_walki_1 = pygame.transform.flip(pygame.image.load("images/player/player_walk.png").convert_alpha(),True,False)
player_walki_2 = pygame.transform.flip(pygame.image.load("images/player/player_walk2.png").convert_alpha(),True,False)
player_walki_3 = pygame.transform.flip(pygame.image.load("images/player/player_walk3.png").convert_alpha(),True,False)
player_walki_4 = pygame.transform.flip(pygame.image.load("images/player/player_walk4.png").convert_alpha(),True,False)
player_walki = [player_walki_1,player_walki_2,player_walki_3,player_walki_4]
player_walki_index = 0

player_jump = pygame.image.load("images/player/player_jump.png").convert_alpha()
player_surf = player_idle[player_index]

player_rect = player_surf.get_rect(midbottom = (60,330))
player_front = pygame.image.load("images/player/player_front_x9.png").convert_alpha()
player_front_rect = player_front.get_rect(center = (360,240))
player_xspeed = 0

#Gravedad, nivel y tiempo
gravity = 0
game_active = False
start_time = 0
score_fin = 0

#Pantalla Inicio
txt_inicio = font.render("Llega al SENA!",False,(11,121,122))
txt_inicio_rect = txt_inicio.get_rect(center = (360,30))
txt_inicio_inst = font.render("Presiona [Space] para empezar",False,(11,121,122))
txt_inicio_inst_rect = txt_inicio_inst.get_rect(center = (360,400))

#Contador para Spawn enemigo
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,1500)

dengue_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(dengue_animation_timer,100)

rat_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(rat_animation_timer,200)

vel_enemies = 5

while True:
    #pygame.event.get() recibe los eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom==330:
                    gravity = -20
            if event.type == obstacle_timer:
                if vel_enemies != -1:
                    if randint(0,2):
                        obstacle_rect_list.append(rat_surf.get_rect(midbottom = (randint(1020,1320),330)))
                    else:
                        obstacle_rect_list.append(dengue_surf.get_rect(midbottom = (randint(1020,1320),140)))
            if event.type == dengue_animation_timer:
                if dengue_index == 0:
                    dengue_index = 1
                else:
                    dengue_index = 0
                dengue_surf = dengue_frames[dengue_index]
            if event.type == rat_animation_timer:
                if rat_index == 0:
                    rat_index = 1
                else:
                    rat_index = 0
                rat_surf = rat_frames[rat_index]
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    player_rect.left = 90
                    player_xspeed = 0
                    player_rect.bottom = 330
                    sky_rect.left = 0
                    ground_rect.left = 0
                    start_time = pygame.time.get_ticks()
                    game_active = True
    if game_active:
        #Mundo
        screen.blit(sky,sky_rect)
        screen.blit(ground,ground_rect)


        #Jugador en pantalla
        screen.blit(player_surf,player_rect)
        gravity += 1
        player_rect.bottom += gravity
        if player_rect.bottom >= 330:
            player_rect.bottom = 330
        player_animation()
        #Movimiento y colision con bordes
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]: player_xspeed = 6
        elif keys[pygame.K_a]: player_xspeed = -6
        else: player_xspeed = 0
        #Colisiones bordes y velocidad de enemigos
        vel_enemies = 5
        player_rect.left += player_xspeed
        if player_rect.left < 30:
            player_rect.left = 30
            if ground_rect.left < 0:
                ground_rect.x += 6
                vel_enemies = -1
            if sky_rect.left < 0:
                sky_rect.x += 1
        if player_rect.right > 320:
            player_rect.right = 320
            if ground_rect.right > 720:
                ground_rect.x += -6
                vel_enemies = 11
            if sky_rect.right > 720  and ground_rect.right > 720:
                sky_rect.x += -1
        
        #Spawnear enemigos
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)


        game_active = collisions(player_rect,obstacle_rect_list)
        score_fin = display_score()

    else:
        screen.fill((111,179,47))
        screen.blit(txt_inicio,txt_inicio_rect)
        screen.blit(player_front,player_front_rect)
        score_surf = font.render(f"Tu puntaje: {score_fin}",False,(11,121,122))
        score_surf_rect = score_surf.get_rect(center = (360,400))
        obstacle_rect_list.clear()
        if score_fin == 0:
            screen.blit(txt_inicio_inst,txt_inicio_inst_rect)
        else:
            screen.blit(score_surf,score_surf_rect)
    #Actualiza el display
    pygame.display.update()
    #Ajusta iteraciones a 60
    clock.tick(60)