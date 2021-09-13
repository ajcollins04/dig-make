import pygame
from pygame.locals import *
from os import listdir
import sprites.sprites_funcs as sfuncs

# Function to get all files in a directory 
def filesIn(dir):
    return [f for f in listdir(dir)]

class Player(pygame.sprite.Sprite):
    def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT):
        super(Player, self).__init__()

        # Animation dictionaries 
        self.walking = {
            "right": filesIn(r"sprites\player\assets\walking\right"),
            "left": filesIn(r"sprites\player\assets\walking\left"),
            "up": filesIn(r"sprites\player\assets\walking\up"),
            "down": filesIn(r"sprites\player\assets\walking\down")
        }

        self.hitting = {
            "right": filesIn(r"sprites\player\assets\hitting\right"),
            "left": filesIn(r"sprites\player\assets\hitting\left"),
            "up": filesIn(r"sprites\player\assets\hitting\up"),
            "down": filesIn(r"sprites\player\assets\hitting\down")
        }

        # Direction and animation style
        self.direction = "right"
        self.animation_style = "walking"

        # Creating the player surf
        self.image_file = self.walking[self.direction][0]
        self.surf = pygame.image.load(f"sprites\\player\\assets\\{self.animation_style}\\{self.direction}\\{self.image_file}").convert_alpha()

        self.height = 60
        self.idle_height = 60
        self.width = int(13/22 * self.height)
        
        # Player surf scaling and setting the mask (for collision)
        self.surf = pygame.transform.scale(self.surf, (self.width, self.height))
        self.mask = pygame.mask.from_surface(self.surf)

        # Surf box setting and positioning
        self.rect = self.surf.get_rect()
        self.pos = self.x, self.y = [SCREEN_WIDTH / 2 - (self.width / 2), SCREEN_HEIGHT / 2 - (self.height / 2)]
        self.idle_pos = self.pos[::]
        self.rect.move_ip(*self.pos)

        # Current Animation and idle boolean
        self.current_iter = iter(self.walking[self.direction])

        # Mining cooldown
        self.cooldown = False

    # Method for changing surf image
    def change_surf(self, image_url, ratio=(15/22), height=60):
        self.surf = pygame.image.load(f"sprites\\player\\assets\\{self.animation_style}\\{self.direction}\\{image_url}").convert()
        self.width = int(self.surf.get_width() / self.surf.get_height() * self.height)
        self.surf = pygame.transform.scale(self.surf, (self.width, self.height))
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect()
        self.rect.move_ip(*self.pos)

    # Method for checking if the sprite is facing in the same direction for animation
    def check_direction(self):
        if self.image_file not in self.walking[self.direction]:
            self.animation()
            

    # Update method
    def update(self, keys, _, all_sprites, cooldowns, **kwargs):
        # Gets all collisions
        collision = sfuncs.rect_collision(self, all_sprites)

        # Mining
        if keys[K_SPACE] and "Resource" in collision and self.cooldown == False:
            if self.facing(collision["Resource"][0]):
                # Makes sure player is placed correctly
                if self.direction == "left":
                    self.pos[0] -= 22
                if self.direction == "down":
                    self.height = 71

                # Mining cooldown
                self.cooldown = True
                pygame.time.set_timer(cooldowns["HITCOOLDOWN"], 1000)

                # Decrements sprite health on hit
                collision["Resource"][0].health -= 1

                # Plays hitting animation
                self.current_iter = iter(self.hitting[self.direction])
                self.animation_style = "hitting"
                self.animation()

        if self.animation_style == "hitting":
            pass
        # Movement
        elif keys[K_d] or keys[K_a]:
            self.animation_style = "walking"
            if keys[K_d]:
                self.direction = "right"
                self.check_direction()

            if keys[K_a]:
                self.direction = "left"
                self.check_direction()       
        elif keys[K_w] or keys[K_s]:
            self.animation_style = "walking"
            self.not_idle = True
            if keys[K_w]:
                self.direction = "up"
                self.check_direction()
            if keys[K_s]:
                self.direction = "down"
                self.check_direction()
        else:
            self.reset_to_idle()



    # Method to see if you are facing toward a sprite (used in mining)
    def facing(self, sprite):
        if (self.rect.bottom > sprite.rect.bottom - 5 and self.direction == "up") or \
           (self.rect.top < sprite.rect.top + 5 and self.direction == "down") or \
           (self.rect.left < sprite.rect.left + 5 and self.direction == "right") or \
           (self.rect.right > sprite.rect.right - 5 and self.direction == "left"):
            return True
        return False

    # Method to set the animation back to idle
    def reset_to_idle(self):
        self.pos = self.idle_pos[::]
        self.height = self.idle_height
        self.animation_style = "walking"
        self.current_iter = iter(self.walking[self.direction])
        self.image_file = next(self.current_iter)
        self.change_surf(self.image_file)


    # Method for animation
    def animation(self):
        try:
            if self.animation_style == "walking":
                if self.image_file not in self.walking[self.direction]:
                    self.current_iter = iter(self.walking[self.direction])


            self.image_file = next(self.current_iter)
            self.change_surf(self.image_file)

            
        except StopIteration:
            # Reset to idle
            self.reset_to_idle()