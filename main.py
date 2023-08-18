# First attempt at a game using pygame
# Author: Matt Young
# Date created: March 16, 2023

import random
import pygame

pygame.init()

# CONSTANTS
FALL_CHANCE = 250  # chance of ladder breaking (default 250)
SLIP_CHANCE = 100  # chance of slipping in puddle (default 100)
FALL_SPEED = 45
LIGHT_LEVEL = 0  # sets the darkness of all lights out
FLOOR = 530
CEILING = 395
X_SPEED = 9
Y_SPEED = 6
LADDER_Y_WALK = 415
LADDER_Y_CLIMB = 380
testFont = pygame.font.Font(None, 150)
smallFont = pygame.font.Font(None, 60)
smallerFont = pygame.font.Font(None, 35)
flashTimer = 4  # max duration of lightning strike
fade = 255
gameTimer = 0

DISPLAY_TITLE = testFont.render('NIGHT SHIFT', True, 'White')
DISPLAY_PRESS_SPACE = smallerFont.render('Press Space to Play...', True, 'White')
DISPLAY_INTRO = smallFont.render('Welcome to the night shift.', True, 'White')
DISPLAY_INTRO2 = smallFont.render('All you have to do is keep the lights on...', True, 'White')
red = (200, 0, 0)  # set to 200,0,0
green = (0, 200, 0)
DISPLAY_INTRO3 = smallFont.render('To stay alive.', True, red)
DISPLAY_WINNER1 = testFont.render('Player One Wins!', True, green)
DISPLAY_WINNER2 = testFont.render('Player Two Wins!', True, red)
POINTS1 = 0
POINTS2 = 0

w, h = 1320, 600
screen = pygame.display.set_mode((w, h), pygame.NOFRAME)

pygame.display.set_caption('Night Shift')  # Title of the window
clock = pygame.time.Clock()
test_font = pygame.font.Font(None, 100)

bg_black = pygame.Surface((1920, 1080))
bg_black.fill('black')

fg_white = pygame.Surface((w, h)).convert_alpha()
color = (200, 220, 255)
fg_white.fill(color)
frame = pygame.image.load('assets/frame.png').convert_alpha()
frame = pygame.transform.scale(frame, (1920, 1080))

bg_clouds = pygame.image.load('assets/clouds.png').convert_alpha()
bg_lightning = pygame.image.load('assets/lightning.png').convert_alpha()
bg_rain1 = pygame.image.load('assets/rain1.png').convert_alpha()
bg_rain2 = pygame.image.load('assets/rain2.png').convert_alpha()
bg_rain3 = pygame.image.load('assets/rain3.png').convert_alpha()
bg_rain_surf = bg_rain1
bg_rain = [bg_rain1, bg_rain2, bg_rain3]
bg_rain_index = 0

bg_store = pygame.image.load('assets/template-work.png').convert_alpha()

# shadow overlays when lights on
fg_light1_on = pygame.image.load('assets/light1_on.png').convert_alpha()
fg_light2_on = pygame.image.load('assets/light2_on.png').convert_alpha()
fg_light3_on = pygame.image.load('assets/light3_on.png').convert_alpha()
fg_light4_on = pygame.image.load('assets/light4_on.png').convert_alpha()
fg_light5_on = pygame.image.load('assets/light5_on.png').convert_alpha()
fg_light6_on = pygame.image.load('assets/light6_on.png').convert_alpha()

# shadow overlays when lights on
fg_light1_off = pygame.image.load('assets/light1_off.png').convert_alpha()
fg_light2_off = pygame.image.load('assets/light2_off.png').convert_alpha()
fg_light3_off = pygame.image.load('assets/light3_off.png').convert_alpha()
fg_light4_off = pygame.image.load('assets/light4_off.png').convert_alpha()
fg_light5_off = pygame.image.load('assets/light5_off.png').convert_alpha()
fg_light6_off = pygame.image.load('assets/light6_off.png').convert_alpha()

# bulb when off
lamp1 = pygame.image.load('assets/bulb_on.png').convert_alpha()
lamp_rect1 = lamp1.get_rect(midtop=(110, 0))
# bulb when on
lampOff1 = pygame.image.load('assets/bulb_off.png').convert_alpha()
lampOff_rect1 = lampOff1.get_rect(midtop=(110, 0))

# bulb when off
lamp2 = pygame.image.load('assets/bulb_on.png').convert_alpha()
lamp_rect2 = lamp2.get_rect(midtop=(330, 0))
# bulb when on
lampOff2 = pygame.image.load('assets/bulb_off.png').convert_alpha()
lampOff_rect2 = lampOff2.get_rect(midtop=(330, 0))

