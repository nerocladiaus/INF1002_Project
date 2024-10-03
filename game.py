import pygame
import random
from player import Player
from enemy import Enemy

pygame.init()
pygame.display.set_caption("Urban Onslaught")

class Game:
    def __init__(self):
        self.screenWidth, self.screenHeight = 1280, 800
        self.display = pygame.display.set_mode((self.screenWidth, self.screenHeight))
        self.screen = pygame.Surface((self.screenWidth, self.screenHeight))
        self.running = True
        self.clock = pygame.time.Clock()
        
        
    
    def game_loop(self):
        self.player = Player()
        self.enemies = []
        self.enemySpawnTimer = 0
        self.score = 0
        self.enemySpawnTimermax = 50
        #self.levelspike = 0
        self.enemy_typelist = ["weak", "normal", "strong"]
        
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False        

            if self.enemySpawnTimer >= self.enemySpawnTimermax:
                self.enemytype = random.choice(self.enemy_typelist)
                self.enemies.append(Enemy(self.screenWidth,self.screenHeight, self.enemytype))
                print(f'Enemy {self.enemytype} spawn')
                self.enemySpawnTimer = 0
            else:
                self.enemySpawnTimer += 1
                #print(self.enemySpawnTimer)
            
            #Collison Testing Shift to enenmy Class
            pos = pygame.mouse.get_pos()
            mouse_rect = pygame.Rect(0, 0, 25, 25)
            mouse_rect.center = pos
            
            #Draw Sprites to game window and updates.
            self.screen.fill((0,0,0))
            pygame.draw.rect(self.screen, "BLUE" , mouse_rect)    
            self.player.playerUpdate(self.screen,mouse_rect,self.screenWidth,self.screenHeight)  
            #self.enemies.update(self.screen,self.screenHeight,self.screenWidth)
            for enemy in self.enemies:
                enemy.update(self.screen,self.player,mouse_rect)
                if enemy.dead:
                    self.enemies.remove(enemy)
                    self.score += 100
                    #self.levelspike += 10
                    #print(self.levelspike)

            """if self.enemySpawnTimermax > 5 and self.levelspike >= 1000:
                self.enemySpawnTimermax -=5
                self.levelspike = 0
                print("Diffculty inceased")"""
            
            self.display.blit(self.screen, (0,0))
            pygame.display.flip()
            self.clock.tick(60) 

    



if __name__ == "__main__":
    instance = Game()
    instance.game_loop()


