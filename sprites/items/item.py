import pygame
from pygame.locals import *
from itertools import chain
import sprites.sprites_funcs as sfuncs

class Item(pygame.sprite.Sprite):
    def __init__(self, start_position, image, height=20, placeable=True):
        super(Item, self).__init__()

        # Creates surf and initial rect of surf
        self.image = image
        self.surf = pygame.image.load(image).convert_alpha()
        self.rect = self.surf.get_rect()

        # Sets height and width based off of the height, keeps ratio for resizing later
        self.start_height = height
        self.height = height
        self.width_over_height = self.rect.width / self.rect.height
        self.width = self.width_over_height * height

        # Positions item in the center of the mined resource
        start_position[0] -= 0.5 * self.width
        start_position[1] -= 0.5 * self.height

        # Creates surf and mask (for collision)
        self.surf = pygame.transform.scale(self.surf, (round(self.width),
                                                       round(self.height)))
        self.mask = pygame.mask.from_surface(self.surf)

        # Gets sprite rect and sets movement speed
        self.rect = self.surf.get_rect()
        self.rect.move_ip(*start_position)
        self.speed = 1

        # Clicked position and boolean for dragging in inventory
        self.clicked = False
        self.click_position = (0, 0)
        self.placeable = placeable


    # Move the background based on keypresses
    def update(self, keys, player, all_sprites, cooldowns, **kwargs):
        # If hasn't been collected
        if self not in chain(*kwargs["inventory_items"]):
            # Movement
            sfuncs.movement(self, player, keys)
            
           


    def collect_item(self, inventory_items, player):
        if self not in chain(*inventory_items):
            # Checks for collision
            offset_x = self.rect.x - player.rect.x
            offset_y = self.rect.y - player.rect.y
            if player.mask.overlap(self.mask, (offset_x, offset_y)):
                # If inventory isn't full
                if len([item for row in inventory_items for item in row]) < 12:
                    # Change size of item for inventory and hotbar
                    self.height = 32
                    self.width = self.width_over_height * self.height
                    self.surf = pygame.image.load(self.image).convert_alpha()
                    self.surf = pygame.transform.scale(self.surf, (round(self.width),
                                                                    round(self.height)))
                    self.mask = pygame.mask.from_surface(self.surf)
                    self.rect = self.surf.get_rect()

                    # Adds item to collected items
                    inventory_items[0].append(self)
                    return True

    
    # Method to move item back if player collides
    def move_back(self, pos_dif, **kwargs):
        # Moves the item back if it hasn't been collected
        if self not in chain(*kwargs["inventory_items"]):
             self.rect.move_ip(*pos_dif)

    def drop_item(self, player, inventory_items):
        self.height = self.start_height
        self.width = self.width_over_height * self.height
        self.surf = pygame.image.load(self.image).convert_alpha()
        self.surf = pygame.transform.scale(self.surf, (round(self.width),
                                                        round(self.height)))
        self.mask = pygame.mask.from_surface(self.surf)
        self.rect = self.surf.get_rect()
        self.rect.center = player.rect.center
        inventory_items[0].remove(self)

