import pygame
from pygame.locals import *
import random
import sprites.resource.resource as resource
import math


# Function to move all sprites back if there is collision
def stop_movement(all_sprites, inventory_items):
    for sprite in all_sprites:
        if type(sprite).__name__ != "Background" and type(sprite).__name__ != "Player" and hasattr(sprite, "collision"):
            if sprite.collision:
                for move_sprite in all_sprites:
                    if hasattr(move_sprite, "move_back"):
                        move_sprite.move_back(sprite.collision_pos, inventory_items=inventory_items)
                break


# Function to test if there is a sprite between the specified coordinates
def on_screen(sprite, x, y, width, height):
    if sprite.rect.right >= x and sprite.rect.bottom >= y and sprite.rect.left <= x + width and sprite.rect.top <= y + height:
        return True
    return False


# Function for random sprite generation 
def sprite_generation(resource_name, SCREEN_WIDTH, SCREEN_HEIGHT, all_sprites, resource_amount, *args):
    # Loops through the 8 chunks surrounding the player's chunk
    for i in ((-SCREEN_WIDTH, -SCREEN_HEIGHT), (0, -SCREEN_HEIGHT), (SCREEN_WIDTH, -SCREEN_HEIGHT),
              (-SCREEN_WIDTH, 0), (SCREEN_WIDTH, 0),
              (-SCREEN_WIDTH, SCREEN_HEIGHT), (0, SCREEN_HEIGHT), (SCREEN_WIDTH, SCREEN_HEIGHT)):

        # Gets the number of sprites in that chunk
        sprites_in_chunk = 0
        for sprite in all_sprites:
            if type(sprite).__name__ == "Resource" and on_screen(sprite, i[0], i[1], SCREEN_WIDTH, SCREEN_HEIGHT):
                if sprite.resource_name == resource_name:
                    sprites_in_chunk += 1

        # If there are less than two sprites in that chunk
        if sprites_in_chunk < resource_amount:

            # Create a new sprite
            needs_sprite = True
            while needs_sprite:
                new_pos = (random.randint(
                    i[0], i[0] + SCREEN_WIDTH - 100), random.randint(i[1], i[1] + SCREEN_HEIGHT - 100))
                new_sprite = resource.Resource(new_pos, *args)

                for sprite in all_sprites:
                    needs_sprite = False
                    if type(sprite).__name__ == "Resource":

                        # Make sure the sprite isn't on top of another sprite 
                        if pygame.sprite.collide_rect(new_sprite, sprite):
                            needs_sprite = True
                            break

            all_sprites.append(new_sprite)

# Function to check collision for all sprites and return the sprites that are being collided with 
def rect_collision(collision_with, all_sprites):
    def create_list(sprite):
        # If no sprite of the same kind has been added to the collision dictionary
        if type(sprite).__name__ not in collisions:
            # Add an empty list
            collisions[type(sprite).__name__] = []

    # Initial dictionary of collisions
    collisions = {

    }
    for sprite in all_sprites:
        # Add to the list of collisions of the same sprite type, prioritizing hitbox
        try:
            if collision_with.rect.colliderect(sprite.hitbox) and sprite != collision_with:
                create_list(sprite)
                collisions[type(sprite).__name__].append(sprite)

        except:
            if collision_with.rect.colliderect(sprite.rect) and sprite != collision_with:
                create_list(sprite)
                collisions[type(sprite).__name__].append(sprite)

    return collisions

def movement(sprite, player, keys):
    movement_speed = 1
    if player.animation_style == "walking":
        if keys[K_d] or keys[K_a]:
            if keys[K_d]:
                sprite.rect.move_ip(-movement_speed, 0)

            if keys[K_a]:
                sprite.rect.move_ip(movement_speed, 0)
        elif keys[K_w] or keys[K_s]:
            if keys[K_w]:
                sprite.rect.move_ip(0, movement_speed)

            if keys[K_s]:
                sprite.rect.move_ip(0, -movement_speed)

def closest_point(vertices, player):
    def player_facing(vertex):
        if (player.direction == "up" or player.direction == "down") and player.rect.left < vertex[0] < player.rect.right:
            return True 
        if (player.direction == "right" or player.direction == "left") and player.rect.top < vertex[1] < player.rect.bottom:
            return True
    point_from_direct = {
        "right": (player.rect.right, player.rect.centery),
        "left": (player.rect.left, player.rect.centery),
        "up": (player.rect.centerx, player.rect.top),
        "down": (player.rect.centerx, player.rect.bottom)
    }
    
    closest_vertex = -1
    shortest_dist = -1

    playerx, playery = point_from_direct[player.direction]

    for vertex in vertices:
        if not player.rect.collidepoint(vertex):
            x, y = vertex

            distance = math.hypot(x - playerx, y - playery)

            if(distance < shortest_dist or shortest_dist == -1) and player_facing(vertex):
                shortest_dist = distance
                closest_vertex = vertex


    return closest_vertex