import pygame # Pygame is not a built-in python package, so a 'pip install pygame' may be needed (version used - 2.1.2)
import os
import sys
import random
import time

class Fighter(object):
    def __init__(self, fighter_name, fighter_information, platform_position, player):
        self.fighter_name = fighter_name
        self.fighter_information = fighter_information

        self.animations = [] # [Idle, Attack1, Attack2, Attack3, Jump, Fall, Run, Hit, Death, Frame width, Frame height]
        self.animation_names = ['Idle', 'Attack1', 'Attack2', 'Attack3', 'Jump', 'Fall', 'Run', 'Hit', 'Death']
        self.animation_steps = fighter_information[f'{fighter_name}_sprite_steps']
        self.sprite_scale = self.fighter_information[f'{self.fighter_name}_hitbox'][4]

        for x in range(0,9): # Split all animation frames and append them to an array
            self.spritesheet_loop = pygame.image.load(os.path.join(sourcedirectory, f'Data/Sprites/{self.fighter_name}/{self.animation_names[x]}.png')).convert_alpha()
            self.animation_loop = self.create_animation(self.animation_steps[x], self.spritesheet_loop, self.fighter_information[f'{self.fighter_name}_spriteframe_info'][0], self.fighter_information[f'{self.fighter_name}_spriteframe_info'][1], self.sprite_scale)
            self.animations.append(self.animation_loop)

        self.positionx = 0
        self.positiony = platform_position
        self.gravity = 3
        self.vely = 0
        self.flip = False

        self.hitbox = pygame.Rect(self.positionx, self.positiony, self.fighter_information[f'{self.fighter_name}_hitbox'][2] * self.sprite_scale, self.fighter_information[f'{self.fighter_name}_hitbox'][3] * self.sprite_scale) # [chr]_hitbox: [left, top, width, height]
        self.attacking_hitbox = pygame.Rect(0, 0, 0, 0)
        self.movement_speed = 7

        self.attacking = False
        self.attacking_cooldown = 450
        self.attacking_timer = pygame.time.get_ticks()

        self.hit = False
        self.dohit = False
        self.jump = False
        self.dead = False
        self.changed_animation = False
        self.pause_animation = False

        self.hitbox_color = (0, 255, 0) # debugging
        self.platform_location = platform_position
        
        self.player = player
        self.round_finished = False
        self.health = 100

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

    def action(self, surface, enemy_hitbox, enemy_attacking):
        playerinput_jump = [pygame.K_w, pygame.K_UP]
        playerinput_left = [pygame.K_a, pygame.K_LEFT]
        playerinput_right = [pygame.K_d, pygame.K_RIGHT]
        playerinput_attack1 = [pygame.K_e, pygame.K_KP1]
        playerinput_attack2 = [pygame.K_q, pygame.K_KP2]
        playerinput_attack3 = [pygame.K_f, pygame.K_KP3]

        input = pygame.key.get_pressed() #input

        # hit
        if self.hit == True and self.dead == False: # check if character has been hit
            if self.dohit == False:
                self.current_animation = 7 # change to hit animation
                self.hit = False # reset the hit variable
                self.dohit = True # extra variable necessary in order to complete the animation and not be stuck in a constant hit loop
                self.health -= 10
        
        # death
        if self.health <= 0: # if the character is below or equal to 0 health
            if self.dead == False:
                self.current_animation = 8 # change to death animation
                self.current_animation_step = 0 # reset animation step
                self.dead = True
        else:    
            # attack
            if pygame.time.get_ticks() - self.attacking_timer > self.attacking_cooldown: # check if the attack cooldown has finished
                if input[playerinput_attack1[self.player]]:
                    if self.jump == True: # cancel the attack if the character is in the air
                        pass
                    else:
                        if self.attacking == True or self.dohit == True: # cancel the attack if the character is already attacking
                            pass
                        else:
                            self.attacking = True
                            self.current_animation = 1 # change to first attack animation
                            self.current_animation_step = 0 # reset the animation step

                if input[playerinput_attack2[self.player]]:
                    if self.jump == True: # cancel the attack if the character is in the air
                        pass
                    else:
                        if self.attacking == True or self.dohit == True: # cancel the attack if the character is already attacking or being hit
                            pass
                        else:
                            self.attacking = True
                            self.current_animation = 2 # change to second attack animation
                            self.current_animation_step = 0 # reset the animation step

            # movement
            if input[playerinput_jump[self.player]]:
                if self.jump == True or self.dohit == True or self.attacking == True: # cancel the jump if the character is in the air, attacking, or being hit
                    pass
                else:
                    self.vely -= 40 # set a negative velocity so the character propels upwards
                    self.jump = True
                    self.current_animation = 4 # change to jump animation

            if input[playerinput_left[self.player]] or input[playerinput_right[self.player]]:
                if self.attacking == True or self.dohit == True: # cancel movement if the character is attacking, or being hit
                    pass
                else:
                    if input[playerinput_left[self.player]]:
                        if self.hitbox.left <= 0: # check is character has hit the left border
                            pass
                        else:
                            self.positionx -= self.movement_speed
                            if self.jump == False: # check if character is on the ground
                                self.current_animation = 6 # change to running animation
                    if input[playerinput_right[self.player]]:
                        if self.hitbox.right >= swidth: # check is character has hit the right border
                            pass
                        else:
                            self.positionx += self.movement_speed
                            if self.jump == False:
                                self.current_animation = 6
            else:
                if self.attacking == True or self.jump == True or self.dohit == True: # check if the character is performing an action
                    pass
                else:
                    self.current_animation = 0 # change to idle animation
        
        self.vely += self.gravity # apply gravity
        if self.vely >= 0: # check if character has positive velocity
            if self.jump == True and self.dead == False: # check if character has jumped
                self.current_animation = 5 # change to falling animation
                self.changed_animation = True

        self.positiony += self.vely # move character's position
        if self.positiony >= self.platform_location: # check if the character is on the ground
            self.vely = 0 # reset velocity
            if self.jump == True:
                self.jump = False # character is not jumping if their feet is on the ground
                self.current_animation = 0 # change to idle animation
                self.changed_animation = True
            self.positiony = self.platform_location

        if enemy_hitbox.centerx > self.hitbox.centerx: # check if the character should face in the opposite direction
            self.flip = False
        else:
            self.flip = True

        self.hitbox.left, self.hitbox.bottom = self.positionx, self.positiony # moves the character's hitbox

        # set sprite
        self.animation_done = self.current_animation_step > self.fighter_information[f'{self.fighter_name}_sprite_steps'][self.current_animation] - 1 # check if the animation is finished
        if self.animation_done == True:
            if self.attacking == True and self.dead == False:
                self.current_animation = 0 # change to idle animation
                self.current_animation_step = 0 # reset the animation step to 0
            elif self.dead == False:
                self.current_animation_step = 0 # reset the animation step to 0
            elif self.dead == True:
                self.current_animation_step -= 1
                self.pause_animation = True
            
        if enemy_attacking == False and self.dohit == True and self.dead == False:
            self.hit = False
            self.dohit = False
            self.current_animation = 0
            
        sprite_surface = self.animations[self.current_animation][self.current_animation_step] # grabs the current frame
        if self.dead == False:
            sprite_surface = pygame.transform.flip(sprite_surface, self.flip, False) # flips the frame if necessary

        if self.pause_animation == False: # if the animation doesn't need to be puased
            if pygame.time.get_ticks() - self.update_tick > self.animation_delay: # check if animation needs to progress
                self.current_animation_step += 1 # move to the next frame
                self.update_tick = pygame.time.get_ticks() # reset the animation timer

        # draw
        # pygame.draw.rect(surface, self.hitbox_color, self.hitbox) # draws the character's hitbox
        if self.attacking == True: # check if the character is attacking
            if self.animation_done == True: # check if the attacking animation has finished
                self.attacking_timer = pygame.time.get_ticks() # reset the cooldown timer
                self.attacking = False # player is no longer attacking
                self.attacking_hitbox = pygame.Rect(0, 0, 0, 0) # reset the attacking hitbox
            else:
                self.attacking_hitbox = pygame.Rect(0, 0, (self.fighter_information[f'{self.fighter_name}_atk_hitbox'][0] * self.sprite_scale), (self.fighter_information[f'{self.fighter_name}_atk_hitbox'][1] * self.sprite_scale)) # define the width and height of the attacking hitbox

                if self.flip == True: # flip the attacking hitbox
                    self.attacking_hitbox.right = self.hitbox.right
                else:
                    self.attacking_hitbox.left = self.hitbox.left

                self.attacking_hitbox.bottom = self.hitbox.bottom # the attacking hitbox is not allowed to fly to space
                # pygame.draw.rect(surface, self.hitbox_color, self.attacking_hitbox) # draws the attacking hitbox

        sprite_rect = sprite_surface.get_rect() # grabs the Rect of the sprite
        sprite_rect.center = (self.hitbox.center[0] + self.fighter_information[f'{self.fighter_name}_offset'][0], self.hitbox.center[1] + self.fighter_information[f'{self.fighter_name}_offset'][1]) # offsets the sprite in order for it to be in it's hitbox

        surface.blit(sprite_surface, sprite_rect) # blit character to the screen

        if self.dead == True and self.animation_done == True: # if the character has died and have finished their animation
            self.round_finished = True


