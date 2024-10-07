import pygame
import random
import sys
import time
from player import Player
from enemy import Enemy
from projectile import Projectile

class Game:
    def __init__(self):
        self.screenWidth, self.screenHeight = 1280, 800
        self.display = pygame.display.set_mode((self.screenWidth, self.screenHeight))
        self.screen = pygame.Surface((self.screenWidth, self.screenHeight))
        self.running = True
        self.clock = pygame.time.Clock()

        # Initialize Pygame font module
        pygame.font.init()
        # Set up fonts for the clock
        self.font = pygame.font.Font(None, 36)  # Initialize the font
        # Store the start time
        self.start_time = pygame.time.get_ticks()  # Time in milliseconds
        self.timer_running = True  # Initialize the timer flag

    def draw_clock(self):
        if self.timer_running:
            # Calculate the elapsed time
            elapsed_time = (pygame.time.get_ticks() - self.start_time) // 1000  # Convert to seconds
            minutes = elapsed_time // 60
            seconds = elapsed_time % 60
            timer_display = f"{minutes:02}:{seconds:02}"  # Format as MM:SS
        else:
            timer_display = "Game Over"  # Display "Game Over" when the timer stops

        text_surface = self.font.render(timer_display, True, (255, 255, 255))  # White text
        text_rect = text_surface.get_rect(topright=(self.screenWidth - 10, 10))  # Top right corner
        self.screen.blit(text_surface, text_rect)
    
    def game_loop(self):
        self.player = Player()
        self.enemies = []
        self.enemySpawnTimer = 0
        self.score = 0
        self.enemySpawnTimermax = 50
        self.kills = 0
        self.enemy_threshold,self. enemy_level = 10, 0
        self.enemy_typelist = ["weak"]

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # Check if player's health is 0 to stop the timer
            if self.player.hp <= 0:
                self.timer_running = False  # Stop the timer

            #Enemy Spawn Handling
            if self.enemySpawnTimer >= self.enemySpawnTimermax:
                #Check Kills for current game and allow Higher Enemy Spawn
                if self.kills >= self.enemy_threshold:
                    if self.enemy_level == 0:
                        self.enemy_level = 1
                        self.enemy_typelist.append("normal")
                        self.enemy_threshold = 20
                        print("normal Unlocked")
                    elif self.enemy_level == 1:
                        self.enemy_level = 2
                        self.enemy_typelist.append("strong")
                        print("strong Unlocked")
                #Choose Enemy Type and Spawn off screen
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
                enemy.update(self.screen,self.player,self.player.projectiles)
                if enemy.dead:
                    self.enemies.remove(enemy)
                    self.score += 100
                    self.kills += 1
                    #print(self.levelspike)

            """if self.enemySpawnTimermax > 5 and self.levelspike >= 1000:
                self.enemySpawnTimermax -=5
                self.levelspike = 0
                print("Diffculty inceased")"""
            
            #Draw the timer
            self.draw_clock()
            
            self.display.blit(self.screen, (0,0))
            pygame.display.flip()
            self.clock.tick(60) 

if __name__ == "__main__":
    instance = Game()
    instance.game_loop()


