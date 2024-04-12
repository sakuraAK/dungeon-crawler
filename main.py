import pygame
from pygame import mixer
import csv
from world import World

import constants
from constants import SCREEN_HEIGHT, SCREEN_WIDTH, BG, FPS, SPEED, SCALE, SCALE_WEAPON, BOSS_SCALE
from weapon import Weapon
from item import Item

mixer.init()
pygame.init()


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dungeon Crawler")
game_level = 1
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

    def update(self, scroll):

        self.rect.centerx += scroll[0]
        self.rect.centery += scroll[1]

        self.rect.y -= 1
        self.fade_counter += 1
        if self.fade_counter > 100:
            self.kill()

class Fade:
    def __init__(self, direction, color, speed):
        self.direction = direction
        self.speed = speed
        self.color = color
        self.fade_counter = 0

    def fade(self):
        fade_complete = False
        pygame.draw.rect(screen, self.color, (0 - self.fade_counter, 0, constants.SCREEN_WIDTH // 2, constants.SCREEN_HEIGHT))
        pygame.draw.rect(screen, self.color,
                         (constants.SCREEN_WIDTH // 2 + self.fade_counter, 0, constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))


        self.fade_counter += self.speed

        if self.fade_counter >= constants.SCREEN_WIDTH:
            fade_complete = True

        return fade_complete




def scale_image(image, scale):
    w = image.get_width()
    h = image.get_height()
    return pygame.transform.scale(image, (w * scale, h * scale))

# images start

# map tiles
tile_images = []
for i in range(constants.IMAGE_TYPE):
    img = pygame.image.load(f"assets/images/tiles/{i}.png").convert_alpha()
    img = pygame.transform.scale(img, (constants.TILE_SIZE, constants.TILE_SIZE))
    tile_images.append(img)

bow_image = scale_image(pygame.image.load("assets/images/weapons/bow.png").convert_alpha(), SCALE_WEAPON)
arrow_image = scale_image(pygame.image.load("assets/images/weapons/arrow.png").convert_alpha(), SCALE_WEAPON)
fireball_image = scale_image(pygame.image.load("assets/images/weapons/fireball.png").convert_alpha(), SCALE_WEAPON)

full_heart = scale_image(pygame.image.load("assets/images/items/heart_full.png").convert_alpha(), constants.SCALE_ITEMS)
half_heart = scale_image(pygame.image.load("assets/images/items/heart_half.png").convert_alpha(), constants.SCALE_ITEMS)
empty_heart = scale_image(pygame.image.load("assets/images/items/heart_empty.png").convert_alpha(), constants.SCALE_ITEMS)

# items images
coins = []
for i in range(4):
    img = scale_image(pygame.image.load(f"assets/images/items/coin_f{i}.png").convert_alpha(), constants.SCALE_ITEMS)
    coins.append(img)
red_potion = scale_image(pygame.image.load(f"assets/images/items/potion_red.png").convert_alpha(), constants.SCALE_ITEMS)
items_image_list = []
items_image_list.append(coins)
items_image_list.append([red_potion])

character_list = ["dracula", "zombie", "big_demon"]
action_types = ["idle", "run"]
all_animation_list = []
for character in character_list:
    animation_list = []
    for action in action_types:
        tmp_list = []
        for i in range(4):
            image = pygame.image.load(f"assets/images/characters/{character}/{action}/{i}.png").convert_alpha()
            image = scale_image(image, SCALE if character != "big_demon" else BOSS_SCALE)
            tmp_list.append(image)
        animation_list.append(tmp_list)
    all_animation_list.append(animation_list)

# images end
pygame.mixer.music.load("assets/audio/music.wav")
pygame.mixer.music.set_volume(0.2)
# pygame.mixer.music.play(-1, 0.0, 5000)

shot_fx = pygame.mixer.Sound("assets/audio/arrow_shot.mp3")
shot_fx.set_volume(0.5)

arrow_hit = pygame.mixer.Sound("assets/audio/arrow_hit.wav")
arrow_hit.set_volume(0.5)

coin_fx = pygame.mixer.Sound("assets/audio/coin.wav")
coin_fx.set_volume(0.5)

heal_fx = pygame.mixer.Sound("assets/audio/heal.wav")
heal_fx.set_volume(0.5)

# load sounds


def generate_world():
    map = World()
    world_data = []
    for i in range(constants.COL_NUMBER):
        row = [-1] * constants.COL_NUMBER
        world_data.append(row)

    with open(f"assets/levels/level{game_level}_data.csv") as in_file:
        tile_data = csv.reader(in_file, delimiter=",")
        for i, row in enumerate(tile_data):
            for j, tile in enumerate(row):
                world_data[i][j] = int(tile)

    map.process_data(world_data, tile_images, all_animation_list, items_image_list)
    return map

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

    # level info
    draw_text(SCREEN_WIDTH // 2, 15, font, f"LEVEL: {game_level}", constants.WHITE)


score_coin = Item(SCREEN_WIDTH - 60, 20, 0, coins, True)

#game map, characters, items, and objects
bow = Weapon(bow_image, arrow_image)

# # sprite groups
# arrow_group = pygame.sprite.Group()
# damage_text_group = pygame.sprite.Group()
# items_group = pygame.sprite.Group()
# fireball_group = pygame.sprite.Group()


# create world
world_map = generate_world()



arrow_group = pygame.sprite.Group()
damage_text_group = pygame.sprite.Group()
items_group = pygame.sprite.Group()
fireball_group = pygame.sprite.Group()

def reset_level():
    arrow_group.empty()
    damage_text_group.empty()
    items_group.empty()
    fireball_group.empty()

screen_fade = Fade(1, constants.BLACK,4)

player = world_map.player
enemies_list = world_map.enemies
for item in world_map.items:
    items_group.add(item)

# game loop
run = True
show_intro = True
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

    scroll, next_level = player.move(dx, dy, world_map.obstacles, world_map.exit)

    if next_level:
        game_level += 1
        if game_level > 4:
            game_level = 1

        reset_level()

        world_map = generate_world()

        player = world_map.player
        enemies_list = world_map.enemies
        for item in world_map.items:
            items_group.add(item)
        show_intro = True
    else:
        # update section
        player.update()
        world_map.update(scroll)
        arrow = bow.update(player)
        if arrow:
            shot_fx.play()
            arrow_group.add(arrow)
        for arrow in arrow_group:
            damage, enemy_pos_rect = arrow.update(enemies_list, scroll, arrow_hit)
            if damage:
                damage_text_group.add(DamageText(enemy_pos_rect.centerx, enemy_pos_rect.y, str(damage), constants.RED))

        for enemy in enemies_list:
            fireball = enemy.ai(player, world_map.obstacles, scroll, fireball_image)
            if fireball:
                fireball_group.add(fireball)
            enemy.update()

        fireball_group.update(player, scroll)
        damage_text_group.update(scroll)
        items_group.update(player, scroll, [coin_fx, heal_fx])
        score_coin.update(player, scroll, [coin_fx, heal_fx])

        # draw section
        world_map.draw(screen)
        draw_game_info(player)

        player.draw(screen)
        bow.draw(screen)
        arrow_group.draw(screen)
        fireball_group.draw(screen)
        for enemy in enemies_list:
            enemy.draw(screen)
        damage_text_group.draw(screen)
        score_coin.draw(screen)
        items_group.draw(screen)

    if show_intro:
        if screen_fade.fade():
            show_intro = False
            screen_fade.fade_counter = 0
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
