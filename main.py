# First attempt at a game using pygame
# Author: Matt Young
# Date created: March 16, 2023

import pygame
import math

# CONSTANTS
# sets the darkness of all lights out
LIGHT_LEVEL = 0
FLOOR = 530
CEILING = 395
X_SPEED = 8
Y_SPEED = 5
LADDER_Y_WALK = 415
LADDER_Y_CLIMB = 380

#  defaults
char_x = 100
char_y = FLOOR
ladder_x = -1
ladder_y = LADDER_Y_WALK

lights_list = [True, True, True, True, True, True]

player1_hasLadder = False
player2_hasLadder = False


pygame.init()

w, h = 1320, 600
screen = pygame.display.set_mode((w, h))
pygame.display.set_caption('Night Shift')  # Title of the window
clock = pygame.time.Clock()
test_font = pygame.font.Font(None, 100)

bg_black = pygame.Surface((w, h))
bg_black.fill('black')

bg_clouds = pygame.image.load('assets/clouds.png').convert()
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
lampOff1 = pygame.image.load('assets/bulb_off.png')
lampOff_rect1 = lampOff1.get_rect(midtop=(110, 0))

# bulb when off
lamp2 = pygame.image.load('assets/bulb_on.png').convert_alpha()
lamp_rect2 = lamp2.get_rect(midtop=(330, 0))
# bulb when on
lampOff2 = pygame.image.load('assets/bulb_off.png')
lampOff_rect2 = lampOff2.get_rect(midtop=(330, 0))

# bulb when off
lamp3 = pygame.image.load('assets/bulb_on.png').convert_alpha()
lamp_rect3 = lamp3.get_rect(topleft=(490, 0))
# bulb when on
lampOff3 = pygame.image.load('assets/bulb_off.png')
lampOff_rect3 = lampOff3.get_rect(topleft=(490, 0))

# bulb when off
lamp4 = pygame.image.load('assets/bulb_on.png').convert_alpha()
lamp_rect4 = lamp4.get_rect(topleft=(710, 0))
# bulb when on
lampOff4 = pygame.image.load('assets/bulb_off.png')
lampOff_rect4 = lampOff4.get_rect(topleft=(710, 0))

# bulb when off
lamp5 = pygame.image.load('assets/bulb_on.png').convert_alpha()
lamp_rect5 = lamp5.get_rect(topleft=(930, 0))
# bulb when on
lampOff5 = pygame.image.load('assets/bulb_off.png')
lampOff_rect5 = lampOff5.get_rect(topleft=(930, 0))

# bulb when off
lamp6 = pygame.image.load('assets/bulb_on.png').convert_alpha()
lamp_rect6 = lamp6.get_rect(topleft=(1150, 0))
# bulb when on
lampOff6 = pygame.image.load('assets/bulb_off.png')
lampOff_rect6 = lampOff6.get_rect(topleft=(1150, 0))


char_surf = pygame.image.load('assets/char_idle.png').convert_alpha()
char_surf_right = char_surf
char_surf_left = pygame.transform.flip(char_surf, flip_x=True, flip_y=False)

char_idle = pygame.image.load('assets/char_idle.png')
char_idle_right = char_idle
char_idle_left = pygame.transform.flip(char_idle_right,flip_x=True, flip_y=False)
char_walk1 = pygame.image.load('assets/char_walk1.png')
char_walk2 = pygame.image.load('assets/char_walk2.png')
char_walk = [char_walk1, char_walk2]
char_index = 0

ladder = pygame.image.load('assets/ladder.png').convert_alpha()
ladder_player1 = ladder
ladder_player2 = ladder

ladder_player1_left = pygame.transform.rotate(ladder_player1, angle=90)
ladder_player1_right = pygame.transform.flip(ladder_player1_left, flip_x=True, flip_y=False)

ladder_player1 = ladder_player1_right  # default starting direction


def rain_animation():
    global bg_rain_surf, bg_rain_index
    bg_rain_index += 0.2
    if bg_rain_index >= len(bg_rain):
        bg_rain_index = 0
    bg_rain_surf = bg_rain[int(bg_rain_index)]



def char_animation(direction='right'):
    global char_surf, char_index
    # walk
    char_index += 0.1
    if char_index >= len(char_walk):
        char_index = 0
    if direction == 'right':
        char_surf = char_walk[int(char_index)]
    elif direction == 'left':
        char_surf = pygame.transform.flip(char_walk[int(char_index)], flip_x=True, flip_y=False)
    else:
        char_surf = char_idle


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    # player 1 movement
    char_rect = char_surf.get_rect(midbottom=(char_x, char_y))
    char_surf = char_idle

    keys_pressed = pygame.key.get_pressed()
    if keys_pressed[pygame.K_ESCAPE]:
        exit()

    if keys_pressed[pygame.K_LEFT] and char_y == FLOOR:
        char_x -= X_SPEED
        char_animation('left')
        ladder_player1 = ladder_player1_left
        ladder_x = char_rect.x
        ladder_y = LADDER_Y_WALK
        char_idle = char_idle_left
    if keys_pressed[pygame.K_RIGHT] and char_y == FLOOR:
        char_x += X_SPEED
        char_animation('right')
        ladder_player1 = ladder_player1_right
        ladder_x = char_rect.x
        ladder_y = LADDER_Y_WALK
        char_idle = char_idle_right

    if keys_pressed[pygame.K_UP]:  # climb
        if player1_hasLadder:
            ladder_player1 = ladder

            ladder_x = char_rect.x + 15
            ladder_y = LADDER_Y_CLIMB
            char_y -= Y_SPEED
            if 80 <= char_x <= 140:
                char_x = lamp_rect1.centerx

    print(char_x)


    if keys_pressed[pygame.K_DOWN]:
        char_y += Y_SPEED

    screen.blit(bg_clouds, (0, -220))
    bg_rain_surf.set_alpha(100)
    screen.blit(bg_rain_surf, (0, 0))
    rain_animation()
    screen.blit(bg_store, (0, 0))

    # character sprites go here
    if char_rect.right <= 0:  # transports to other side of screen
        player1_hasLadder = True  # gets a ladder off-screen
        char_x = 1320
    if char_rect.left >= 1320:
        player1_hasLadder = True
        char_x = 0
    if char_y >= FLOOR:
        char_y = FLOOR
    if char_y <= CEILING:
        char_y = CEILING

    if player1_hasLadder:
        screen.blit(ladder_player1, (ladder_x, ladder_y))
    screen.blit(char_surf, char_rect)

    screen.blit(lampOff1, lampOff_rect1)  # always visible
    screen.blit(lampOff2, lampOff_rect2)
    screen.blit(lampOff3, lampOff_rect3)
    screen.blit(lampOff4, lampOff_rect4)
    screen.blit(lampOff5, lampOff_rect5)
    screen.blit(lampOff6, lampOff_rect6)

    # default shadow overlays.
    lamps = [lamp1, lamp2, lamp3, lamp4, lamp5, lamp6]

    lights_list[0] = True
    lights_list[1] = False
    lights_list[2] = False
    lights_list[3] = False

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

    LIGHT_LEVEL = 0
    for i in lights_list:

        if not i:
            LIGHT_LEVEL += 51

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

    pygame.display.update()
    clock.tick(60)
