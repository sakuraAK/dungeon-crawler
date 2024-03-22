import constants
class World:

    def __init__(self):
        self.map_tiles = []


    def process_data(self, data, tile_images):
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

                self.map_tiles.append(tile_data)

    def update(self, scroll):
        for tile in self.map_tiles:
            tile[2] += scroll[0]
            tile[3] += scroll[1]
            tile[1].center = (tile[2], tile[3])

    def draw(self, surface):
        for tile in self.map_tiles:
            surface.blit(tile[0], tile[1])