import pygame

import constants
from constants import SCREEN_HEIGHT, SCREEN_WIDTH, BG, FPS, SPEED, SCALE, SCALE_WEAPON
from character import Character
from weapon import Weapon, Arrow
from enemies import  Zombie
from item import Item

pygame.init()


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dungeon Crawler")

clock = pygame.time.Clock()

# player movement variables
move_left = False
move_right = False
move_up = False
move_down = False

font = pygame.font.Font("assets/fonts/AtariClassic.ttf", constants.FONT_SIZE)


def draw_text(x, y, font, text, color):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))


class DamageText(pygame.sprite.Sprite):
    def __init__(self, x, y, damage, color):
        pygame.sprite.Sprite.__init__(self)
        self.image = font.render(damage, True, color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.fade_counter = 0

    def update(self):
        self.rect.y -= 1
        self.fade_counter += 1
        if self.fade_counter > 100:
            self.kill()

def scale_image(image, scale):
    w = image.get_width()
    h = image.get_height()
    return pygame.transform.scale(image, (w * scale, h * scale))

# work on images
bow_image = scale_image(pygame.image.load("assets/images/weapons/bow.png").convert_alpha(), SCALE_WEAPON)
arrow_image = scale_image(pygame.image.load("assets/images/weapons/arrow.png").convert_alpha(), SCALE_WEAPON)

full_heart = scale_image(pygame.image.load("assets/images/items/heart_full.png").convert_alpha(), constants.SCALE_ITEMS)
half_heart = scale_image(pygame.image.load("assets/images/items/heart_half.png").convert_alpha(), constants.SCALE_ITEMS)
empty_heart = scale_image(pygame.image.load("assets/images/items/heart_empty.png").convert_alpha(), constants.SCALE_ITEMS)

coins = []
for i in range(4):
    img = scale_image(pygame.image.load(f"assets/images/items/coin_f{i}.png").convert_alpha(), constants.SCALE_ITEMS)
    coins.append(img)
red_potion = scale_image(pygame.image.load(f"assets/images/items/potion_red.png").convert_alpha(), constants.SCALE_ITEMS)

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


def draw_game_info(player):
    pygame.draw.rect(screen, constants.PANEL, (0, 0, SCREEN_WIDTH, 50))
    pygame.draw.line(screen, constants.WHITE, (0, 50), (SCREEN_WIDTH, 50))

    # player info

    # health
    for i in range(constants.PLAYER_INIT_HEALTH // 20):
        # 20 - full heart; >10 < 20 - half; < 10 - empty
        if player.health - i * 20 >= 20:
            screen.blit(full_heart, (10 + 50 * i, 0))
        elif player.health - i * 20 > 10:
            screen.blit(half_heart, (10 + 50 * i, 0))
        else:
            screen.blit(empty_heart, (10 + 50 * i, 0))

    # score
    draw_text(SCREEN_WIDTH - 50, 15, font, f"x{player.score}", constants.WHITE)

# create player
player = Character(100, 100, 55, all_animation_list, 0)
bow = Weapon(bow_image, arrow_image)

# sprite groups
arrow_group = pygame.sprite.Group()
damage_text_group = pygame.sprite.Group()
items_group = pygame.sprite.Group()
items_group.add(Item(400, 600, 0, coins))
items_group.add(Item(600, 400, 1, [red_potion]))
score_coin = Item(SCREEN_WIDTH - 60, 20, 0, coins)

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

    # update section
    # move player
    player.move(dx, dy)
    player.update()

    arrow = bow.update(player)

    if arrow:
        arrow_group.add(arrow)
    for arrow in arrow_group:
        damage, enemy_pos_rect = arrow.update(enemies_list)
        if damage:
            damage_text_group.add(DamageText(enemy_pos_rect.centerx, enemy_pos_rect.y, str(damage), constants.RED))


    for enemy in enemies_list:
        enemy.update()

    damage_text_group.update()

    items_group.update(player)

    score_coin.update(player)

    # drawing section

    player.draw(screen)
    bow.draw(screen)
    arrow_group.draw(screen)
    for enemy in enemies_list:
        enemy.draw(screen)
    damage_text_group.draw(screen)

    draw_game_info(player)
    score_coin.draw(screen)

    items_group.draw(screen)

    # event handling section
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
