import pygame
import random
import math

class Enemy():
    def __init__(self,surfaceW,surfaceH):
        self.rectsizex, self.rectsizey = 40,70
        self.color = "ORANGE"
        self.max_hp = 100
        self.hp = self.max_hp
        self.dead = False
        self.edge = random.choice(["left","right","top","bottom"])
        self.x ,self.y = 0,0

        print(self.edge)
        if self.edge == "left":
            self.x = self.rectsizex
            self.y = random.randint(0, surfaceH + self.rectsizey)
        elif self.edge == "right":
            self.x = surfaceW
            self.y = random.randint(0, surfaceH - self.rectsizey)
        elif self.edge == "top":
            self.x = random.randint(0, surfaceW - self.rectsizex)
            self.y = -self.rectsizey
        elif self.edge == "bottom":
            self.x = random.randint(0, surfaceW - self.rectsizex)
            self.y = surfaceH

        self.rect = pygame.Rect(self.x, self.y, self.rectsizex, self.rectsizey)
            
    
    #Draw rectangle on Game screen
    def draw(self,surface):
        pygame.draw.rect(surface, self.color, self.rect)
        
    #Move Enemy towards Player   
    def move(self,player):
        #Calculate x and y distance from player      
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery

        distance = math.hypot(dx,dy)
        #print(distance)
        if distance > 0:  # Avoid division by zero
            dx /= distance
            dy /= distance
            self.rect.move_ip(dx * 2, dy * 2)

    #Update Loop
    def update(self,surface,player):
        self.move(player)
        self.draw(surface)
