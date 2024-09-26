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

            pos = pygame.mouse.get_pos()
            
            #Collison Testing Shift to enenmy Class
            enemy_rect = pygame.Rect(0, 0, 25, 25)
            enemy_rect.center = pos
            """if player.color == "YELLOW" and player.tick >= 4:
                player.color = "GREEN"
            else:
                player.color = "GREEN"""
            
            #Testing Collision for Enemy Can be removed.
            """if player.rect.colliderect(enemy_rect):
               player.color = "RED"
               player.hp -=1
               print(player.hp)"""

            
            #Draw Sprites to game window and updates.
            self.screen.fill((0,0,0))
            pygame.draw.rect(self.screen, "BLUE" , enemy_rect)    
            player.playerUpdate(self.screen,enemy_rect)     #Change to a list containing enemy
            self.display.blit(self.screen, (0,0))
            pygame.display.flip()
            self.clock.tick(60) 

    



if __name__ == "__main__":
    instance = Game()
    instance.game_loop()


