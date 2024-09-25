import pygame
from player import Player

pygame.init()

class Game:
    def __init__(self):
        self.screenWidth, self.screenHeight = 1280, 720
        self.display = pygame.display.set_mode((self.screenWidth, self.screenHeight))
        self.screen = pygame.Surface((self.screenWidth, self.screenHeight))
        self.running = True
        self.clock = pygame.time.Clock()
    
    def game_loop(self):
        player = Player()

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False        

            #Draw Sprites to game window and updates.
            self.screen.fill((0,0,0))
            player.playerUpdate(self.screen)
            self.display.blit(self.screen, (0,0))
            pygame.display.flip()
            self.clock.tick(60) 

    



if __name__ == "__main__":
    instance = Game()
    instance.game_loop()


