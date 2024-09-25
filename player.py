import pygame

class Player():
    def __init__(self):
        #self.image =  Set image to put
        self.rect = pygame.Rect(0, 0, 75, 100)
        self.color = (0,255,0)
        self.rect.center = (640,360)
        self.max_hp = 100
        self.hp = self.max_hp
        self.dead = False
        self.score = 0
    
    #check player status
    def player_alive(self):
        if self.hp <= 0:
            self.color = (255,0,0)
            self.dead = True
            #Player Dead

    #Handle Player input
    def input(self):
        if self.dead != True:
            key = pygame.key.get_pressed()
            if key[pygame.K_w]:
                self.rect.move_ip(0,-3)
            if key[pygame.K_a]:
                self.rect.move_ip(-3,0)
            if key[pygame.K_s]:
                self.rect.move_ip(0,3)
            if key[pygame.K_d]:
                self.rect.move_ip(3,0)

    #Draw player on to surface(Game screen)
    def draw(self,surface):
        pygame.draw.rect(surface, self.color, self.rect)

    def playerUpdate(self,surface):
        self.player_alive()
        self.input()
        self.draw(surface)