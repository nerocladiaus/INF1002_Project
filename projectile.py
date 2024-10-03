import pygame

class Projectile:
    def __init__(self,x,y,direction, speed):
        self.rect = pygame.Rect(x, y, 5, 5)  # Small square for the projectile
        self.speed = speed
        self.direction = direction
        self.color = "YELLOW"
        self.hitcount = 0

    def update(self):
        self.rect.x += self.direction.x * self.speed
        self.rect.y += self.direction.y * self.speed
    
    def draw(self,surface):
        pygame.draw.rect(surface, self.color, self.rect)