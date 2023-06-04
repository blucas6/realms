import pygame
from config import *
from tileset import Tileset
from displayObject import DisplayObject

class Game:
    
    def __init__(self):
        displayObj = []
        gameDisplay = pygame.display.set_mode((TILE_WIDTH * GRID_SIZE,TILE_HEIGHT * GRID_SIZE))
        pygame.display.set_caption('Game')
        self.tileset = Tileset("./assets/sprites.png", [16,16], 0,0)
        clock = pygame.time.Clock()
        quit = False

        while not quit:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        displayObj.append(DisplayObject(self.tileset.tiles[2], (3,5)))
            #background
            gameDisplay.fill((0,0,0))
            #display displayOBJ
            for obj in displayObj:
                gameDisplay.blit(obj.image, (TILE_WIDTH * obj.pos[0], TILE_HEIGHT * obj.pos[1]))
            #display
            pygame.display.update()
            clock.tick(60)