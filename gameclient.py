import pygame
from config import *
from displayObject import DisplayObject
from tileset import Tileset
from gameserver import GameServer
from client import Client

class GameClient:
    
    def __init__(self, site):
        self.gameDisplay = pygame.display.set_mode((TILE_WIDTH * GRID_SIZE,TILE_HEIGHT * GRID_SIZE))
        self.tileset = Tileset("./assets/sprites.png", [16,16], 0,0)
        pygame.display.set_caption(site.name)
        
        self.clock = pygame.time.Clock()
        self.quit = False

        # Client obj
        self.client = Client()
        self.client.start_client()

        #instantiating the player
        site.addObject(2, [0,0])
        #run
        self.run(site)

    def run(self, site):
        while not self.quit:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit = True
                if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_s:
                             pass
            #background
            self.gameDisplay.fill((0,0,0))
            #display landArray
            for x,arr in enumerate(site.landArray):
                for y,value in enumerate(arr):
                    self.gameDisplay.blit(self.tileset.tiles[value], (TILE_WIDTH * x, TILE_HEIGHT * y))
            #display objectArray
            for x,arr in enumerate(site.objArray):
                if (len(arr) > 0):
                    for y,value in enumerate(arr):
                        self.gameDisplay.blit(self.tileset.tiles[value], (TILE_WIDTH * x, TILE_HEIGHT * y))
            #display
            pygame.display.update()
            self.clock.tick(60)