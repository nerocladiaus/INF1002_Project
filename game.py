import pygame
from player import Player
from enemy import Enemy

pygame.init()

class Game:
    def __init__(self):
        self.screenWidth, self.screenHeight = 1280, 720
        self.display = pygame.display.set_mode((self.screenWidth, self.screenHeight))
        self.screen = pygame.Surface((self.screenWidth, self.screenHeight))
        self.running = True
        self.clock = pygame.time.Clock()
        
    
    def game_loop(self):
        self.player = Player()
        self.enemies = []
        self.enemySpawnTimer = 0
        
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False        

            if self.enemySpawnTimer >= 50:
                self.enemies.append(Enemy(self.screenWidth,self.screenHeight))
                print("Enemy spawn")
                self.enemySpawnTimer = 0
            else:
                self.enemySpawnTimer += 1
                #print(self.enemySpawnTimer)
            
            #Collison Testing Shift to enenmy Class
            pos = pygame.mouse.get_pos()
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
            self.player.playerUpdate(self.screen,enemy_rect)     #Change to a list containing enemy
            #self.enemies.update(self.screen,self.screenHeight,self.screenWidth)
            for enemy in self.enemies:
                enemy.update(self.screen,self.player)
            self.display.blit(self.screen, (0,0))
            pygame.display.flip()
            self.clock.tick(60) 

    



if __name__ == "__main__":
    instance = Game()
    instance.game_loop()


