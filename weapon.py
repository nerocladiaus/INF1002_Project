import pygame

class Weapon:
    def __init__(self, name, attack_speed, damage, cost):
        self.name = name
        self.attack_speed = attack_speed
        self.damage = damage
        self.cost = cost

# Weapon options (example values)
weapon_list = [
    Weapon("AK47", attack_speed=25, damage=20, cost=80),
    Weapon("Uzi", attack_speed=20, damage=10, cost=60),
    Weapon("Sniper", attack_speed=3, damage=35, cost=100),
 
]

