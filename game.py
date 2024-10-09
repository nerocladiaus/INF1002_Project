import pygame
import random
import sys
import time
from player import Player
from enemy import Enemy
from projectile import Projectile
from userLogin import load_user_data, save_user_data, load_user_total_data, add_user_total_data, save_user_total_data






def saveuserdata(score, kills):
            users = load_user_data()
            users[current_user] = {"score":score,
                                    "kills":kills,
                                    "time":elapsed_time}
            save_user_data(users)
            add_user_total_data(users)
            



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
        self.data_saved = False



    def draw_clock(self):
        if self.timer_running:
            # Calculate the elapsed time
            global elapsed_time
            elapsed_time = (pygame.time.get_ticks() - self.start_time) // 1000  # Convert to seconds
            minutes = elapsed_time // 60
            seconds = elapsed_time % 60
            timer_display = f"{minutes:02}:{seconds:02}"  # Format as MM:SS
        else:
            timer_display = "Game Over"  # Display "Game Over" when the timer stops
            
            if not self.data_saved:
                saveuserdata(self.score, self.kills)
                self.data_saved = True
            

        text_surface = self.font.render(timer_display, True, (255, 255, 255))  # White text
        text_rect = text_surface.get_rect(topright=(self.screenWidth - 10, 10))  # Top right corner
        self.screen.blit(text_surface, text_rect)

    def draw_score(self):
        score_display = f"Score: {self.score}"  # Prepare score text
        text_surface = self.font.render(score_display, True, (255, 255, 255))  # White text
        text_rect = text_surface.get_rect(topleft=(10, 10))  # Top left corner
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
            self.draw_score() # Call the draw_score function to display the score
            
            self.display.blit(self.screen, (0,0))
            pygame.display.flip()
            self.clock.tick(60)






#Login and Main Menu code

pygame.init()

SCREEN = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Menu")
font = pygame.font.SysFont("Arial", 70)


mx, my = pygame.mouse.get_pos()

def blit_text(text, textx, texty, size):
    font = pygame.font.SysFont("Arial", size)
    TEXT = font.render(text, True, "#b68f40")
    TEXT_RECT = TEXT.get_rect(center=(textx, texty))
    SCREEN.blit(TEXT, TEXT_RECT)
    


def login():
    username = ""
    while True:

        SCREEN.fill((75, 135, 180))

        mx, my = pygame.mouse.get_pos()
        
        users = load_user_data()  # Load user data from file
        usersdata = load_user_total_data()
        
        global current_user
        current_user = None # Variable for the logged in user
        

        blit_text("Login/Register", 640, 90, 70)


        for event in pygame.event.get():

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    username = username[:-1]  # Remove last character
                elif len(username) < 15:
                    username += event.unicode  # Add character to text

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                

        blit_text(username, 640, 300, 70)


        normal_color = (255, 255, 255)
        hover_color = (100,100,100)

        LOGIN_TEXT = font.render(" Login ", True, normal_color)
        LOGIN_RECT = LOGIN_TEXT.get_rect(center=(320, 500))
        if LOGIN_RECT.collidepoint((mx, my)):
            LOGIN_TEXT = font.render(" Login ", True, hover_color)
        LOGIN_BUTTON = SCREEN.blit(LOGIN_TEXT, LOGIN_RECT)

        REGISTER_TEXT = font.render(" Register ", True, normal_color)
        REGISTER_RECT = REGISTER_TEXT.get_rect(center=(960, 500))
        if REGISTER_RECT.collidepoint((mx, my)):
            REGISTER_TEXT = font.render(" Register ", True, hover_color)
        REGISTER_BUTTON = SCREEN.blit(REGISTER_TEXT, REGISTER_RECT)

        if LOGIN_BUTTON.collidepoint((mx, my)):
            if click:
                if username in users:
                    current_user = username
                else:
                    blit_text("username not found!", 640, 370, 70)
                    pygame.time.delay(1000)

        if REGISTER_BUTTON.collidepoint((mx, my)):
            if click:
                if username in users:
                    blit_text("username already exists!", 640, 370, 70)
                    pygame.time.delay(1000)
                else:
                    current_user = username
                    
                    users[username] = {"score":0,
                                       "kills":0,
                                       "time":0}
                    save_user_data(users)

                    usersdata[username] = {"score":0,
                                       "kills":0,
                                       "time":0}
                    save_user_total_data(usersdata)
                    
        if current_user:
            main_menu()
            
        click = False


        

        pygame.display.update()





