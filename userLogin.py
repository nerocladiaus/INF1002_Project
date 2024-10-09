import pygame, sys
import os

# Initialize Pygame
pygame.init()

# Constants for screen dimensions and frames per second

font = pygame.font.SysFont("Arial", 36)  # Default font for text rendering
SCREEN = pygame.display.set_mode((1280, 720))

# Setup display

# Window title

# User data file to store usernames and scores
USER_FILE = "users.txt"
USER_FILE2 = "usersdata.txt"



def blit_text(text, textx, texty):
    TEXT = font.render(text, True, "#b68f40")
    TEXT_RECT = TEXT.get_rect(center=(textx, texty))
    SCREEN.blit(TEXT, TEXT_RECT)
    pygame.display.flip()


# Load user data from the file
def load_user_data():
    if not os.path.exists(USER_FILE):  # Check if the file exists
        return {}
    users = {}
    with open(USER_FILE, 'r') as file:
        for line in file:
            username, score, kills, time = line.strip().split(',')  # Split line into username and score
            users[username] = {
                "score": int(score),
                "kills": int(kills),
                "time": int(time)}  # Store in a dictionary
    return users



# Save user data to the file
def save_user_data(users):
    with open(USER_FILE, 'w') as file:  # Open file in write mode
        for username, data in users.items():
            score = data["score"]
            kills = data["kills"]
            time = data["time"]
            file.write(f"{username},{score},{kills},{time}\n")
    

def load_user_total_data():
    if not os.path.exists(USER_FILE2):  # Check if the file exists
        return {}
    usersdata = {}
    with open(USER_FILE2, 'r') as file:
        for line in file:
            username, score, kills, time = line.strip().split(',')  # Split line into username and score
            usersdata[username] = {
                "score": int(score),
                "kills": int(kills),
                "time": int(time)}  # Store in a dictionary
    return usersdata

def save_user_total_data(users):
    with open(USER_FILE2, 'w') as file:  # Open file in write mode
        for username, data in users.items():
            score = data["score"]
            kills = data["kills"]
            time = data["time"]
            file.write(f"{username},{score},{kills},{time}\n")

def add_user_total_data(userstat):

    users = load_user_total_data()

    with open(USER_FILE2, 'r') as file:  # Open file in write mode
        for line in file:
            username, score, kills, time = line.strip().split(',')
            users[username] = {
                "score": int(score),
                "kills": int(kills),
                "time": int(time)}
            
    for username, data in userstat.items():
        users[username]["score"] += data["score"]
        users[username]["kills"] += data["kills"]
        users[username]["time"] += data["time"]

    with open(USER_FILE2, 'w') as file:  # Open file in write mode
        for username, data in users.items():
            score = data["score"]
            kills = data["kills"]
            time = data["time"]
            file.write(f"{username},{score},{kills},{time}\n")   








    