# bulb when off
lamp3 = pygame.image.load('assets/bulb_on.png').convert_alpha()
lamp_rect3 = lamp3.get_rect(midtop=(550, 0))
# bulb when on
lampOff3 = pygame.image.load('assets/bulb_off.png').convert_alpha()
lampOff_rect3 = lampOff3.get_rect(midtop=(550, 0))

# bulb when off
lamp4 = pygame.image.load('assets/bulb_on.png').convert_alpha()
lamp_rect4 = lamp4.get_rect(midtop=(770, 0))
# bulb when on
lampOff4 = pygame.image.load('assets/bulb_off.png').convert_alpha()
lampOff_rect4 = lampOff4.get_rect(midtop=(770, 0))

# bulb when off
lamp5 = pygame.image.load('assets/bulb_on.png').convert_alpha()
lamp_rect5 = lamp5.get_rect(midtop=(990, 0))
# bulb when on
lampOff5 = pygame.image.load('assets/bulb_off.png').convert_alpha()
lampOff_rect5 = lampOff5.get_rect(midtop=(990, 0))

# bulb when off
lamp6 = pygame.image.load('assets/bulb_on.png').convert_alpha()
lamp_rect6 = lamp6.get_rect(midtop=(1210, 0))
# bulb when on
lampOff6 = pygame.image.load('assets/bulb_off.png').convert_alpha()
lampOff_rect6 = lampOff6.get_rect(midtop=(1210, 0))

# player 1

char_idle = pygame.image.load('assets/char_idle.png').convert_alpha()
char_idle_right = char_idle
char_idle_left = pygame.transform.flip(char_idle_right, flip_x=True, flip_y=False)
char_fall = pygame.image.load('assets/char_fall.png').convert_alpha()
char_fall_right = char_fall
char_fall_left = pygame.transform.flip(char_fall_right, flip_x=True, flip_y=False)
char_idleL = pygame.image.load('assets/char_idleL.png').convert_alpha()
char_idle_rightL = char_idleL
char_idle_leftL = pygame.transform.flip(char_idle_rightL, flip_x=True, flip_y=False)
char_walk1 = pygame.image.load('assets/char_walk1.png').convert_alpha()
char_walk2 = pygame.image.load('assets/char_walk2.png').convert_alpha()
char_walk = [char_walk1, char_walk2]
char_walk1L = pygame.image.load('assets/char_walk1L.png').convert_alpha()
char_walk2L = pygame.image.load('assets/char_walk2L.png').convert_alpha()
char_walkL = [char_walk1L, char_walk2L]
char_climb1 = pygame.image.load('assets/char_climb1.png').convert_alpha()
char_climb1 = pygame.transform.scale(char_climb1, (150, 155))
char_climb2 = pygame.image.load('assets/char_climb2.png').convert_alpha()
char_climb2 = pygame.transform.scale(char_climb2, (150, 155))
char_climb = [char_climb1, char_climb2]
char_dead = pygame.image.load('assets/char_dead.png').convert_alpha()
char_index = 0
char_surf = char_idle

# player 2
enemy_idle = pygame.image.load('assets/enemy_walk1.png').convert_alpha()
enemy_idle_right = enemy_idle
enemy_idle_left = pygame.transform.flip(enemy_idle_right, flip_x=True, flip_y=False)
enemy_idle = enemy_idle_left
enemy_walk1 = pygame.image.load('assets/enemy_walk1.png').convert_alpha()
enemy_walk2 = pygame.image.load('assets/enemy_walk2.png').convert_alpha()
enemy_walk = [enemy_walk1, enemy_walk2]
enemy_walk1L = pygame.image.load('assets/enemy_walk1L.png').convert_alpha()
enemy_walk2L = pygame.image.load('assets/enemy_walk2L.png').convert_alpha()
enemy_walkL = [enemy_walk1L, enemy_walk2L]
enemy_idleL = pygame.image.load('assets/enemy_walk1L.png').convert_alpha()
enemy_idle_rightL = enemy_idleL
enemy_idle_leftL = pygame.transform.flip(enemy_idle_rightL, flip_x=True, flip_y=False)
enemy_climb1 = pygame.image.load('assets/enemy_climb1.png').convert_alpha()
enemy_climb2 = pygame.transform.flip(enemy_climb1, flip_x=True, flip_y=False)
enemy_climb = [enemy_climb1, enemy_climb2]
enemy_fall = pygame.image.load('assets/enemy_fall.png').convert_alpha()
enemy_fall_right = enemy_fall
enemy_fall_left = pygame.transform.flip(enemy_fall_right, flip_x=True, flip_y=False)
enemy_index = 0
enemy_surf = enemy_idle