def main_menu():
    while True:
        SCREEN.fill((75, 135, 180))

        mx, my = pygame.mouse.get_pos() #get the mouse position
        normal_color = (255, 255, 255)
        hover_color = (100,100,100)

        users = load_user_data()

        blit_text("MAIN MENU", 640, 50, 70)
        blit_text(f"Logged in as: {current_user}", 640, 650, 35)

        if current_user in users:
            data = users[current_user]
            text = f"Previous Score:{data['score']}"
            blit_text(text, 640, 150, 50)



        PLAY_TEXT = font.render(" PLAY ", True, normal_color)
        PLAY_RECT = PLAY_TEXT.get_rect(center=(640,250))
        if PLAY_RECT.collidepoint((mx, my)):
            PLAY_TEXT = font.render(" PLAY ", True, hover_color)
        PLAY_BUTTON = SCREEN.blit(PLAY_TEXT, PLAY_RECT)

        PROFILE_TEXT = font.render(" PLAYER PROFILE ", True, normal_color)
        PROFILE_RECT = PROFILE_TEXT.get_rect(center=(640,350))
        if PROFILE_RECT.collidepoint((mx, my)):
            PROFILE_TEXT = font.render(" PLAYER PROFILE ", True, hover_color)
        PROFILE_BUTTON = SCREEN.blit(PROFILE_TEXT, PROFILE_RECT)

        OPTIONS_TEXT = font.render(" OPTIONS ", True, normal_color)
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640,450))
        if OPTIONS_RECT.collidepoint((mx, my)):
            OPTIONS_TEXT = font.render(" OPTIONS ", True, hover_color)
        OPTIONS_BUTTON = SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

        QUIT_TEXT = font.render(" QUIT ", True, normal_color)
        QUIT_RECT = QUIT_TEXT.get_rect(center=(640,550))
        if QUIT_RECT.collidepoint((mx, my)):    
            QUIT_TEXT = font.render(" QUIT ", True, hover_color)
        QUIT_BUTTON = SCREEN.blit(QUIT_TEXT, QUIT_RECT)
        


        if PLAY_BUTTON.collidepoint((mx, my)):
            if click:
                gameloop = Game()
                gameloop.game_loop()
                
        if PROFILE_BUTTON.collidepoint((mx,my)):
            if click:
                profile()
        if OPTIONS_BUTTON.collidepoint((mx, my)):
            if click:
                options()
        if QUIT_BUTTON.collidepoint((mx, mx)):
            if click:
                pygame.quit()
                sys.exit

        click = False

        
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            


        pygame.display.update()


def profile():
    running = True
    while running:

        SCREEN.fill("black")
        users = load_user_total_data()

        PROFILE_TEXT = font.render("PROFILE", True, "BLUE")
        PROFILE_RECT = PROFILE_TEXT.get_rect(center=(640, 200))
        SCREEN.blit(PROFILE_TEXT, PROFILE_RECT)

        if current_user in users:
            data = users[current_user]
            text = f"{current_user}\nTotal Score: {data['score']}\nTotal Kills: {data['kills']}\nTotal Time: {data['time']}s"
            textlines = text.split("\n")
            y_position = 300
            for line in textlines:
                blit_text(line, 640, y_position, 70)
                y_position += 100



        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()


    
def options():
    running = True
    while running:

        SCREEN.fill("black")

        OPTIONS_TEXT = font.render("OPTIONS", True, "BLUE")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 200))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)



        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


        pygame.display.update()

def quit():
    pygame.quit()
    sys.exit()


login()





























    
        
        



#if __name__ == "__main__":
 #   instance = Game()
  #  instance.game_loop()
    
    


