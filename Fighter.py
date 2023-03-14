import pygame # Pygame is not a built-in python package, so a 'pip install pygame' may be needed (version used - 2.1.2)
import os
import sys
import random

class Fighter(object):
    def __init__(self, fighter_name, fighter_information, player):
        self.fighter_name = fighter_name
        self.fighter_information = fighter_information

        self.animations = [] # [Idle, Attack1, Attack2, Attack3, Jump, Fall, Run, Hit, Death, Frame width, Frame height]
        self.animation_names = ['Idle', 'Attack1', 'Attack2', 'Attack3', 'Jump', 'Fall', 'Run', 'Hit', 'Death']
        self.animation_steps = fighter_information[f'{fighter_name}_sprite_steps']
        self.sprite_scale = 3

        for x in range(0,9):
            self.spritesheet_loop = pygame.image.load(os.path.join(sourcedirectory, f'Data/Sprites/{self.fighter_name}/{self.animation_names[x]}.png')).convert_alpha()
            self.animation_loop = self.create_animation(self.animation_steps[x], self.spritesheet_loop, self.fighter_information[f'{self.fighter_name}_spriteframe_info'][0], self.fighter_information[f'{self.fighter_name}_spriteframe_info'][1], self.sprite_scale)
            self.animations.append(self.animation_loop)

        self.positionx = 0
        self.positiony = 300
        self.gravity = 3
        self.vely = 0
        self.flip = False

        self.hitbox = pygame.Rect(self.positionx, self.positiony, self.fighter_information[f'{self.fighter_name}_hitbox'][2] * self.sprite_scale, self.fighter_information[f'{self.fighter_name}_hitbox'][3] * self.sprite_scale) # [chr]_hitbox: [left, top, width, height]
        self.movement_speed = 7

        self.attacking = False
        self.jump = False
        self.dead = False
        self.changed_animation = False

        self.hitbox_color = (0, 255, 0) # debugging
        self.platform_location = 400
        
        self.player = player

        self.current_animation = 0
        self.current_animation_step = 0
        self.update_tick = pygame.time.get_ticks()
        self.animation_delay = 100
        

    def create_animation(self, steps, sheet, frame_width, frame_height, scale): # Split a spritesheet into individual frames
        def get_image(sheet, frame):
            image = pygame.Surface((frame_width, frame_height), pygame.SRCALPHA)
            image.blit(sheet, (0, 0), ((frame * frame_width), 0, frame_width, frame_height))
            return image

        animation_list = []
        for x in range(steps):
            cropped_image = get_image(sheet, x)
            cropped_image = pygame.transform.scale(cropped_image, (frame_width * scale, frame_height * scale))
            animation_list.append(cropped_image)
        return animation_list

    def action(self, surface, enemy_hitbox):
        playerinput_jump = [pygame.K_w, pygame.K_UP]
        playerinput_left = [pygame.K_a, pygame.K_LEFT]
        playerinput_right = [pygame.K_d, pygame.K_RIGHT]
        playerinput_attack1 = [pygame.K_e, pygame.K_KP1]
        playerinput_attack2 = [pygame.K_q, pygame.K_KP2]
        playerinput_attack3 = [pygame.K_f, pygame.K_KP3]

        input = pygame.key.get_pressed() #input
        # attack
        if input[playerinput_attack1[self.player]]:
            if self.jump == True:
                pass
            else:
                if self.attacking == True:
                    pass
                else:
                    self.attacking = True
                    self.current_animation = 1
                    self.current_animation_step = 0

        if input[playerinput_attack2[self.player]]:
            if self.jump == True:
                pass
            else:
                if self.attacking == True:
                    pass
                else:
                    self.attacking = True
                    self.current_animation = 2
                    self.current_animation_step = 0

        # movement
        if input[playerinput_jump[self.player]]:
            if self.jump == True:
                pass
            else:
                self.vely -= 40
                self.jump = True
                self.current_animation = 4

        if input[playerinput_left[self.player]] or input[playerinput_right[self.player]]:
            if self.attacking == True:
                pass
            else:
                if input[playerinput_left[self.player]]:
                    if self.hitbox.left <= 0:
                        pass
                    else:
                        self.positionx -= self.movement_speed
                        if self.jump == False:
                            self.current_animation = 6
                if input[playerinput_right[self.player]]:
                    if self.hitbox.right >= swidth:
                        pass
                    else:
                        self.positionx += self.movement_speed
                        if self.jump == False:
                            self.current_animation = 6
        else:
            if self.attacking == True or self.jump == True:
                pass
            else:
                self.current_animation = 0
        
        self.vely += self.gravity
        if self.vely >= 0:
            if self.jump == True:
                self.current_animation = 5
                self.changed_animation = True

        self.positiony += self.vely
        # print(f'before: {self.positiony}')
        if self.positiony >= self.platform_location:
            # print(f'calc: {self.hitbox.bottom + self.positiony} > {sheight - self.platform_location}')
            # print(f'player {self.player} hitbox bottom: {self.hitbox.bottom}')
            self.vely = 0
            if self.jump == True:
                self.jump = False
                self.current_animation = 0
                self.changed_animation = True
            self.positiony = self.platform_location

        if enemy_hitbox.centerx > self.hitbox.centerx:
            self.flip = False
        else:
            self.flip = True

        self.hitbox.left, self.hitbox.bottom = self.positionx, self.positiony

        # set sprite
        self.animation_done = self.current_animation_step > self.fighter_information[f'{self.fighter_name}_sprite_steps'][self.current_animation] - 1
        if self.animation_done == True:
            if self.attacking == True:
                self.current_animation = 0
            self.current_animation_step = 0

        sprite_surface = self.animations[self.current_animation][self.current_animation_step]
        sprite_surface = pygame.transform.flip(sprite_surface, self.flip, False)

        if pygame.time.get_ticks() - self.update_tick > self.animation_delay:
            self.current_animation_step += 1
            self.update_tick = pygame.time.get_ticks()

        # draw
        pygame.draw.rect(surface, self.hitbox_color, self.hitbox)
        if self.attacking == True:
            if self.animation_done == True:
                self.attacking = False
            else:
                self.attacking_hitbox = pygame.Rect(self.hitbox.left - (self.hitbox.width * self.flip), self.hitbox.top - self.hitbox.height, (self.hitbox.width * 2), (self.hitbox.height * 2))
                pygame.draw.rect(surface, self.hitbox_color, self.attacking_hitbox)

        sprite_rect = sprite_surface.get_rect()
        sprite_rect.center = (self.hitbox.center[0] + self.fighter_information[f'{self.fighter_name}_offset'][0], self.hitbox.center[1] + self.fighter_information[f'{self.fighter_name}_offset'][1])

        surface.blit(sprite_surface, sprite_rect)


