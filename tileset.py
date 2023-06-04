import pygame
class Tileset:
    def __init__(self, file, size, margins, spacing):
        self.file = file
        self.size = size
        self.margins = margins
        self.spacing = spacing
        self.tileset_img = pygame.image.load(file).convert()
        self.rect = self.tileset_img.get_rect()
        self.tiles = []
        #splitting image into tiles
        x0 = y0 = self.margins
        w,h = self.rect.size
        dx = self.size[0] + self.spacing
        dy = self.size[1] + self.spacing

        for x in range(x0, w, dx):
            for y in range(y0,h,dy):
                tile = pygame.Surface(self.size)
                tile.blit(self.tileset_img, (0,0), (y,x, *self.size))
                self.tiles.append(tile)