crow1 = pygame.image.load('assets/Crow1.png').convert_alpha()
crow2 = pygame.image.load('assets/Crow2.png').convert_alpha()
crow3 = pygame.image.load('assets/Crow3.png').convert_alpha()
crow = [crow1, crow2, crow3]
crow_surf = crow1
crow_index = 0

ladder = pygame.image.load('assets/ladder.png').convert_alpha()
ladder_broken = pygame.image.load('assets/ladder_broken.png')
ladder1_break = [ladder, ladder_broken]
ladder1_index = 0

ladder_player1 = ladder
ladder_player2 = ladder

ladder_player1_left = pygame.transform.rotate(ladder_player1, angle=90)
ladder_player1_right = pygame.transform.flip(ladder_player1_left, flip_x=True, flip_y=False)
ladder_player2_left = pygame.transform.rotate(ladder_player2, angle=90)
ladder_player2_right = pygame.transform.flip(ladder_player2_left, flip_x=True, flip_y=False)

ladder_player1 = ladder_player1_right  # default starting direction
ladder_player2 = ladder_player2_left  # default starting direction

# sounds and music
thunderClap = pygame.mixer.Sound('assets/thunder.wav')
introMusic = pygame.mixer.Sound('assets/chopinintro.wav')
introMusic2 = pygame.mixer.Sound('assets/chopinintro2.wav')
music = pygame.mixer.Sound('assets/chopin_main.mp3')
screwLight = pygame.mixer.Sound('assets/screwlight.wav')
screwLight2 = screwLight
breakSound = pygame.mixer.Sound('assets/break.wav')
slipSound = pygame.mixer.Sound('assets/slip.wav')
player1win = pygame.mixer.Sound('assets/player1win.wav')
player2win = pygame.mixer.Sound('assets/player2win.wav')
thunderClap.set_volume(0.25)  # 0.3
introMusic.set_volume(0.8)  # 0.8
introMusic2.set_volume(0.9)  # 0.9
music.set_volume(0.4)  # 0.4
screwLight.set_volume(0.4)  # 0.4
breakSound.set_volume(1.0)  # 1.0
slipSound.set_volume(0.4)  # 0.4
player1win.set_volume(0.8)  # 0.8
player2win.set_volume(0.3)  # 0.3


def rain_animation():
    global bg_rain_surf, bg_rain_index
    bg_rain_index += 0.3
    if bg_rain_index >= len(bg_rain):
        bg_rain_index = 0
    bg_rain_surf = bg_rain[int(bg_rain_index)]


def char_animation(direction):
    global char_surf, char_index
    char_index += 0.15
    if char_index >= len(char_walk):
        char_index = 0
    if direction == 'right':
        char_surf = char_walk[int(char_index)]
    elif direction == 'left':
        char_surf = pygame.transform.flip(char_walk[int(char_index)], flip_x=True, flip_y=False)
    else:
        char_surf = char_idle


def char_animation_ladder(direction):
    global char_surf, char_index
    char_index += 0.15
    if char_index >= len(char_walk):
        char_index = 0
    if direction == 'right':
        char_surf = char_walkL[int(char_index)]
    elif direction == 'left':
        char_surf = pygame.transform.flip(char_walkL[int(char_index)], flip_x=True, flip_y=False)
    else:
        char_surf = char_idleL


def char_climb_animation():
    global char_surf, char_index, char_y
    if char_y > CEILING:
        char_index += 0.09
    if char_index >= len(char_climb):
        char_index = 0
    char_surf = char_climb[int(char_index)]


def enemy_animation(direction='right'):
    global enemy_surf, enemy_index
    # walk
    enemy_index += 0.15
    if enemy_index >= len(enemy_walk):
        enemy_index = 0
    if direction == 'right':
        enemy_surf = enemy_walk[int(enemy_index)]
    elif direction == 'left':
        enemy_surf = pygame.transform.flip(enemy_walk[int(enemy_index)], flip_x=True, flip_y=False)
    else:
        enemy_surf = enemy_idle


def enemy_animation_ladder(direction):
    global enemy_surf, enemy_index
    enemy_index += 0.15
    if enemy_index >= len(enemy_walk):
        enemy_index = 0
    if direction == 'right':
        enemy_surf = enemy_walkL[int(enemy_index)]
    elif direction == 'left':
        enemy_surf = pygame.transform.flip(enemy_walkL[int(enemy_index)], flip_x=True, flip_y=False)
    else:
        enemy_surf = enemy_idleL


