import pygame
import numpy as np
from pygame import mixer
import random

#initialise pygame

pygame.init()
 
# Initial screen diplay, title and background music
screen_size = (900 ,600)
screen = pygame.display.set_mode(screen_size)
running = True
clock = pygame.time.Clock()
fps = 240

pygame.display.set_caption('Space Invaders')
icon = pygame.image.load('Images/logo.png')
pygame.display.set_icon(icon)

background = pygame.image.load('Images/background.jpg')
mixer.music.load('Sounds/background_music.mp3')
mixer.music.play(-1)

title = pygame.image.load('Images/title.png')

font = pygame.font.Font('arcade_ya/ARCADE_N.TTF',32)
opacity = 0
opacity_change = 0.5

def fading_text(text,opacity,position):
    text = font.render(text, True, (255,255,255))
    surf = pygame.Surface(text.get_size()).convert_alpha()
    surf.fill((255, 255, 255, opacity))

    text.blit(surf, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    screen.blit(text, position)

def Title_screen():
    global opacity
    global opacity_change
    text = 'Ready Player One'
    fading_text(text,opacity,(225,500))
    screen.blit(title,(175,100))

    if opacity > 254:
        opacity_change = -1.0
    elif opacity < 1:
        opacity_change = 0.5
    opacity += opacity_change


def Ending_screen():
    global opacity_change
    global opacity

    text = 'Press Space to play again'
    fading_text(text, opacity,(75,500))

    if opacity > 254:
        opacity_change = -1.0
    elif opacity < 1:
        opacity_change = 0.5
    opacity += opacity_change
    


#PLayer

player_image = pygame.image.load('Images/space_ship.png')
playerX = 450
playerY = 700
player_life = True
player_explosion_index = 0
movement_x = 0
movement_y = 1

def player():
    global playerX
    global playerY
    global player_life
    global movement_x
    global fire 

    if player_life:
        playerX += movement_x
        playerX = np.clip(playerX,0,850)
        screen.blit(player_image,(playerX,playerY))
    
    else:
        fire = False
        pass

# Projectile

projectile_image = pygame.image.load('Images/bullet.png')
projectileX = 400
projectileY = 500
fire = False
movement_y_projectile= 3
bullet_sound = mixer.Sound('Sounds/laser_shot.mp3')
bullet_sound.set_volume(0.5)


def projectile_fire(projectileX):
    global projectileY
    global fire

    if fire:
        screen.blit(projectile_image,(projectileX+12,projectileY-20))
        projectileY -= movement_y_projectile
        if projectileY <= 0 :
            fire = False
            projectileY = 500


# Alien
alien_image = pygame.image.load('Images/green_alien.png')
number_of_aliens = 24
collisions = [False for i in range(number_of_aliens)]

vel_alien_x =  np.zeros(number_of_aliens)
vel_alien_y =  np.ones(number_of_aliens) * 1.0

alien_x = np.linspace(90,810,number_of_aliens//3)
alien_x = np.concatenate([alien_x,alien_x,alien_x])

alien_y = np.ones(number_of_aliens//3) *-50
alien_y = np.concatenate([alien_y,3*alien_y,5*alien_y])

def alien(index):
    global collisions
    global alien_x
    global alien_y

    if not collisions[index]:
        screen.blit(alien_image,(alien_x[index],alien_y[index]))
        if alien_x[index] >= 850:
            vel_alien_x[index] = -1.5
            alien_y[index] += vel_alien_y[index]

        elif alien_x[index] <= 0:
            vel_alien_x[index] = 1.5
            alien_y[index] += vel_alien_y[index]

        alien_x[index] += vel_alien_x[index]
    else:
        vel_alien_x[index] = 0
        vel_alien_y[index] = 0

#Loading screen

round_one_sound = mixer.Sound('Sounds/round_one.mp3')

def load_aliens():
    global number_of_aliens
    global alien_x
    global alien_y
    global vel_alien_x
    global vel_alien_y
    global load_state_1
    global play_state_1
    global movement_y
    global movement_x
    global finish_him

    font = pygame.font.Font('arcade_ya/ARCADE_N.TTF',20)
    text_string = 'Aliens are coming to invade!'
    text = font.render(text_string, True, (255,255,255))
    screen.blit(text,(200,400))

    if finish_him:
        round_one_sound.play()
        finish_him = False

    #Update positions
    alien_y = alien_y + vel_alien_y
    for i in range(number_of_aliens):
        screen.blit(alien_image,(alien_x[i],alien_y[i]))

    if alien_y[i] >= 100:
        finish_him = True
        load_state_1 = False
        play_state_1 = True
        vel_alien_x = np.ones(number_of_aliens) * 1.0
        vel_alien_y = np.ones(number_of_aliens) * 50.0
        movement_y = 0.0
        movement_x = 0.0


# Aliens explosion

def is_collision(index,x1,y1,x2,y2):
    global collisions
    global fire
    global projectileY

    distance = np.linalg.norm(np.array([x1,y1])-np.array([x2,y2]))
    
    if distance < 25:
        collisions[index] = True
        fire = False
        projectileY = 500



explosion_sheet = pygame.image.load('Images/explosion_sheet.png').convert_alpha()
explosion_sound = mixer.Sound('Sounds/explosion1.mp3')
explosion_sound.set_volume(0.5)
explosion_pass = [True for i in range(number_of_aliens)]
explosion_indexs = np.zeros(number_of_aliens)
explosion_x = np.zeros(number_of_aliens)
explosion_y = np.zeros(number_of_aliens)


def get_explosion_image(index,width,height):
    global explosion_sheet
    x = index % 5
    y = index // 5
    x *= 48
    y *= 48
    image = pygame.Surface((width,height)).convert_alpha()
    image.blit(explosion_sheet,(0,0),(x,y,width,height))
    return image


def new_explosion(i):

    global alien_x
    global alien_y
    global collisions
    global explosion_indexs
    global explosion_x
    global explosion_y

    is_collision(i,projectileX,projectileY,alien_x[i],alien_y[i])
    frames = 8

    if not collisions[i]:
        explosion_x[i] = alien_x[i]
        explosion_y[i] = alien_y[i]
   
    else:
        #off screen 
        alien_x[i] = 300
        alien_y[i] = -500
        index = explosion_indexs[i] // frames
        if explosion_indexs[i] < 1.0:
            explosion_sound.play()

        
        image = get_explosion_image(index,48,48)
        screen.blit(image,(explosion_x[i],explosion_y[i]))
        explosion_indexs[i] += 1
        #Cap out index


#Boss

boss_image = pygame.image.load('Images/boss.png')
boss_health = 10
boss_x = 200
boss_y = -1000
boss_collision = False
boss_explosion_sound = mixer.Sound('Sounds/explosion2.mp3')
boss_final_explosion = mixer.Sound('Sounds/boss_explosion.mp3')

vel_boss_x = 2.0
vel_boss_y = 5.0
boss_index = 0

def boss():
    global boss_health
    global boss_index
    global boss_x
    global boss_y
    global vel_boss_y
    global vel_boss_x
    global play_state_1 
    global wins_state


    if boss_health > 0.0:
        if boss_y < -75:
            boss_y += vel_boss_y
        if boss_x > 675:
            vel_boss_x = -2.0
        elif boss_x < 0:
            vel_boss_x = 2.0
        boss_x += vel_boss_x
        screen.blit(boss_image,(boss_x,boss_y))
        side_fire()
        middle_fire()
    
    else:
        #Remove Boss from screen

        frames = 20

        if boss_index == 0:
            mixer.music.stop()
            boss_final_explosion.play()
            toasty_sound.play()
            

        enter_index = boss_index // frames

        if enter_index > 30:
            play_state_1 = False
            wins_state = True



        image = boss_explosion_image(enter_index,300,200)
        screen.blit(image,(boss_x,boss_y+50))
        boss_index +=1

        
# Boss explosion

boss_explosion_sheet = pygame.image.load('Images/boss_explosion.png')

def boss_explosion_image(index,width,height):
    global boss_explosion_sheet
    x = index % 5

    y = index // 5
    x *= 300
    y *= 200
    y += 75
    image = pygame.Surface((width,height)).convert_alpha()
    image.blit(boss_explosion_sheet,(0,0),(x,y,width,height))
    return image

def is_boss_collision():
    global projectileX
    global projectileY
    global boss_x
    global boss_y
    global boss_collision
    global boss_health
    global fire



    x_dist = boss_x - projectileX 
    y_dist = abs(boss_y - projectileY)

    if x_dist <5 and x_dist > -200:

        if y_dist < 150:
            boss_health -= 1.0
            projectileY = 500
            fire = False
            boss_explosion_sound.play()

#Boss firing projectiles

double_fire = pygame.image.load('Images/double_fire.png')
triple_fire = pygame.image.load('Images/triple_fire.png')
quadruple_fire_image = pygame.image.load('Images/quadruple_fire.png')
special_fire = pygame.image.load('Images/special_fire.png')


boss_fire_velovity = 3.0
boss_side_fire = False
boss_middle_fire = False
special_fire_choice = False

middle_fire_x = 0
middle_fire_y = 0
side_fire_x = 0
side_fire_y = 0

middle_firing_frames = 800
side_firing_frames = 700

side_fire_sound = mixer.Sound('Sounds/side_fire.mp3')
side_fire_sound.set_volume(0.5)
middle_fire_sound  = mixer.Sound('Sounds/middle_fire.mp3')
middle_fire_sound.set_volume(0.5)

def middle_fire():
    global boss_middle_fire
    global boss_x
    global boss_y
    global middle_fire_y
    global middle_fire_x
    global middle_firing_frames
    global special_fire_choice


    if middle_firing_frames < 1:
        middle_firing_frames = random.randint(250,500)
        boss_middle_fire = True
        special_fire_choice = random.choice([True,False])
        middle_fire_sound.play()
    
    else:
        middle_firing_frames -= 1
    

    if boss_middle_fire:
        middle_fire_y += boss_fire_velovity

        if special_fire_choice:

           screen.blit(special_fire,(middle_fire_x+65,middle_fire_y+140))

        else:
            screen.blit(quadruple_fire_image,(middle_fire_x+85,middle_fire_y+150)) 
        if middle_fire_y > 600:
            middle_fire_y = 0
            boss_middle_fire = False

    
    else:
        middle_fire_y = boss_y
        middle_fire_x = boss_x


def side_fire():
    global boss_side_fire
    global boss_x
    global boss_y
    global side_fire_y
    global side_fire_x
    global side_firing_frames


    if side_firing_frames < 1:
        side_firing_frames = random.randint(250,500)
        boss_side_fire = True
        #triple_fire_choice = random.choice([True,False])
        triple_fire_choice = True
        side_fire_sound.play()
    
    else:
        side_firing_frames -= 1

    

    if boss_side_fire:
        side_fire_y += boss_fire_velovity


        screen.blit(triple_fire,(side_fire_x+40,side_fire_y+160))
        screen.blit(triple_fire,(side_fire_x+150,side_fire_y+160))

        
        if side_fire_y > 600:
            side_fire_y = 0
            boss_side_fire = False

    
    else:
        side_fire_y = boss_y
        side_fire_x = boss_x


# Player Explosion
    
def laser_collision():
    global middle_fire_x
    global middle_fire_y
    global side_fire_x
    global side_fire_y
    global playerX
    global playerY
    global player_life
    global special_fire_choice

    mid_dist_y = playerY - middle_fire_y 
    mid_dist_x = playerX - middle_fire_x

    side_dist_x = playerX - side_fire_x
    side_dist_y = playerY - side_fire_y

    #distance = np.linalg.norm(np.array([playerX,playerY])-np.array([x2,y2]))

    if not special_fire_choice:
        if mid_dist_y < 200 and mid_dist_y > 165:
            if mid_dist_x > 50 and mid_dist_x < 155:
                player_life = False

                explosion_sound.play()
    else:
        if mid_dist_y < 200 and mid_dist_y > 165:
            if mid_dist_x > 25 and mid_dist_x < 175:
                player_life = False

                explosion_sound.play()


    if side_dist_y < 200 and side_dist_y > 165:
        if (side_dist_x > 0 and side_dist_x < 90) or (side_dist_x > 110 and side_dist_x < 200) :
            player_life = False
            explosion_sound.play()
   

def destruction():
    global alien_x
    global alien_y
    global playerX
    global player_life
    global lose_state
    global play_state_1

    if max(alien_y) > 450:
        i = list(alien_y).index(max(alien_y))
        dist = abs(alien_x[i]-playerX)
        if dist < 400:
            if player_life:
                explosion_sound.play()

            player_life = False
       
                
def player_explosion():
    global player_life
    global playerX
    global playerY
    global player_explosion_index
    global lose_state
    global play_state_1

    frames = 15

    laser_collision()
    destruction()
    if not player_life:
        index = player_explosion_index // frames

        image = get_explosion_image(index,48,48)
        screen.blit(image,(playerX,playerY))
        player_explosion_index += 1
        if index == 16:
            lose_state = True
            play_state_1 = False





# State Machine

intro_state = True

load_state_1 = False

play_state_1 = False

wins_state = False

lose_state = False

def play_state():
    screen.blit(background,(0,0))
    player()
    boss()
    is_boss_collision()
    player_explosion()
    
    for i in range(number_of_aliens):
        new_explosion(i)
        alien(i)
        

    projectile_fire(projectileX)

def original_state():
    global playerX
    global playerY
    global player_life
    global player_explosion_index
    global movement_x 
    global movement_y 
    global collisions
    global vel_alien_x 
    global vel_alien_y 
    global alien_x 
    global alien_y 
    global alien_y 
    global projectileX
    global projectileY 
    global fire 
    global movement_y_projectile
    global boss_health 
    global boss_x 
    global boss_y
    global boss_collision 
    global vel_boss_x 
    global vel_boss_y
    global boss_index
    global boss_fire_velovity 
    global boss_side_fire 
    global boss_middle_fire 
    global special_fire_choice 
    global middle_fire_x 
    global middle_fire_y 
    global side_fire_x 
    global side_fire_y
    global middle_firing_frames 
    global side_firing_frames 
    global explosion_pass 
    global explosion_indexs 
    global explosion_x
    global explosion_y 
    global finish_him 
    global finish_sound
    
    playerX = 450
    playerY = 700
    player_life = True
    player_explosion_index = 0
    movement_x = 0
    movement_y = 1
    collisions = [False for i in range(number_of_aliens)]


    vel_alien_x =  np.zeros(number_of_aliens)
    vel_alien_y =  np.ones(number_of_aliens) * 1.0

    alien_x = np.linspace(90,810,number_of_aliens//3)
    alien_x = np.concatenate([alien_x,alien_x,alien_x])

    alien_y = np.ones(number_of_aliens//3) *-50
    alien_y = np.concatenate([alien_y,3*alien_y,5*alien_y])
    projectileX = 400
    projectileY = 500
    fire = False
    movement_y_projectile= 3
    boss_health = 10
    boss_x = 200
    boss_y = -1000
    boss_collision = False

    vel_boss_x = 2.0
    vel_boss_y = 5.0
    boss_index = 0

    boss_fire_velovity = 2.5
    boss_side_fire = False
    boss_middle_fire = False
    special_fire_choice = False

    middle_fire_x = 0
    middle_fire_y = 0
    side_fire_x = 0
    side_fire_y = 0

    middle_firing_frames = 800
    side_firing_frames = 700

    explosion_pass = [True for i in range(number_of_aliens)]
    explosion_indexs = np.zeros(number_of_aliens)
    explosion_x = np.zeros(number_of_aliens)
    explosion_y = np.zeros(number_of_aliens)
    finish_him = True
    finish_sound = True


    mixer.music.play(-1)



# Added sound effects

finish_him_sound = mixer.Sound('Sounds/finish_him.mp3')
flawless = mixer.Sound('Sounds/flawless.mp3')
fatality = mixer.Sound('Sounds/fatality.mp3')
fatality_background = mixer.Sound('Sounds/fatality_background.mp3')
toasty_sound = mixer.Sound('Sounds/toasty.mp3')
finish_him = True
finish_sound = True


    

while running:

    if intro_state:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                intro_state = False
                load_state_1 = True
        
        screen.fill((0,0,0))
        Title_screen()

    elif load_state_1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        screen.blit(background,(0,0))
        load_aliens()
        if playerY > 500:
            playerY -= movement_y
        
        screen.blit(player_image,(playerX,playerY))
        


    elif play_state_1:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    movement_x = -1.5
                if event.key == pygame.K_RIGHT:
                    movement_x = 1.5
                if event.key == pygame.K_UP:
                    movement_y = -1
                if event.key == pygame.K_DOWN:
                    movement_y = 1
                if event.key == pygame.K_SPACE:
                    if not fire:
                        projectileX = playerX
                        bullet_sound.play()
                    fire = True
                    

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT  or event.key == pygame.K_LEFT:

                    movement_x = 0.0
                if event.key == pygame.K_UP  or event.key == pygame.K_DOWN:

                    movement_y = 0.0
    
            

        #running in the game

        play_state()
        if all(collisions):
            if finish_him:
                finish_him_sound.play()
                finish_him = False
        

    elif lose_state:
        mixer.music.stop()
        screen.fill((0,0,0))
        text_string = 'Game Over'
        text = font.render(text_string, True, (255,255,255))
        screen.blit(text,(325,250))
        text_string = 'You Lose'
        text = font.render(text_string, True, (255,255,255))
        screen.blit(text,(350,350))
        Ending_screen()

        
        if finish_sound:
            
            fatality_background.play()
            fatality.play()
            finish_sound = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    original_state()
                    intro_state = True
                    load_state_1 = False
                    play_state_1 = False
                    wins_state = False
                    lose_state = False

            
    elif wins_state:
        mixer.music.stop()
        screen.fill((0,0,0))

        text_string = 'Hudaifa is a Whore!!!'
        text = font.render(text_string, True, (255,255,255))
        screen.blit(text,(150,100))
        text_string = 'Game Over'
        text = font.render(text_string, True, (255,255,255))
        screen.blit(text,(325,250))
        text_string = 'You Win'
        text = font.render(text_string, True, (255,255,255))
        screen.blit(text,(350,350))

        Ending_screen()

        if finish_sound:
            flawless.play()
            finish_sound = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    original_state()

                    intro_state = True
                    load_state_1 = False
                    play_state_1 = False
                    wins_state = False
                    lose_state = False

    clock.tick(fps)
    pygame.display.update()


pygame.quit()