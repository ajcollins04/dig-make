import pygame
from pygame.locals import *
import sprites.items.item as item
import sprites.backgrounds.backgrounds as backgrounds
import sprites.sprites_funcs as sfuncs


class Resource(pygame.sprite.Sprite):
    def __init__(self, start_position, height=100, image=r"sprites\resource\assets\tree1.png", init_health=4, 
                 item_drop=r"sprites\items\assets\wood.png", resource_name="Tree"):
        super(Resource, self).__init__()

        # Creates surf and initial rect of surf
        self.surf = pygame.image.load(image).convert_alpha()
        self.rect = self.surf.get_rect()

        # Sets height and width based off of the height
        self.height = height
        self.width = (self.rect.width / self.rect.height) * height

        # Scales the surf to specified height and width
        self.surf = pygame.transform.scale(self.surf, (round(self.width),
                                                       round(self.height)))

        # Sets mask for collision
        self.mask = pygame.mask.from_surface(self.surf)

        # Gets sprite rect and sets movement speed
        self.rect = self.surf.get_rect()
        self.rect.move_ip(*start_position)
        self.speed = 1

        # Creates resource hitbox (for mining)
        self.hitbox = pygame.Rect(self.rect.left - 10, self.rect.top - 10, self.rect.width + 20, self.rect.height + 20)

        # Collision boolean and position for stopping player movement
        self.collision = False
        self.collision_pos = ()

        # Max health and current health (for mining)
        self.max_health = init_health
        self.health = init_health

        # The name of the resource and the image of the item that is dropped
        self.item_drop = item_drop
        self.resource_name = resource_name

    # Update method
    def update(self, keys, player, all_sprites, cooldowns, **kwargs):
        # Removes sprite and replaces with dropped item if resource is mined
        if self.health <= 0:
            all_sprites.append(
                item.Item(list(self.rect.center), self.item_drop))
            all_sprites.remove(self)
            self.kill()

        # Resets collision to false
        self.collision = False

        # Sets old sprite position before movement
        old_topleft = self.rect.topleft

        # Movement
        sfuncs.movement(self, player, keys)


        # Checks for collision
        offset_x = self.rect.x - player.rect.x
        offset_y = self.rect.y - player.rect.y
        if player.mask.overlap(self.mask, (offset_x, offset_y)):
            self.collision = True
            self.collision_pos = (old_topleft[0] - self.rect.topleft[0], old_topleft[1] - self.rect.topleft[1])
        else:
            # Sets new hitbox position
            self.hitbox = pygame.Rect(self.rect.left - 10, self.rect.top - 10, self.rect.width + 20, self.rect.height + 20)


    # Method to move tree back if player collides
    def move_back(self, pos_dif, **kwargs):
        self.rect.move_ip(*pos_dif)


    # Draws health bar
    def blit_health(self, screen):
        if self.health < self.max_health:
            pygame.draw.rect(screen, [0, 0, 0], [self.rect.left, self.rect.bottom, self.rect.width, 10], 0)
            pygame.draw.rect(screen, [255, 0, 0], [self.rect.left + 2, self.rect.bottom + 2, 
                             int(self.health / self.max_health * (self.rect.width - 4)), 6], 0)
