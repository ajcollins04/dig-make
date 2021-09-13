import pygame
from pygame.locals import *

class Inventory(pygame.sprite.Sprite):
    def __init__(self, start_position, inventory_bezels, height=200, image=r"sprites\inventory\assets\inventory.png"):
        super(Inventory, self).__init__()

        # Creates surf and initial rect of surf
        self.surf = pygame.image.load(image).convert_alpha()
        self.rect = self.surf.get_rect()

        # Sets height and width based off of the height
        self.height = height
        self.width = (self.rect.width / self.rect.height) * height

        # Scales the surf to specified height and width
        self.surf = pygame.transform.scale(self.surf, (round(self.width),
                                                       round(self.height)))

        # Gets sprite rect and sets movement speed
        self.rect = self.surf.get_rect()
        self.rect.move_ip(*start_position)
        self.inventory_bezels = inventory_bezels

        self.selected = 1
    
    def update(self, keys, **kwargs):
        for count, key in enumerate([K_1, K_2, K_3, K_4]):
            if keys[key]:
                self.selected = count + 1

    def draw_numbers(self, screen, font):
        for i in range(4):
            if (i + 1) == self.selected: color = (255, 0, 0)
            else: color = (0, 0, 0)
            text = font.render(f'{i + 1}', False, color)
            try:
                bezels = self.inventory_bezels[i]["x"]
            except:
                bezels = self.inventory_bezels[i]
                
            screen.blit(text, (self.rect.topleft[0] + bezels + (60 * i) + 6 ,
                               self.rect.topleft[1] + 8))
