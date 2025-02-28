import random

import pygame
import os

from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT

pygame.init()

FPS = pygame.time.Clock()

HEIGHT = 600
WIDHT = 1000

FONT = pygame.font.SysFont("Verdana", 20)

COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0) 
COLOR_BLUE = (0, 0, 255)
COLOR_GREEN = (0, 255, 0)

ANIMATION_DIR = "goose" 
CHANGE_IMAGE_TIME = 250  


main_display = pygame.display.set_mode((WIDHT, HEIGHT))

bg = pygame.transform.scale(pygame.image.load("background.png"), (WIDHT, HEIGHT))
bg_X1 = 0
bg_X2 = bg.get_width()
bg_move = 3


player_size = (20, 20)
player = pygame.image.load("player.png").convert_alpha()
player_rect = player.get_rect()
player_move_down = [0, 4]
player_move_right = [4, 0]
player_move_up = [0, -4]
player_move_left = [-4, 0] 

def create_bonus():
    create_bonus_size = (50, 50)
    create_bonus = pygame.image.load("bonus.png").convert_alpha()
    center_x = WIDHT // 2 - create_bonus_size[0] // 2 
    create_bonus_rect = pygame.Rect(center_x, 0, *create_bonus_size)
    create_bonus_move = [0, random.randint(4, 8)]
    return [create_bonus, create_bonus_rect, create_bonus_move]

CREATE_BONUS = pygame.USEREVENT + 2
pygame.time.set_timer(CREATE_BONUS, 1500) 

bonuses = []
score = 0


def create_enemy():
    enemy_size = (30, 30)
    enemy = pygame.image.load("enemy.png").convert_alpha()
    center_y = HEIGHT // 2
    offset_y = 150 
    random_y = random.randint(center_y - offset_y, center_y + offset_y)
    enemy_rect = pygame.Rect(WIDHT, random_y, *enemy_size)
    enemy_move = [random.randint(-8, -4), 0]
    return [enemy, enemy_rect, enemy_move]

CREATE_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENEMY, 1500)  

enemies = []

playing = True

player_images = []
for filename in os.listdir(ANIMATION_DIR):
    if filename.endswith(".png"):
        image = pygame.image.load(os.path.join(ANIMATION_DIR, filename)).convert_alpha()
        player_images.append(image)

player = player_images[0]
player_rect = player.get_rect()
player_rect.centery = HEIGHT // 2 
player_rect.left = 20  
current_frame = 0
last_update = pygame.time.get_ticks()

while playing:
    FPS.tick(120)

    for event in pygame.event.get():
        if event.type == QUIT:
            playing = False
        if event.type == CREATE_ENEMY:
            enemies.append(create_enemy())
        if event.type == CREATE_BONUS:
            bonuses.append(create_bonus())    

    bg_X1 -= bg_move
    bg_X2 -= bg_move
    
    if bg_X1 < -bg.get_width():
        bg_X1 = bg.get_width()
    if bg_X2 < -bg.get_width():
        bg_X2 = bg.get_width()
    

    main_display.blit(bg, (bg_X1, 0))
    main_display.blit(bg, (bg_X2, 0))
    
    current_time = pygame.time.get_ticks()
    if current_time - last_update >= CHANGE_IMAGE_TIME:
        current_frame = (current_frame + 1) % len(player_images)
        player = player_images[current_frame]
        last_update = current_time
    
    keys = pygame.key.get_pressed ()
    
    if keys[K_DOWN] and player_rect.bottom < HEIGHT:
        player_rect = player_rect.move(player_move_down)
    if keys[K_UP] and player_rect.top > 0:
        player_rect = player_rect.move(player_move_up)
    if keys[K_RIGHT] and player_rect.right < WIDHT:
        player_rect = player_rect.move(player_move_right) 
    if keys[K_LEFT] and player_rect.left > 0:
        player_rect = player_rect.move(player_move_left)

    for enemy in enemies:
        enemy[1] = enemy[1].move(enemy[2])
        main_display.blit(enemy[0], enemy[1])
        
        if player_rect.colliderect(enemy[1]):
            playing = False
        
    for bonus in bonuses:
        bonus[1] = bonus[1].move(bonus[2])
        main_display.blit(bonus[0], bonus[1])
        
        if player_rect.colliderect(bonus[1]):
            score += 1
            bonuses.pop(bonuses.index(bonus))
            

    main_display.blit(FONT.render(str(score), True, COLOR_BLACK), (WIDHT -50, 20))
    main_display.blit(player, player_rect)


    pygame.display.flip()   

    for enemy in enemies:
        if enemy[1].left < 0:
            enemies.pop(enemies.index(enemy))  
            
    
    for bonus in bonuses:
        if bonus[1].bottom > HEIGHT:  
            bonuses.pop(bonuses.index(bonus))

    print(len(enemies))
  
  


        
            
    