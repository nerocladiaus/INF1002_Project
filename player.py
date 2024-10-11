import pygame
from projectile import Projectile
from weapon import Weapon

class Player():
    def __init__(self):
        #self.image =  Set image to put
        self.color = (0,255,0)
        self.max_hp = 100
        self.hp = self.max_hp
        self.dead = False
        self.score = 0
        self.tick = 0
        self.rectsizex, self.rectsizey = 30,30
        self.x , self.y = 640,360
        self.rect = pygame.Rect(self.x, self.y, self.rectsizex, self.rectsizey)
        
    #Shooting attributes
        self.projectiles = []
        self.bulletspeed = 10
        self.reload = 4
        
        self.weapon = None  # Initialize weapon as None
        self.weapon_damage = 10
        self.weapon_purchased = None

    def draw_health_bar(self, surface):
        health_percentage = self.hp / self.max_hp
        pygame.draw.rect(surface, (255, 0, 0), (self.rect.x, self.rect.y - 10, self.rectsizex, 5))  # Red
        pygame.draw.rect(surface, (0, 255, 0), (self.rect.x, self.rect.y - 10, self.rectsizex * health_percentage, 5))  # Green
    
    #check player status
    def player_alive(self):
        if self.hp <= 0:        #Player Dead
            self.color = (255,0,0)
            self.dead = True
        elif self.tick < 4:
            self.color = "YELLOW"
        else:
            self.color = "GREEN"

    #Handle Player input
    def input(self,screen_width,screen_height):
        if self.dead != True:
            #Check Player input
            key = pygame.key.get_pressed()
            if key[pygame.K_w]:
                self.rect.move_ip(0,-3)
            if key[pygame.K_a]:
                self.rect.move_ip(-3,0)
            if key[pygame.K_s]:
                self.rect.move_ip(0,3)
            if key[pygame.K_d]:
                self.rect.move_ip(3,0)
            if pygame.mouse.get_pressed()[0]:  # If left mouse button is pressed
                self.shoot()
                
            #Prevent player from Moving offscreen/MAP
            if self.rect.left < 0:              # Left boundary
                self.rect.left = 0
            if self.rect.right > screen_width:  # Right boundary
                self.rect.right = screen_width
            if self.rect.top < 0:               # Top boundary
                self.rect.top = 0
            if self.rect.bottom > screen_height:  # Bottom boundary
                self.rect.bottom = screen_height    
                
    def shoot(self):
        if self.reload >= 16:
            #Get Mouse pos
            mouse_x, mouse_y = pygame.mouse.get_pos()
            # Calculate the direction from the player to the mouse        
            direction = pygame.Vector2(mouse_x - self.rect.centerx, mouse_y - self.rect.centery)

            if direction.length() > 0:  # Avoid division by zero
                    direction.normalize_ip()
            damage = self.weapon_damage if self.weapon is None else self.weapon.damage
            # Determine bullet speed based on weapon or default
            speed = self.bulletspeed if self.weapon is None else self.weapon.attack_speed

            projectile = Projectile(self.rect.centerx, self.rect.centery, direction, speed, damage)
            print("Projectile spawn")
            self.reload = 0
            self.projectiles.append(projectile)
        else:
            self.reload += 1

    def update_projectiles(self,surface):
        for projectile in self.projectiles:
            if projectile.hitcount >= 2:
                self.projectiles.remove(projectile)
                continue
            projectile.update()
            if projectile.rect.x < 0 or projectile.rect.x > 1280 or projectile.rect.y < 0 or projectile.rect.y > 800:
                self.projectiles.remove(projectile)  # Remove if off screen
            else:
                projectile.draw(surface)
            

    """def checkCollision(self,enemies):
        #for enemy in enemies:
            if self.rect.colliderect(enemies) and self.tick >= 4:
                self.color = "YELLOW"
                self.hp -=1
                self.tick = 0
                print(self.hp)"""

    #Draw player on to surface(Game screen)
    def draw(self,surface):
        pygame.draw.rect(surface, self.color, self.rect)
        for projectile in self.projectiles:
            projectile.draw(surface)

    def equip_weapon(self, weapon):
        """Equip a weapon and update player attributes."""
        self.weapon = weapon
        self.bulletspeed = weapon.attack_speed
        self.weapon_damage = weapon.damage
        self.weapon_purchased = weapon  # Track the purchased weapon
        print(f"Weapon equipped: {weapon.name}")

    def playerUpdate(self,surface,enemies,screen_width,screen_height):
        self.player_alive()
        #self.checkCollision(enemies)
        self.input(screen_width,screen_height)
        self.update_projectiles(surface)
        self.draw(surface)
        self.draw_health_bar(surface)
        self.tick +=1
        