# Dig Make v1.0.0 by Andrew Collins
# 5/3/2021
# Sprites taken from OpenGameArt.org
import pygame
import sprites.backgrounds.backgrounds as backgrounds
import sprites.player.player as player
import sprites.resource.resource as resource
import sprites.sprites_funcs as sfuncs
import sprites.items.item as item
import sprites.inventory.inventory as inventory
from pygame.locals import *
import random
from itertools import chain
import pygame.locals

# Initializing pygame and window
pygame.init()
pygame.display.set_caption('Dig Make')

# Creating the screen
SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 640, 640
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT )) #, pygame.FULLSCREEN

# Clock for framerate limiting
clock = pygame.time.Clock()

# Creating the player and backgrounds, putting them in a list of all sprites
player = player.Player(*SCREEN_SIZE)
all_sprites = [backgrounds.Background((0, 0), SCREEN_WIDTH, SCREEN_HEIGHT, r"sprites\backgrounds\assets\grass.png"), 
               backgrounds.Background((SCREEN_WIDTH, 0), SCREEN_WIDTH, SCREEN_HEIGHT, r"sprites\backgrounds\assets\grass.png"),
               backgrounds.Background((0, SCREEN_HEIGHT), SCREEN_WIDTH, SCREEN_HEIGHT, r"sprites\backgrounds\assets\grass.png"),    
               backgrounds.Background((SCREEN_WIDTH, SCREEN_HEIGHT), SCREEN_WIDTH, SCREEN_HEIGHT, r"sprites\backgrounds\assets\grass.png"),
               player,
               resource.Resource((100, 100)), # Tree
               resource.Resource((400, 400)), # Tree
               ]

# Set structure for inventory items, three rows
inventory_items = [[],
                   [],
                   []]

# Create the inventory and hotbar image sprites and boolean to show inventory
inventory_gui = inventory.Inventory((int((SCREEN_WIDTH / 2) - ((147 / 112) * 200 / 2)), 100), {
            0: {"x": 8, "y": 8},
            1: {"x": 13, "y": 14},
            2: {"x": 20, "y": 21},
            3: {"x": 27}
        })
inventory_open = False
hotbar = inventory.Inventory((0, 0), {
            0: 8,
            1: 14,
            2: 21,
            3: 29
        }, image=r"sprites\inventory\assets\hotbar.png", height=75)

# User events (animation, cooldowns)
PLAYERANIMATION = pygame.USEREVENT + 1
pygame.time.set_timer(PLAYERANIMATION, 200)
HITCOOLDOWN = pygame.USEREVENT + 2

pygame.font.init()
font = pygame.font.SysFont(r'fonts\Pixelar.ttf', 25)

# Dictionary of cooldowns, given to the update function
cooldowns = {
    "HITCOOLDOWN": HITCOOLDOWN,
    "PLAYERANIMATION": PLAYERANIMATION
    }

# Toggleable debug boolean (shows hitboxes)
debug = False