def enemy_climb_animation():
    global enemy_surf, enemy_index, enemy_y
    if enemy_y > CEILING:
        enemy_index += 0.09
    if enemy_index >= len(enemy_climb):
        enemy_index = 0
    enemy_surf = enemy_climb[int(enemy_index)]


def thunder():
    global flashTimer, bg_lightning
    flashTimer = random.randint(0, 2)
    thunderClap.play()
    bg_lightning = pygame.transform.flip(bg_lightning, flip_x=True, flip_y=False)


def startMusic():
    global musicPlaying
    music.play(-1)
    musicPlaying = True


def playIntro():
    global introMusicPlaying, gameTimer
    music.stop()
    introMusic.play()
    introMusicPlaying = True
    gameTimer = 0


def playIntro2():
    global introMusic2Playing, gameTimer, introMusicPlaying
    introMusic.stop()
    introMusic2.play()
    introMusic2Playing = True
    gameTimer = 0


def playScrew1():
    global screw1Playing
    screwLight.play()
    screw1Playing = True


def playScrew2():
    global screw2Playing
    screwLight2.play()
    screw2Playing = True


def screw(light):
    global player1_climbing, timeStart, lights_list, screw1Playing
    if not lights_list[light]:
        if not screw1Playing:
            playScrew1()
        timeElapsed = (gameTimer - timeStart)

        if timeElapsed >= 1.0:
            screw1Playing = False
            lights_list[light] = True
            player1_climbing = False
    else:
        player1_climbing = False


def unscrew(light):
    global player2_climbing, timeStart2, lights_list, screw2Playing
    if lights_list[light]:
        if not screw2Playing:
            playScrew2()
        timeElapsed = (gameTimer - timeStart2)

        if timeElapsed >= 1.0:
            screw2Playing = False
            lights_list[light] = False
            player2_climbing = False
    else:
        player2_climbing = False


def playBreak1():
    breakSound.play()


def playBreak2():
    breakSound.play()


def playSlip1():
    slipSound.play()


def playSlip2():
    slipSound.play()


def ladder1_breaks():
    global ladder_player1, ladder1_broken, player1_hasLadder, ladder_player1_y, char_y, player1_climbing, screw1Playing
    playBreak1()
    screwLight.stop()
    ladder_player1 = ladder_broken
    ladder1_broken = True
    player1_hasLadder = False
    ladder_player1_y = 420
    char_y += FALL_SPEED
    player1_climbing = False
    screw1Playing = False


def ladder2_breaks():
    global ladder_player2, ladder2_broken, player2_hasLadder, ladder_player2_y, enemy_y, player2_climbing, screw2Playing
    playBreak2()
    screwLight2.stop()
    ladder_player2 = ladder_broken
    ladder2_broken = True
    player2_hasLadder = False
    ladder_player2_y = 420
    enemy_y += FALL_SPEED
    player2_climbing = False
    screw2Playing = False


def player1_falling(direction):
    global player1_fall, char_surf, char_y
    timeElapsed = gameTimer - falltimeStart
    if direction == "right":
        char_surf = char_fall_right
    elif direction == "left":
        char_surf = char_fall_left
    if timeElapsed >= 1:
        player1_fall = False


def player2_falling(direction):
    global player2_fall, enemy_surf, enemy_y
    timeElapsed = gameTimer - timeStart2
    if direction == "right":
        enemy_surf = enemy_fall_right
    elif direction == "left":
        enemy_surf = enemy_fall_left
    if timeElapsed >= 1:
        player2_fall = False


def crow_anim():
    global crow, crow_index, crow_surf
    crow_index += 0.01
    if crow_index >= len(crow):
        crow_index = 0
    crow_surf = crow[int(crow_index)]
    crow_surf = pygame.transform.scale(crow_surf, (100, 100))


# Game Intro
introMusicPlaying = False

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    if not introMusicPlaying:
        playIntro()

    keys_pressed = pygame.key.get_pressed()
    if keys_pressed[pygame.K_ESCAPE]:
        exit()
    if keys_pressed[pygame.K_SPACE] and gameTimer > 0.5:
        break

    gameTimer += 0.016
    screen.blit(bg_black, (0, 0))
    bg_rain_surf.set_alpha(80)
    screen.blit(bg_rain_surf, (0, 0))
    rain_animation()

    screen.blit(DISPLAY_TITLE, (330, 250))
    if gameTimer > 6.3:
        screen.blit(DISPLAY_PRESS_SPACE, (1000, 520))

    screen.blit(frame, (-300, -240))
    pygame.display.update()
    clock.tick(60)

