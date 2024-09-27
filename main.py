import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Game Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
PLAYER_SIZE = 40
ENEMY_SIZE = 40
BULLET_SIZE = 5

# Create Game Window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Top-Down Shooter")

# Health Bar
class Healthbar():
    def __init__(self,x ,y, w, h, max_hp):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.hp = max_hp
        self.max_hp = max_hp
    # end def

    def draw(self, surface):
        #calculate health ratio
        ratio = self.hp / self.max_hp
        pygame.draw.rect(surface, "red", (self.x, self.y, self.w, self.h))
        pygame.draw.rect(surface, "green", (self.x, self.y, self.w * ratio, self.h))
    # end def

health_bar = Healthbar(250, 200, 300, 40, 100)

# Player class
class Player:
    def __init__(self):
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT // 2
        self.size = PLAYER_SIZE
        self.speed = 5
        self.color = GREEN
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.size, self.size))
    
    def move(self, keys):
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.x += self.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.y -= self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.y += self.speed
        self.x = max(0, min(self.x, SCREEN_WIDTH - self.size))  # Keep within screen
        self.y = max(0, min(self.y, SCREEN_HEIGHT - self.size))

# Bullet class
class Bullet:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.size = BULLET_SIZE
        self.speed = 10
        self.angle = angle
    
    def move(self):
        self.x += self.speed * math.cos(self.angle)
        self.y += self.speed * math.sin(self.angle)
    
    def draw(self, screen):
        pygame.draw.circle(screen, BLACK, (int(self.x), int(self.y)), self.size)

# Enemy class
class Enemy:
    def __init__(self):
        edge = random.choice(['left', 'right', 'top', 'bottom'])
        self.size = ENEMY_SIZE
        self.speed = 2
        self.color = RED
        
        if edge == 'left':
            self.x = -self.size  # Start just off the left edge
            self.y = random.randint(0, SCREEN_HEIGHT - self.size)
        elif edge == 'right':
            self.x = SCREEN_WIDTH
            self.y = random.randint(0, SCREEN_HEIGHT - self.size)
        elif edge == 'top':
            self.x = random.randint(0, SCREEN_WIDTH - self.size)
            self.y = -self.size  # Start just off the top edge
        elif edge == 'bottom':
            self.x = random.randint(0, SCREEN_WIDTH - self.size)
            self.y = SCREEN_HEIGHT  # Start just off the bottom edge

    def move(self, player):
        # Move towards the player
        angle = math.atan2(player.y - self.y, player.x - self.x)
        self.x += self.speed * math.cos(angle)
        self.y += self.speed * math.sin(angle)
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.size, self.size))

# Collision check
def is_collision(obj1, obj2):
    return obj1.x < obj2.x + obj2.size and obj1.x + obj1.size > obj2.x and \
           obj1.y < obj2.y + obj2.size and obj1.y + obj1.size > obj2.y

# Game loop
def game_loop():
    player = Player()
    bullets = []
    enemies = []
    clock = pygame.time.Clock()
    running = True
    spawn_timer = 0
    score = 0
    font = pygame.font.SysFont(None, 36)
    
    while running:
    
        screen.fill(WHITE)
        clock.tick(60)

        #ADD
        # Draw Health Bar
        health_bar.draw(screen)
        
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Check for left mouse button click to shoot
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button is pressed
                mouse_x, mouse_y = pygame.mouse.get_pos()
                # Calculate angle between player and mouse position
                angle = math.atan2(mouse_y - (player.y + player.size // 2), mouse_x - (player.x + player.size // 2))
                bullets.append(Bullet(player.x + player.size // 2, player.y + player.size // 2, angle))

        keys = pygame.key.get_pressed()

        # Player movement
        player.move(keys)

        # Move and draw bullets
        for bullet in bullets[:]:
            bullet.move()
            bullet.draw(screen)
            # Remove bullets if they go off-screen
            if bullet.x < 0 or bullet.x > SCREEN_WIDTH or bullet.y < 0 or bullet.y > SCREEN_HEIGHT:
                bullets.remove(bullet)

        # Spawn enemies
        spawn_timer += 1
        if spawn_timer == 50:  # Spawn a new enemy every 50 frames
            enemies.append(Enemy())
            spawn_timer = 0

        # Move and draw enemies
        for enemy in enemies[:]:
            enemy.move(player)
            enemy.draw(screen)
            if is_collision(player, enemy):
                #ADD
                health_bar.hp -= 1  #Takes 1 damage for each collision
                # Ensures no more health
                if health_bar.hp <= 0: 
                    running = False  # Game over if an enemy touches the player                    
                continue

            for bullet in bullets[:]:
                if is_collision(bullet, enemy):
                    enemies.remove(enemy)  # Remove enemy if hit by a bullet
                    bullets.remove(bullet)  # Remove bullet
                    score += 1
                    break
        
        #ADD
        # When No More Health
        if health_bar.hp == 0:
            running = False

        # Draw player
        player.draw(screen)

        # Display score
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))
        
        pygame.display.update()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    game_loop()