# Game Loop
running = True
while running:
    # Get the set of keys pressed and mouse presses for user input
    pressed_keys = pygame.key.get_pressed()
    mouse_presses = left_click, middle_click, right_click = pygame.mouse.get_pressed()

    inventory_gui.update(pressed_keys)
    hotbar.update(pressed_keys)

    # Gets all events triggered
    for event in pygame.event.get():
        # Stop the game when window X is pressed
        if event.type == pygame.QUIT:
            quit()

        # A key has been pressed
        if event.type == pygame.KEYDOWN:
            # Stop the game when escape is pressed
            if event.key == K_ESCAPE:
                quit()

            # Toggles debug mode
            if event.key == K_F3:
                debug = not debug

            # Toggles inventory
            if event.key == K_e:
                inventory_open = not inventory_open
            
            if event.key == K_q:
                if len(inventory_items[0]) >= hotbar.selected and len(inventory_items[0]) != 0:
                    inventory_items[0][hotbar.selected - 1].drop_item(player, inventory_items)

            if event.key == K_LSHIFT:
                for item in all_sprites:
                    if type(item).__name__ == "Item":
                        if item.collect_item(inventory_items, player):
                            break


        # Stops animation and cooldown if the inventory isn't open
        if not inventory_open:
            # Loops through player animation
            if event.type == PLAYERANIMATION:
                player.animation()

            # Sets player hit cooldown to false to limit hitting speed
            if event.type == HITCOOLDOWN:
                player.cooldown = False

        # Event triggered on click in inventory
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and inventory_open:
            mouse_pos = pygame.mouse.get_pos()

            # Sets an item as clicked and the position of the click on the item
            for item in [item for row in inventory_items for item in row]:
                if item.rect.collidepoint(mouse_pos):
                    item.clicked = True
                    item.click_position = (mouse_pos[0] - item.rect.x, mouse_pos[1] - item.rect.y)

        # Event triggered when left click is released in inventory
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and inventory_open:
            # List of all items in inventory (no rows)
            items_in_inventory = [item for row in inventory_items for item in row]

            for item in items_in_inventory:
                # If an item is being dragged
                if item.clicked:
                    clicked_item = item

                    # Swaps the dragged item with the item hovered over
                    for item_no_click in items_in_inventory:
                        if item_no_click != item and item_no_click.rect.collidepoint(pygame.mouse.get_pos()):
                            item_to_replace = item_no_click

                            for count, row in enumerate(inventory_items):
                                if item_to_replace in row:
                                    original_position_collided = [count, row.index(item_to_replace)]
                            
                            for count, row in enumerate(inventory_items):
                                if item in row:
                                    row[row.index(item)] = item_to_replace

                            inventory_items[original_position_collided[0]][original_position_collided[1]] = clicked_item  
                    # Item is no longer being clicked
                    item.clicked = False


    # Fill background as black (shouldn't be seen)
    screen.fill((0, 0, 0))

    # Sprite Generation
    gen_args = [SCREEN_WIDTH, SCREEN_HEIGHT, all_sprites]
    sfuncs.sprite_generation("Tree", *gen_args, 3)
    sfuncs.sprite_generation("Stone", *gen_args, 1, 80, r"sprites\resource\assets\rock1.png", 6, r"sprites\items\assets\rock.png", "Stone")

    

    if not inventory_open:
        player.update(pressed_keys, player, all_sprites, cooldowns, hotbar=hotbar, inventory_items=inventory_items)
 
        # Update all sprites
        for sprite in all_sprites:
            if callable(getattr(sprite, "update")):
                sprite.update(pressed_keys, player, all_sprites, cooldowns, hotbar=hotbar, inventory_items=inventory_items, left_click=left_click)

        # Stop movement on collision
        sfuncs.stop_movement(all_sprites, inventory_items=inventory_items)

    # Displays backgrounds, healthbars, and items
    for sprite in all_sprites:
        if type(sprite).__name__ == "Background":
            screen.blit(sprite.surf, sprite.rect)

        if hasattr(sprite, 'blit_health'):
            sprite.blit_health(screen)

        if type(sprite).__name__ == "Item" and sprite not in chain(*inventory_items):
            screen.blit(sprite.surf, sprite.rect)

    # Displays the rest of the sprites
    for sprite in all_sprites:
        if type(sprite).__name__ != "Background" and type(sprite).__name__ != "Item" and type != "Inventory":
            screen.blit(sprite.surf, sprite.rect)
    if len(inventory_items[0]) >= hotbar.selected:
        if inventory_items[0][hotbar.selected - 1].placeable:
            for sprite in all_sprites:
                if type(sprite).__name__ != "Background":
                    break
                if player.rect.colliderect(sprite) and sfuncs.closest_point(sprite.points, player) != -1:
                    pygame.draw.circle(screen, (255, 0, 0), sfuncs.closest_point(sprite.points, player), 2)
                    break

    # Groups the items into their correct rows
    for count, row in enumerate(inventory_items):
        while len(row) > 4: 
            if count != 2:
                inventory_items[count + 1].append(row[-1])
                row.remove(row[-1])
        if len(row) == 3:
            if count + 1 < len(inventory_items):
                if len(inventory_items[count + 1]) != 0:
                    row.append(inventory_items[count + 1][-1])
                    inventory_items[count + 1].pop()

    if not inventory_open:
        # Dictionary of the hotbar image's weird inconsistent bezels caused by the resizing
        inventory_bezels = hotbar.inventory_bezels

        # Draws the hotbar on the screen
        screen.blit(hotbar.surf, hotbar.rect)

        # Math logic for centering the items in their hotbar slots
        for item_count, item in enumerate(inventory_items[0]):
            item.rect.topleft = (hotbar.rect.topleft[0] + inventory_bezels[item_count] + (60 * item_count) + (60 / 2) - (item.rect.width / 2), 
                                 hotbar.rect.topleft[1] + 8 + (60 / 2) - (item.rect.height / 2))
            screen.blit(item.surf, item.rect)
        
        hotbar.draw_numbers(screen, font)


    # Debug mode (shows hitboxes)
    if debug:
        for sprite in all_sprites:
            if type(sprite).__name__ != "Background":
                if hasattr(sprite, "hitbox"):
                    pygame.draw.rect(screen, (0,0,255), sprite.hitbox, 2)
                pygame.draw.rect(screen, (255,0,0), sprite.rect, 2)
        for sprite in all_sprites:
            if type(sprite).__name__ != "Background":
                break
            # print(sprite.points)
            for point in sprite.points:
                pygame.draw.circle(screen, (255, 0, 0), (point[0], point[1]), 2)


    if inventory_open: 
        # Dictionary for weird inconsistent bezzles for the inventory image caused by image resizing
        inventory_bezels = inventory_gui.inventory_bezels
        clicked_item = None
        screen.blit(inventory_gui.surf, inventory_gui.rect)

        # Loops through all inventory items
        for row_count, row in enumerate(inventory_items):
            for item_count, item in enumerate(row):

                # Sets the position of a clicked item
                if item.clicked:
                    clicked_item = item
                    mouse_pos = pygame.mouse.get_pos()
                    item.rect.x = mouse_pos[0] - item.click_position[0]
                    item.rect.y = mouse_pos[1] - item.click_position[1]

                # Math logic for the unclicked items to be in their inventory slots
                else:
                    item.rect.topleft = (inventory_gui.rect.topleft[0] + inventory_bezels[item_count]["x"] + (57 * item_count) + (57 / 2) - (item.rect.width / 2), 
                                            inventory_gui.rect.topleft[1] + inventory_bezels[row_count]["y"] + (57 * row_count) + (57 / 2) - (item.rect.height / 2))
                    screen.blit(item.surf, item.rect)
            inventory_gui.draw_numbers(screen, font)


        # Draws the dragged item last
        if clicked_item != None:
            screen.blit(clicked_item.surf, clicked_item.rect)


    # Update the display
    pygame.display.flip()

    # Ensure program maintains a rate of 120 frames per second
    clock.tick(120)
pygame.quit()