global sourcedirectory
sourcedirectory = os.path.dirname(os.path.abspath(__file__))

pygame.init()
global swidth, sheight
swidth, sheight = 740, 740
screen = pygame.display.set_mode((swidth, sheight)) # width, height of the screen
pygame.scrap.init() ### Scrap can only be initialised after the display set mode command has been done
# pygame.key.set_repeat(500, 50) # allows keys to be held

clock = pygame.time.Clock()
FPS = 60

backgrounds = ['construction', 'forest', 'japan_coast']
random_background = random.randint(0, 2)
current_background = pygame.image.load(os.path.join(sourcedirectory, f'Data/Background/{backgrounds[random_background]}.gif')).convert_alpha()
current_background_rect = current_background.get_rect()
current_background_rect.midbottom = ((swidth / 2), 500)


# Sprite information for each character
# [chr]_sprite_steps: [Idle, Attack1, Attack2, Attack3, Jump, Fall, Run, Hit, Death, Frame width, Frame height]
# [chr]_spriteframe_info: [Frame width, frame height]
# [chr]_hitbox: [left, top, width, height]
fighter_information = {
    'squire_sprite_steps': [10, 4, 4, 4, 2, 2, 6, 3, 9],
    'squire_spriteframe_info': [135, 135],
    'squire_hitbox': [56, 48, 23, 37],
    'squire_offset': [0, 0],

    'huntress_sprite_steps': [8, 5, 5, 7, 2, 2, 8, 3, 8],
    'huntress_spriteframe_info': [150, 150],
    'huntress_hitbox': [65, 58, 17, 38],
    'huntress_offset': [2, -8],

    'nomad_sprite_steps': [10, 7, 7, 8, 3, 3, 8, 3, 7],
    'nomad_spriteframe_info': [162, 162],
    'nomad_hitbox': [72, 56, 20, 44],
    'nomad_offset': [-4, 7],

    'shinobi_sprite_steps': [8, 6, 6, 4, 2, 2, 8, 4, 6],
    'shinobi_spriteframe_info': [200, 200],
    'shinobi_hitbox': [87, 76, 23, 45],
    'shinobi_offset': [0, 2]
}


player1 = Fighter('huntress', fighter_information, player=0)
player1.positionx = 200
# player1.hitbox.bottom = 465

player2 = Fighter('squire', fighter_information, player=1)
player2.positionx = 400
player2.hitbox_color = (255, 0, 255)
# player2.hitbox.bottom = 465

game_active = True
while (game_active == True):
    clock.tick(FPS)

    screen.blit(current_background, current_background_rect)

    player1.action(screen, player2.hitbox)
    player2.action(screen, player1.hitbox)

    pygame.display.flip()
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            game_active = False
            pygame.quit()
            sys.exit