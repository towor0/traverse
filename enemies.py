import pygame
import random
import math
import os
from helpers import posSpeed, getDistance


class Trailer:
    def __init__(self, x, y, scale):
        self.pos = pygame.Vector2(x * scale + scale / 2, y * scale + scale / 2)
        self.rect = pygame.Rect(0, 0, 10, 10)
        self.rect.center = self.pos
        self.speed = 1
        self.steps = (
            pygame.mixer.Sound(os.path.join("assets", "trailer_left.wav")),
            pygame.mixer.Sound(os.path.join("assets", "trailer_right.wav"))
        )
        self.stepcd = 0
        self.stepside = 0
        self.targetpos = None
        self.square = [x, y]
        self.onBlood = False
        self.inRnage = False

    def getData(self):
        return {
            "pos": self.pos,
        }

    def update(self, dt, events, gMap, scale, player, bloods):
        vel = pygame.Vector2(0, 0)
        self.square = [math.floor(self.pos.x/scale), math.floor(self.pos.y/scale)]
        self.onBlood = False
        self.inRange = False
        if not self.targetpos:
            squares = []
            if gMap[self.square[1]-1][self.square[0]] == "0":
                squares.append((self.square[0], self.square[1]-1))
            if gMap[self.square[1]+1][self.square[0]] == "0":
                squares.append((self.square[0], self.square[1]+1))
            if gMap[self.square[1]][self.square[0]+1] == "0":
                squares.append((self.square[0]+1, self.square[1]))
            if gMap[self.square[1]][self.square[0]-1] == "0":
                squares.append((self.square[0]-1, self.square[1]))
            randnum = random.randint(0, len(squares)-1)
            self.targetpos = pygame.Vector2(squares[randnum][0] * scale + scale/2, squares[randnum][1] * scale + scale/2)
            if self.speed == 3:
                self.speed = 1
        dop = abs(getDistance(self.pos, player["pos"]))
        for blood in bloods:
            dob = abs(getDistance(pygame.Vector2(blood.x, blood.y), self.pos))
            if dob < 200:
                self.targetpos = pygame.Vector2(blood.x, blood.y)
                self.speed = 3
                self.onBlood = True
        if ((dop < 150 and player["state"] == "walk") or (dop < 400 and player["state"] == "run")) or \
                (dop < 300 and player["state"] == "water") and not self.onBlood:
            self.targetpos = player["pos"]
            self.speed = 3
        if self.targetpos:
            if self.rect.collidepoint((self.targetpos.x, self.targetpos.y)):
                self.targetpos = None
            else:
                vel += posSpeed(self.pos, self.targetpos, self.speed)
        if dop < 600:
            if dop < 300:
                self.inRange = True
            if self.stepcd <= 0:
                self.steps[self.stepside % 2].set_volume((600-dop)/600)
                self.steps[self.stepside % 2].play()
                self.stepside += 1
                if self.speed == 1:
                    self.stepcd = 30
                elif self.speed == 3:
                    self.stepcd = 10
        if self.stepcd > 0:
            self.stepcd -= dt
        self.pos += vel * dt
        self.rect.center = self.pos





