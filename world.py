from character import Character
from item import Item
import constants
class World:

    def __init__(self):
        self.map_tiles = []
        self.obstacles = []
        self.items = []
        self.enemies = []
        self.player = None
        self.exit = None

    def clear_all(self):
        self.map_tiles = []
        self.obstacles = []
        self.items = []
        self.enemies = []
        self.player = None
        self.exit = None

    def process_data(self, data, tile_images, all_animation_list, items_image_list):
        self.clear_all()
        # iterate over each element in level data and create map tile
        for i, row in enumerate(data):
            for j, tile in enumerate(row):
                if tile < 0:
                    continue

                image = tile_images[tile]
                image_rec = image.get_rect()
                image_y = i * constants.TILE_SIZE
                image_x = j * constants.TILE_SIZE
                image_rec.center = (image_x, image_y)
                tile_data = [image, image_rec, image_x, image_y]

                if tile == 7:
                # wall tile
                    self.obstacles.append(tile_data)
                elif tile == 8:
                    self.exit = tile_data

                elif tile == 11:
                    player = Character(image_x, image_y, constants.PLAYER_INIT_HEALTH, all_animation_list, 0)
                    self.player = player
                elif tile >= 12 and tile < 15:
                    # enemy
                    enemy = Character(image_x, image_y, constants.ENEMY_INIT_HEALTH, all_animation_list, 1)
                    self.enemies.append(enemy)
                elif tile >= 15 and tile <= 17:
                    # item
                    # 15: coin
                    # 16: red potion
                    if tile == 15:
                        item = Item(image_x, image_y, 0, items_image_list[0])
                        self.items.append(item)
                    elif tile == 16:
                        item = Item(image_x, image_y, 1, items_image_list[1])
                        self.items.append(item)



                self.map_tiles.append(tile_data)

    def update(self, scroll):
        for tile in self.map_tiles:
            tile[2] += scroll[0]
            tile[3] += scroll[1]
            tile[1].center = (tile[2], tile[3])

    def draw(self, surface):
        for tile in self.map_tiles:
            surface.blit(tile[0], tile[1])