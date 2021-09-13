import pygame
from pygame.locals import *
import sprites.sprites_funcs as sfuncs

class Background(pygame.sprite.Sprite):
    def __init__(self, start_position, width, height, image):
        super(Background, self).__init__()

        # Sets width of sprite based on screen width and height
        self.SCREEN_WIDTH = width
        self.SCREEN_HEIGHT = height

        # Creates surf 
        self.surf = pygame.image.load(image).convert()
        self.surf = pygame.transform.scale(self.surf, (round(self.SCREEN_WIDTH),
                                                       round(self.SCREEN_HEIGHT)))

        # Gets sprite rect and moves it to its start position
        self.rect = self.surf.get_rect()
        self.rect.move_ip(*start_position)

        # Movement speed
        self.speed = 1

        self.points = []
        self.map_grid()
    
    
    def map_grid(self):
        self.points = []
        for i in range(16 + 1):
            for j in range(16 + 1):
                self.points.append((self.rect.width / 16 * j + self.rect.topleft[0], self.rect.height / 16 * i + self.rect.topleft[1]))
    
    # Update method
    def update(self, keys, player, all_sprites, cooldowns, **kwargs):
        # Moves backgrounds so only 4 backgrounds are needed
        if self.rect.right < 0:
            self.rect.left = self.SCREEN_WIDTH - 1
        elif self.rect.left > self.SCREEN_WIDTH:
            self.rect.right = 1
        
        if self.rect.bottom < 0:
            self.rect.top = self.SCREEN_HEIGHT - 1

        elif self.rect.top > self.SCREEN_HEIGHT:
            self.rect.bottom = 1

        # Movement
        sfuncs.movement(self, player, keys)

        self.map_grid()


    # Method to move sprite back after collision
    def move_back(self, pos_dif, **kwargs):
        self.rect.move_ip(*pos_dif)
        self.map_grid()

    
        