global sourcedirectory
sourcedirectory = os.path.dirname(os.path.abspath(__file__)) # grabs directory of the file

pygame.init()
global swidth, sheight
swidth, sheight = 740, 740
screen = pygame.display.set_mode((swidth, sheight)) # width, height of the screen
pygame.scrap.init() ### Scrap can only be initialised after the display set mode command has been done
# pygame.key.set_repeat(500, 50) # allows keys to be held


fontstyle = pygame.font.SysFont(None, 50) # Defaults to a size 50 font
color = (255, 255, 255)

clock = pygame.time.Clock()
FPS = 60

backgrounds = ['sunset.jpg', 665, 'grassland.png', 620, 'coast.png', 630]
random_background = random.choice([0, 2, 4])
current_background = pygame.image.load(os.path.join(sourcedirectory, f'Data/Background/{backgrounds[random_background]}')).convert_alpha()


# Sprite information for each character
# [chr]_sprite_steps: [Idle, Attack1, Attack2, Attack3, Jump, Fall, Run, Hit, Death, Frame width, Frame height]
# [chr]_spriteframe_info: [Frame width, frame height]
# [chr]_hitbox: [left, top, width, height, scale]
# [chr]_atk_hitbox: [width, height]
# [chr]_offset: [x offset, y offset]
fighter_information = {
    'squire_sprite_steps': [10, 4, 4, 4, 2, 2, 6, 3, 9],
    'squire_spriteframe_info': [135, 135],
    'squire_hitbox': [56, 48, 23, 37, 3],
    'squire_atk_hitbox': [67, 48],
    'squire_offset': [0, 0],

    'huntress_sprite_steps': [8, 5, 5, 7, 2, 2, 8, 3, 8],
    'huntress_spriteframe_info': [150, 150],
    'huntress_hitbox': [65, 58, 17, 38, 3],
    'huntress_atk_hitbox': [60, 65],
    'huntress_offset': [2, -8],

    'nomad_sprite_steps': [10, 7, 7, 8, 3, 3, 8, 3, 7],
    'nomad_spriteframe_info': [162, 162],
    'nomad_hitbox': [72, 56, 20, 44, 3.3],
    'nomad_atk_hitbox': [60, 50],
    'nomad_offset': [-4, 7],

    'shinobi_sprite_steps': [8, 6, 6, 4, 2, 2, 8, 4, 6],
    'shinobi_spriteframe_info': [200, 200],
    'shinobi_hitbox': [87, 76, 23, 45, 2.8],
    'shinobi_atk_hitbox': [90, 50],
    'shinobi_offset': [0, 2]
}

