import pygame
from constants import SCREEN_HEIGHT, SCREEN_WIDTH, BG, FPS, SPEED, SCALE, SCALE_WEAPON
from character import Character
from weapon import Weapon, Arrow
from enemies import  Zombie

pygame.init()


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dungeon Crawler")

clock = pygame.time.Clock()

# player movement variables
move_left = False
move_right = False
move_up = False
move_down = False

def scale_image(image, scale):
    w = image.get_width()
    h = image.get_height()
    return pygame.transform.scale(image, (w * scale, h * scale))

# work on images
bow_image = scale_image(pygame.image.load("assets/images/weapons/bow.png").convert_alpha(), SCALE_WEAPON)
arrow_image = scale_image(pygame.image.load("assets/images/weapons/arrow.png").convert_alpha(), SCALE_WEAPON)

character_list = ["dracula", "zombie"]
action_types = ["idle", "run"]
all_animation_list = []
for character in character_list:
    animation_list = []
    for action in action_types:
        tmp_list = []
        for i in range(4):
            image = pygame.image.load(f"assets/images/characters/{character}/{action}/{i}.png").convert_alpha()
            image = scale_image(image, SCALE)
            tmp_list.append(image)
        animation_list.append(tmp_list)
    all_animation_list.append(animation_list)





# create player
player = Character(100, 100, 100, all_animation_list, 0)
bow = Weapon(bow_image, arrow_image)

# sprite groups
arrow_group = pygame.sprite.Group()

#create enemies
enemies_list = []
enemies_list.append(Character(300, 300, 100, all_animation_list, 1))

# game loop
run = True
while run:
    # control game speed
    clock.tick(FPS)

    # clearing the screen
    screen.fill(BG)

    # calculate player movements
    dx = 0
    dy = 0
    if move_right:
        dx = SPEED
    if move_left:
        dx = -SPEED
    if move_up:
        dy = -SPEED
    if move_down:
        dy = SPEED

    # move player
    player.move(dx, dy)

    # # move enemies
    # for enemy in enemies_list:
    #     enemy.move()

    # update animation
    player.update()
    arrow = bow.update(player)
    if arrow:
        arrow_group.add(arrow)

    for arrow in arrow_group:
        arrow.update(enemies_list)
    #arrow_group.update()

    for enemy in enemies_list:
        enemy.update()

    print(enemies_list[0].health)


    # draw player
    player.draw(screen)
    bow.draw(screen)
    arrow_group.draw(screen)

    # draw enemies
    for enemy in enemies_list:
        enemy.draw(screen)

    #event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        # handle keyboard events
        # handle button pressed event
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                move_left = True
            if event.key == pygame.K_d:
                move_right = True
            if event.key == pygame.K_w:
                move_up = True
            if event.key == pygame.K_s:
                move_down = True
        # handle button release event
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                move_left = False
            if event.key == pygame.K_d:
                move_right = False
            if event.key == pygame.K_w:
                move_up = False
            if event.key == pygame.K_s:
                move_down = False

    # render the display
    pygame.display.update()

pygame.quit()