while True:
    #  defaults
    WINNER = False
    char_x = 150
    char_y = FLOOR
    enemy_x = 1170
    enemy_y = FLOOR
    ladder_player1_x = -200
    ladder_player1_y = LADDER_Y_WALK
    ladder_player2_x = -200
    ladder_player2_y = LADDER_Y_WALK
    lightning = False

    gameTimer = 0
    timeStart = 0
    alpha = 0
    char_direction = 'right'
    enemy_direction = 'left'
    char_idle = char_idle_right
    enemy_idle = enemy_idle_left

    introMusic.stop()
    introMusic2.stop()
    music.stop()
    thunderClap.stop()
    player1win.stop()
    player2win.stop()
    introMusicPlaying = False
    introMusic2Playing = False
    musicPlaying = False
    screw1Playing = False
    screw2Playing = False
    break1Playing = False
    break2Playing = False
    player1_hasLadder = False
    player2_hasLadder = False
    ladder1_broken = False
    ladder2_broken = False
    player1_climbing = False
    player2_climbing = False
    player1_atLight = False
    player2_atLight = False
    player1_fall = False
    player2_fall = False
    counter = False

    lights_list = [False, False, False, False, False, False]

    # turns(3 lights on
    list = [0, 1, 2, 3, 4, 5]
    for i in range(3):
        x = random.choice(list)
        list.remove(x)

    for i in list:
        lights_list[i] = True

    # intro part 2
    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_ESCAPE]:
            exit()

        screen.blit(bg_black, (0, 0))
        if introMusicPlaying:
            introMusic.stop()
        if not introMusic2Playing:
            playIntro2()
        gameTimer += 0.016

        if keys_pressed[pygame.K_SPACE] and gameTimer > 0.5:
            break

        screen.blit(DISPLAY_INTRO, (100, 150))
        if gameTimer > 2.8:
            screen.blit(DISPLAY_INTRO2, (100, 250))
        if gameTimer > 5.5:
            if alpha < 220:
                alpha += 3
            redText = (alpha, 0, 0)
            DISPLAY_INTRO3 = smallFont.render('To stay alive.', True, redText)
            screen.blit(DISPLAY_INTRO3, (100, 400))
        if gameTimer > 9:  # 9
            break

        screen.blit(frame, (-300, -240))
        pygame.display.update()
        clock.tick(60)

    # Main Game
    while True:
        gameTimer += 0.016
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        introMusic.stop()
        introMusic2.stop()
        if not musicPlaying:
            startMusic()
            thunder()

        # lightning flashes
        if flashTimer > 10:  # 9
            flashChance = random.randint(0, 220)  # 220
            if flashChance == 1:
                thunder()

        if flashTimer < 3:
            flashing = random.randint(0, 10)
            if flashing != 0:
                lightning = True
                flash = 255
        flashTimer += .1

        # player 1 movement
        char_rect = char_surf.get_rect(midbottom=(char_x, char_y))
        char_surf = char_idle

        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_ESCAPE]:
            exit()
        if keys_pressed[pygame.K_SPACE] and WINNER:
            break

        if keys_pressed[pygame.K_LEFT] and char_y == FLOOR and not player1_fall and not WINNER:
            char_x -= X_SPEED
            char_direction = 'left'
            if player1_hasLadder:
                char_animation_ladder(char_direction)
                char_idle = char_idle_leftL
                ladder_player1 = ladder_player1_left
                ladder_player1_x = char_rect.x
                ladder_player1_y = LADDER_Y_WALK
            else:
                char_animation(char_direction)
                char_idle = char_idle_left
            if 720 >= char_x >= 600:  # slip on puddle
                slip_chance1 = random.randint(0, SLIP_CHANCE)
                if slip_chance1 == 0:
                    if not player1_fall:
                        playSlip1()
                        falltimeStart = gameTimer
                        player1_fall = True
                    if player1_hasLadder:
                        ladder1_breaks()
        if keys_pressed[pygame.K_RIGHT] and char_y == FLOOR and not player1_fall and not WINNER:
            char_x += X_SPEED
            char_direction = 'right'
            if player1_hasLadder:
                char_animation_ladder(char_direction)
                ladder_player1 = ladder_player1_right
                ladder_player1_x = char_rect.x
                ladder_player1_y = LADDER_Y_WALK
                char_idle = char_idle_rightL
            else:
                char_idle = char_idle_right
                char_animation(char_direction)
            if 720 >= char_x >= 600:  # slip on puddle
                slip_chance1 = random.randint(0, SLIP_CHANCE)
                if slip_chance1 == 0:
                    if not player1_fall:
                        playSlip1()
                        falltimeStart = gameTimer
                        player1_fall = True
                    if player1_hasLadder:
                        ladder1_breaks()

        if keys_pressed[pygame.K_UP]:  # climb
            if player1_hasLadder and not player1_climbing and char_y == FLOOR and not player1_fall and not WINNER:
                if 80 <= char_x <= 140:
                    char_x = lamp_rect1.centerx
                    player1_atLight = True
                elif 300 <= char_x <= 360:
                    char_x = lamp_rect2.centerx
                    player1_atLight = True
                elif 520 <= char_x <= 580:
                    char_x = lamp_rect3.centerx
                    player1_atLight = True
                elif 740 <= char_x <= 800:
                    char_x = lamp_rect4.centerx
                    player1_atLight = True
                elif 960 <= char_x <= 1020:
                    char_x = lamp_rect5.centerx
                    player1_atLight = True
                elif 1180 <= char_x <= 1240:
                    char_x = lamp_rect6.centerx
                    player1_atLight = True
                else:
                    player1_atLight = False

                ladder_player1 = ladder
                ladder_player1_x = char_x - 60
                ladder_player1_y = LADDER_Y_CLIMB
                if not player1_climbing:
                    timeStart = gameTimer
                player1_climbing = True

        if char_y < FLOOR:
            char_climb_animation()

        if player1_climbing and (char_y > CEILING):
            char_y -= Y_SPEED
        if char_y <= 430:
            # ladder breaks
            fall_chance1 = random.randint(0, FALL_CHANCE)
            if fall_chance1 == 0:
                if not player1_fall:
                    falltimeStart = gameTimer
                    player1_fall = True
                ladder1_breaks()
        if player1_fall:
            player1_falling(char_direction)

        if char_x == lamp_rect1.centerx and char_y <= CEILING:
            screw(0)
        if char_x == lamp_rect2.centerx and char_y <= CEILING:
            screw(1)
        if char_x == lamp_rect3.centerx and char_y <= CEILING:
            screw(2)
        if char_x == lamp_rect4.centerx and char_y <= CEILING:
            screw(3)
        if char_x == lamp_rect5.centerx and char_y <= CEILING:
            screw(4)
        if char_x == lamp_rect6.centerx and char_y <= CEILING:
            screw(5)
        if char_y <= CEILING and not player1_atLight:
            player1_climbing = False

        if not player1_climbing and char_y >= CEILING:
            char_y += Y_SPEED

        # player 2 movement
        enemy_rect = enemy_surf.get_rect(midbottom=(enemy_x, enemy_y))
        enemy_surf = enemy_idle

        if keys_pressed[pygame.K_a] and enemy_y == FLOOR and not player2_fall and not WINNER:
            enemy_x -= X_SPEED
            enemy_direction = 'left'
            if player2_hasLadder:
                enemy_animation_ladder(enemy_direction)
                enemy_idle = enemy_idle_leftL
                ladder_player2 = ladder_player2_left
                ladder_player2_x = enemy_rect.x
                ladder_player2_y = LADDER_Y_WALK
            else:
                enemy_idle = enemy_idle_left
                enemy_animation(enemy_direction)
            if 720 >= enemy_x >= 600:  # slip on puddle
                slip_chance2 = random.randint(0, SLIP_CHANCE)
                if slip_chance2 == 0:
                    if not player2_fall:
                        playSlip2()
                        timeStart2 = gameTimer
                        player2_fall = True
                    if player2_hasLadder:
                        ladder2_breaks()
        if keys_pressed[pygame.K_d] and enemy_y == FLOOR and not player2_fall and not WINNER:
            enemy_x += X_SPEED
            enemy_direction = 'right'
            if player2_hasLadder:
                enemy_animation_ladder(enemy_direction)
                enemy_idle = enemy_idle_rightL
                ladder_player2 = ladder_player2_right
                ladder_player2_x = enemy_rect.x
                ladder_player2_y = LADDER_Y_WALK
            else:
                enemy_animation(enemy_direction)
                enemy_idle = enemy_idle_right
            if 720 >= enemy_x >= 600:  # slip on puddle
                slip_chance2 = random.randint(0, SLIP_CHANCE)
                if slip_chance2 == 0:
                    if not player2_fall:
                        playSlip2()
                        timeStart2 = gameTimer
                        player2_fall = True
                    if player2_hasLadder:
                        ladder2_breaks()
        if player2_fall:
            player2_falling(enemy_direction)

        if keys_pressed[pygame.K_w]:  # climb
            if player2_hasLadder and enemy_y == FLOOR and not player2_climbing and not player2_fall and not WINNER:
                if 80 <= enemy_x <= 140:
                    enemy_x = lamp_rect1.centerx
                    player2_atLight = True
                elif 300 <= enemy_x <= 360:
                    enemy_x = lamp_rect2.centerx
                    player2_atLight = True
                elif 520 <= enemy_x <= 580:
                    enemy_x = lamp_rect3.centerx
                    player2_atLight = True
                elif 740 <= enemy_x <= 800:
                    enemy_x = lamp_rect4.centerx
                    player2_atLight = True
                elif 960 <= enemy_x <= 1020:
                    enemy_x = lamp_rect5.centerx
                    player2_atLight = True
                elif 1180 <= enemy_x <= 1240:
                    enemy_x = lamp_rect6.centerx
                    player2_atLight = True
                else:
                    player2_atLight = False

                ladder_player2 = ladder
                ladder_player2_x = enemy_x - 60
                ladder_player2_y = LADDER_Y_CLIMB
                if not player2_climbing:
                    timeStart2 = gameTimer
                player2_climbing = True

        if enemy_y < FLOOR:
            enemy_climb_animation()

        if player2_climbing and (enemy_y > CEILING):
            enemy_y -= Y_SPEED
        if enemy_y <= 430:
            # ladder breaks
            fall_chance2 = random.randint(0, FALL_CHANCE)
            if fall_chance2 == 0:
                if not player2_fall:
                    timeStart2 = gameTimer
                    player2_fall = True
                ladder2_breaks()
        if player2_fall:
            player2_falling(enemy_direction)

        if enemy_x == lamp_rect1.centerx and enemy_y <= CEILING:
            unscrew(0)
        if enemy_x == lamp_rect2.centerx and enemy_y <= CEILING:
            unscrew(1)
        if enemy_x == lamp_rect3.centerx and enemy_y <= CEILING:
            unscrew(2)
        if enemy_x == lamp_rect4.centerx and enemy_y <= CEILING:
            unscrew(3)
        if enemy_x == lamp_rect5.centerx and enemy_y <= CEILING:
            unscrew(4)
        if enemy_x == lamp_rect6.centerx and enemy_y <= CEILING:
            unscrew(5)
        if enemy_y <= CEILING and not player2_atLight:
            player2_climbing = False

        if not player2_climbing and enemy_y >= CEILING:
            enemy_y += Y_SPEED

        # show backgrounds
        flash = 255
        if not lightning:
            flash = 100  # sets brightness of sky without lightning
        screen.blit(bg_black, (0, 0))
        bg_clouds.set_alpha(flash)
        screen.blit(bg_clouds, (0, -220))
        if lightning:
            screen.blit(bg_lightning, (50, -280))
        bg_rain_surf.set_alpha(flash - 50)
        screen.blit(bg_rain_surf, (0, 0))
        rain_animation()
        screen.blit(bg_store, (0, 0))

        # player1 boundaries, get ladder
        if char_rect.right <= 0:  # transports to other side of screen
            player1_hasLadder = True  # gets a ladder off-screen
            ladder1_broken = False
            char_x = 1390
        if char_rect.left >= 1320:
            player1_hasLadder = True
            ladder1_broken = False
            char_x = -70
        if char_y >= FLOOR:
            char_y = FLOOR
        if char_y <= CEILING:
            char_y = CEILING

        # player2 boundaries
        if enemy_rect.right <= 0:  # transports to other side of screen
            player2_hasLadder = True  # gets a ladder off-screen
            enemy_x = 1390
        if enemy_rect.left >= 1320:
            player2_hasLadder = True
            enemy_x = -70
        if enemy_y >= FLOOR:
            enemy_y = FLOOR
        if enemy_y <= CEILING:
            enemy_y = CEILING

        screen.blit(ladder_player2, (ladder_player2_x, ladder_player2_y))
        screen.blit(enemy_surf, enemy_rect)
        screen.blit(ladder_player1, (ladder_player1_x, ladder_player1_y))
        screen.blit(char_surf, char_rect)

        # display light fixture(off) sprites
        screen.blit(lampOff1, lampOff_rect1)  # always visible
        screen.blit(lampOff2, lampOff_rect2)
        screen.blit(lampOff3, lampOff_rect3)
        screen.blit(lampOff4, lampOff_rect4)
        screen.blit(lampOff5, lampOff_rect5)
        screen.blit(lampOff6, lampOff_rect6)

        crow_anim()
        screen.blit(crow_surf, (0, 175))

        # this mess of code sets the parameters of lights on/off
        if lights_list[0]:
            fg_light1 = fg_light1_on
            lamp1.set_alpha(255)
        else:
            fg_light1 = fg_light1_off
            lamp1.set_alpha(0)

        if lights_list[1]:
            fg_light2 = fg_light2_on
            lamp2.set_alpha(255)
        else:
            fg_light2 = fg_light2_off
            lamp2.set_alpha(0)

        if lights_list[2]:
            fg_light3 = fg_light3_on
            lamp3.set_alpha(255)
        else:
            fg_light3 = fg_light3_off
            lamp3.set_alpha(0)

        if lights_list[3]:
            fg_light4 = fg_light4_on
            lamp4.set_alpha(255)
        else:
            fg_light4 = fg_light4_off
            lamp4.set_alpha(0)

        if lights_list[4]:
            fg_light5 = fg_light5_on
            lamp5.set_alpha(255)
        else:
            fg_light5 = fg_light5_off
            lamp5.set_alpha(0)

        if lights_list[5]:
            fg_light6 = fg_light6_on
            lamp6.set_alpha(255)
        else:
            fg_light6 = fg_light6_off
            lamp6.set_alpha(0)

        LIGHT_LEVEL = 80
        if lightning:
            LIGHT_LEVEL -= 180
        for i in lights_list:
            if not i:
                LIGHT_LEVEL += 34

        fg_light1_on.set_alpha(LIGHT_LEVEL)
        fg_light1_off.set_alpha(LIGHT_LEVEL)
        fg_light2_on.set_alpha(LIGHT_LEVEL)
        fg_light2_off.set_alpha(LIGHT_LEVEL)
        fg_light3_on.set_alpha(LIGHT_LEVEL)
        fg_light3_off.set_alpha(LIGHT_LEVEL)
        fg_light4_on.set_alpha(LIGHT_LEVEL)
        fg_light4_off.set_alpha(LIGHT_LEVEL)
        fg_light5_on.set_alpha(LIGHT_LEVEL)
        fg_light5_off.set_alpha(LIGHT_LEVEL)
        fg_light6_on.set_alpha(LIGHT_LEVEL)
        fg_light6_off.set_alpha(LIGHT_LEVEL)

        screen.blit(fg_light1, (0, 0))
        screen.blit(fg_light2, (220, 0))
        screen.blit(fg_light3, (440, 0))
        screen.blit(fg_light4, (660, 0))
        screen.blit(fg_light5, (880, 0))
        screen.blit(fg_light6, (1100, 0))

        screen.blit(lamp1, lamp_rect1)
        screen.blit(lamp2, lamp_rect2)
        screen.blit(lamp3, lamp_rect3)
        screen.blit(lamp4, lamp_rect4)
        screen.blit(lamp5, lamp_rect5)
        screen.blit(lamp6, lamp_rect6)

        # Flash white with lightning
        fg_white.set_alpha(50)
        if lightning:
            screen.blit(fg_white, (0, 0))

        lightning = False

        # Display winner
        if not WINNER:
            fade = 255
        if False not in lights_list:  # player one wins
            if not WINNER:
                player1win.play()
                gameTimer = 0
            gameTimer += 0.016
            WINNER = True
            fade -= 1.7
            screen.blit(DISPLAY_WINNER1, (230, 240))
            if gameTimer > 8:
                screen.blit(DISPLAY_PRESS_SPACE, (1000, 520))
            if not counter:
                POINTS1 += 1
                counter = True
        enemy_surf.set_alpha(fade)

        if True not in lights_list:  # player two wins
            if not WINNER:
                player2win.play()
                gameTimer = 0
            gameTimer += 0.016
            WINNER = True
            if not lightning:
                char_idle = char_dead
                enemy_idle = enemy_fall
                if player1_hasLadder:
                    if char_x <= 600:
                        char_x = ladder_player1_x + 140
                    else:
                        char_x = ladder_player1_x - 40
                enemy_x = char_x
                enemy_y = char_y
            screen.blit(DISPLAY_WINNER2, (230, 240))
            if gameTimer > 8:
                screen.blit(DISPLAY_PRESS_SPACE, (1000, 520))
            if not counter:
                POINTS2 += 1
                counter = True
        if WINNER:
            music.fadeout(100)

        SCORE1 = str(POINTS1)
        SCORE2 = str(POINTS2)

        DISPLAY_SCORE_1 = smallerFont.render(SCORE1, True, green)
        DISPLAY_SCORE_2 = smallerFont.render(SCORE2, True, red)

        screen.blit(DISPLAY_SCORE_1, (12, 2))
        screen.blit(DISPLAY_SCORE_2, (1290, 2))

        screen.blit(frame, (-300, -240))

        pygame.display.update()
        clock.tick(60)