def draw_objects(current_background, current_background_rect):
    screen.fill((255, 255, 255))
    screen.blit(current_background, current_background_rect) # add the background

player1score, player2score = 0, 0
game_active = True
while (game_active == True):
    round = True
    endround = False
    player1 = Fighter('nomad', fighter_information, backgrounds[random_background + 1], player=0)
    player1.positionx = 150
    player2 = Fighter('squire', fighter_information, backgrounds[random_background + 1], player=1)
    player2.positionx = 590

    while (round == True):
        clock.tick(FPS)
 
        draw_objects(current_background, current_background.get_rect())

        player1.action(screen, player2.hitbox, player2.attacking)
        player2.action(screen, player1.hitbox, player1.attacking)

        # if any player attacks, check to see if the attack has landed
        if player1.attacking_hitbox.colliderect(player2.hitbox):
            player2.hit = True
        elif player2.attacking_hitbox.colliderect(player1.hitbox):
            player1.hit = True

        playerhealth = [player1.health, player2.health]
        for x in range(2):
            messageid = fontstyle.render(str(playerhealth[x]), True, color)
            message_rectid = messageid.get_rect(topleft = ((x+1) * 200, 300)) # Message container
            screen.blit(messageid, message_rectid)

        if player1.round_finished == True or player2.round_finished == True or endround == True:
            if player1.round_finished == True:
                player1.round_finished = False
                player2score += 1
                endround_timer = pygame.time.get_ticks()
            elif player2.round_finished == True:
                player2.round_finished = False
                player1score += 1
                endround_timer = pygame.time.get_ticks()
            endround = True

            if pygame.time.get_ticks() - endround_timer > 5000:
                round = False
            messageid = fontstyle.render('ROUND END', True, color)
            message_rectid = messageid.get_rect(topleft = (300, 100)) # Message container
            screen.blit(messageid, message_rectid)



        pygame.display.flip() # update the screen    
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                game_active = False
                pygame.quit()
                sys.exit