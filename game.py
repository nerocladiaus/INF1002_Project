import pygame
import random
import sys
import time
from player import Player
from enemy import Enemy
from projectile import Projectile
from weapon import weapon_list
from userLogin import load_user_data, save_user_data, load_user_total_data, add_user_total_data, save_user_total_data
#from endgame import GameOver  # Import the GameOver class


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
        self.backgroundmusic = pygame.mixer.Sound('game-level-music.wav')
        self.levelup = pygame.mixer.Sound('levelup.wav')

        # Initialize Pygame font module
        pygame.font.init()
        # Set up fonts for the clock
        self.font = pygame.font.Font(None, 36)  # Initialize the font
        # Store the start time
        self.start_time = pygame.time.get_ticks()  # Time in milliseconds
        self.timer_running = True  # Initialize the timer flag
        self.data_saved = False
        # Pause
        self.paused = False # Initialize the pause state
        self.start_time = pygame.time.get_ticks()  # Time in milliseconds
        self.timer_running = True  # Initialize the timer flag
        self.data_saved = False
        self.last_score_for_weapon = 0
        self.coins = 0
        self.weapon_purchased = None
        self.endgame = False

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

    


    def draw_coins(self):
        coins_display = f"Coins: {self.coins}"
        coins_surface = self.font.render(coins_display, True, (255, 255, 255))
        coins_rect = coins_surface.get_rect(topleft=(10, 50))
        self.screen.blit(coins_surface, coins_rect)

    def pause_and_show_weapon_choices(self):
     # Pause the game
     self.timer_running = False
     self.screen.fill((255, 255, 255))

     # Set dimensions for weapon choice rectangles
     rect_width, rect_height = 200, 120  # Updated rectangle size
     spacing = 20
     total_width = 3 * rect_width + 2 * spacing
     start_x = (self.screenWidth - total_width) // 2
     center_y = (self.screenHeight - rect_height) // 2

     # Set font size for weapon text
     weapon_font_size = 36  # Change this to adjust the text size
     weapon_font = pygame.font.Font(None, weapon_font_size)

     # Create and display weapon choice rectangles
     weapon_choice_rects = []
     if self.player.weapon is None:
        choices = [{"weapon": weapon, "cost": weapon.cost} for weapon in weapon_list[:3]]
        message = "Choose a weapon (costs coins)"
     else:
        # Display options for upgrading the current weapon
        choices = [
            {"weapon": self.player.weapon, "cost": 50, "upgrade": "attack_speed"},
            {"weapon": self.player.weapon, "cost": 50, "upgrade": "damage"},
            {"weapon": None, "cost": 0, "upgrade": "skip"}
        ]
        message = "Upgrade your weapon"

     for i, choice in enumerate(choices):
        rect = pygame.Rect(start_x + i * (rect_width + spacing), center_y, rect_width, rect_height)
        weapon_choice_rects.append((rect, choice))

        # Draw the weapon choice rectangle
        pygame.draw.rect(self.screen, (255, 255, 255), rect)
        pygame.draw.rect(self.screen, (0, 0, 0), rect, 3)

        # Customize the text based on the choice
        if "upgrade" in choice:
         if choice["upgrade"] == "attack_speed":
            line1 = "Upgrade"
            line2 = "Attack Speed"
            cost_text = f"(${choice['cost']})"
         elif choice["upgrade"] == "damage":
            line1 = "Upgrade"
            line2 = "Damage"
            cost_text = f"(${choice['cost']})"
         else:
            line1 = "Skip"
            line2 = ""
            cost_text = ""
        else:
            line1 = choice['weapon'].name
            line2 = ""
            cost_text = f"(${choice['cost']})"

        # Render the text with the updated font size
        line1_surface = weapon_font.render(line1, True, (0, 0, 0))
        line2_surface = weapon_font.render(line2, True, (0, 0, 0))
        cost_surface = weapon_font.render(cost_text, True, (0, 0, 0))
        text_y = rect.y + (rect_height // 2 - line1_surface.get_height() - 10)
        self.screen.blit(line1_surface, (rect.x + 8, text_y))
        if line2:
          self.screen.blit(line2_surface, (rect.x + 8, text_y + line1_surface.get_height() + 5))
        if cost_text:
          self.screen.blit(cost_surface, (rect.x + 8, text_y + line1_surface.get_height() + line2_surface.get_height() + 10))

     # Display message at the top
     message_surface = self.font.render(message, True, (0, 0, 0))
     message_rect = message_surface.get_rect(center=(self.screenWidth // 2, center_y - 70))
     self.screen.blit(message_surface, message_rect)

     self.display.blit(self.screen, (0, 0))
     pygame.display.flip()

    # Wait for player selection
     selected_choice = None
     while not selected_choice:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                for rect, choice in weapon_choice_rects:
                    if rect.collidepoint(mouse_pos):
                        # Check if the player has enough coins for the selection
                        if self.coins >= choice["cost"]:
                            selected_choice = choice
                            if "upgrade" in choice:
                                # Upgrade the current weapon
                                if choice["upgrade"] == "attack_speed":
                                    self.player.weapon.attack_speed = max(1, self.player.weapon.attack_speed + 3)
                                elif choice["upgrade"] == "damage":
                                    self.player.weapon.damage += 5
                            else:
                                # Equip the new weapon
                                self.player.equip_weapon(choice["weapon"])
                            # Deduct coins for the selection
                            self.coins -= choice["cost"]
                            print(f"Purchased {choice['upgrade'] if 'upgrade' in choice else choice['weapon'].name} for ${choice['cost']}. Remaining coins: {self.coins}")
                        else:
                            print("Not enough coins to make the purchase!")
                        break

         # Keep choices visible
        self.display.blit(self.screen, (0, 0))
        pygame.display.flip()

     # Resume the game
     self.timer_running = True

    def game_loop(self):
        self.player = Player()
        self.enemies = []
        self.enemySpawnTimer = 0
        self.score = 0
        self.enemySpawnTimermax = 100
        self.kills = 0
        self.enemy_threshold,self. enemy_level = 10, 0
        self.enemy_typelist = ["weak"]
        self.min_spawn_timer = 50
        self.spawn_timer_decrease_rate = 1
        self.backgroundmusic.play(loops=-1)
        self.backgroundmusic.set_volume(0.5)

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # Check for pause/unpause
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:  # Press 'Escape' to quit
                        self.running = False
                        self.backgroundmusic.stop()
                    if event.key == pygame.K_p:  # Toggle pause with 'P' key
                        self.paused = not self.paused
                        if self.paused:
                            self.timer_running = False  # Stop the timer if paused
                            self.backgroundmusic.stop()
                        else:
                            # When unpausing, reset the start_time to the current time minus the elapsed time
                            self.start_time = pygame.time.get_ticks() - (self.elapsed_time * 1000)  # Convert seconds to milliseconds
                            self.timer_running = True  # Resume the timer
                            self.backgroundmusic.play(loops=-1)

            if self.paused:
                self.screen.fill((0, 0, 0))  # Fill the screen with black
                self.draw_pause()  # Draw the pause message
                pygame.display.flip()  # Update the display
                continue  # Skip the rest of the loop if paused

            # Check if player's health is 0 to stop the timer
            if self.player.hp <= 0:
                if not self.endgame:  # Only trigger once when health reaches 0
                    self.endgame = True
                    if self.timer_running:  # Stop the timer when health is 0
                        self.timer_running = False

            #if self.endgame:
                self.draw_endgame()  # Draw the endgame screen
                pygame.display.flip()  # Update the display

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()  # Quit the game
                    
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:  # Quit the game
                            pygame.quit()
                            sys.exit()
                        #elif event.key == pygame.K_r:  # Restart the game (you need to implement reset logic)
                            #self.reset_game()  # Call your reset method to restart the game
                            #self.endgame = False  # Reset the endgame state
            else:


                if self.score // 1000 > self.last_score_for_weapon:
                    self.levelup.play()
                    self.pause_and_show_weapon_choices()
                    self.last_score_for_weapon = self.score // 1000
                    ## Display the Game Over screen
                    #game_over_screen = GameOver(self)
                    #game_over_screen.display()  # Display the game over screen

                    ## Reset health or perform any restart logic
                    #self.player.hp = 100  # Reset player health or any other restart logic
                    #self.score = 0  # Reset score if necessary
                    #self.kills = 0  # Reset kills if necessary
                    #continue  # Skip to the next iteration to avoid further processing
                    
                # Update timer only if it is running
                if self.timer_running:
                    self.elapsed_time = (pygame.time.get_ticks() - self.start_time) // 1000
                #else:
                    #self.elapsed_time = 0  # Reset elapsed_time when the timer is stopped

                #Enemy Spawn Handling
                if self.enemySpawnTimer >= self.enemySpawnTimermax:
                    #Check if spawntimer can decrease
                    print(self.elapsed_time)
                    if self.elapsed_time > 60 and self.elapsed_time < 120:
                        new_spawn_timer = self.enemySpawnTimermax - self.spawn_timer_decrease_rate
                        self.enemySpawnTimermax = max(new_spawn_timer, self.min_spawn_timer)
                        #print("New Spawn Timer lvl 1")
                    elif self.elapsed_time > 120 and self.elapsed_time < 250:
                        self.min_spawn_timer = 32
                        new_spawn_timer = self.enemySpawnTimermax - self.spawn_timer_decrease_rate
                        self.enemySpawnTimermax = max(new_spawn_timer, self.min_spawn_timer)
                        #print("New Spawn Timer lvl 2")
                    #Overwhelm Player at 5 Mins (game Win)
                    elif self.elapsed_time > 250:
                        self.min_spawn_timer = 16
                        self.spawn_timer_decrease_rate = 4
                        new_spawn_timer = self.enemySpawnTimermax - self.spawn_timer_decrease_rate
                        self.enemySpawnTimermax = max(new_spawn_timer, self.min_spawn_timer)
                        print("New Spawn Timer lvl 3")
                    print(self.enemySpawnTimermax)
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
                    enemy.update(self.screen,self.player,self.player.projectiles,self.player.weapon_damage)
                    if enemy.dead:
                        #Check Enemy type and Add score accordingly
                        if enemy.type == 'weak':
                            self.score += 50
                            self.coins += 5
                        elif enemy.type == 'normal':
                            self.score += 100
                            self.coins += 10
                        elif enemy.type == 'strong':
                            self.score += 150
                            self.coins += 15   
                        self.enemies.remove(enemy)
                        self.kills += 1
                            
                """if self.enemySpawnTimermax > 5 and self.levelspike >= 1000:
                    self.enemySpawnTimermax -=5
                    self.levelspike = 0
                    print("Diffculty inceased")"""
            
            #Draw the timer
            self.draw_clock()
            self.draw_score() # Call the draw_score function to display the score
            self.draw_coins() 

            self.display.blit(self.screen, (0,0))
            pygame.display.flip()
            self.clock.tick(60)

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

    def draw_pause(self):
        pause_surface = pygame.Surface((self.screenWidth, self.screenHeight))
        pause_surface.fill((0, 0, 0))  # Fill with black
        pause_text = "Game Paused. Press 'P' to continue."
        text_surface = self.font.render(pause_text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(self.screenWidth // 2, self.screenHeight // 2))
        pause_surface.blit(text_surface, text_rect)
        
        self.display.blit(pause_surface, (0, 0))  # Draw the pause surface onto the display

    def draw_endgame(self):
        endgame_surface = pygame.Surface((self.screenWidth, self.screenHeight))
        endgame_surface.fill((0, 0, 0))  # Fill with black
        endgame_text = "Game Over! Press 'Q' to Quit."
        text_surface = self.font.render(endgame_text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(self.screenWidth // 2, self.screenHeight // 2))
        endgame_surface.blit(text_surface, text_rect)
        
        self.display.blit(endgame_surface, (0, 0))  # Draw the pause surface onto the display

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
        if QUIT_BUTTON.collidepoint((mx, my)):
            if click:
                pygame.quit()
                sys.exit()

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
    
    


