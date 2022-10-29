import pygame
import os
from helpers import angleSpeed


class Player:
    def __init__(self, x, y, scale):
        self.angle = 0
        self.pos = pygame.Vector2(x*scale+scale/2, y*scale+scale/2)
        self.mousesens = 0.1
        self.speed = 2
        self.steps = (
            pygame.mixer.Sound(os.path.join("assets", "player_left.wav")),
            pygame.mixer.Sound(os.path.join("assets", "player_right.wav"))
        )
        self.waterSteps = (
            pygame.mixer.Sound(os.path.join("assets", "player_water_left.wav")),
            pygame.mixer.Sound(os.path.join("assets", "player_water_right.wav"))
        )
        self.stepcd = 0
        self.stepside = 0
        self.state = "walk"
        self.situation = 0
        self.cut = False
        self.sanity = 0
        self.cutSound = pygame.mixer.Sound(os.path.join("assets", "cut.wav"))

    def getData(self):
        return {
            "angle": self.angle,
            "pos": self.pos,
            "situation": self.situation,
            "state": self.state,
            "cut": self.cut,
            "sanity": self.sanity
        }

    def update(self, dt, events, gMap, scale):
        mouse = pygame.mouse.get_rel()[0]
        pressedKeys = pygame.key.get_pressed()
        self.angle += mouse * self.mousesens
        self.angle %= 360
        self.state = "stop"
        self.cut = False
        mAngle = [-int(pressedKeys[pygame.K_a]) + int(pressedKeys[pygame.K_d]),
                  -int(pressedKeys[pygame.K_w]) + int(pressedKeys[pygame.K_s])]
        fAngle = 0
        if mAngle[0] and mAngle[1]:
            if mAngle[0] == 1:
                if mAngle[1] == 1:
                    fAngle = 135
                if mAngle[1] == -1:
                    fAngle = 45
            elif mAngle[0] == -1:
                if mAngle[1] == 1:
                    fAngle = 225
                if mAngle[1] == -1:
                    fAngle = 315
        elif mAngle[0]:
            if mAngle[0] == 1:
                fAngle = 90
            elif mAngle[0] == -1:
                fAngle = 270
        elif mAngle[1] == 1:
            fAngle = 180
        vel = pygame.Vector2(0, 0)
        if mAngle[0] or mAngle[1]:
            if gMap[int(self.pos.y/scale)][int(self.pos.x/scale)] == "2":
                vel += angleSpeed(self.speed / 2, self.angle + fAngle) * dt
                self.state = "walk"
                if self.stepcd <= 0:
                    self.waterSteps[self.stepside % 2].play()
                    self.stepcd = 60
                    self.stepside += 1
                    self.state = "water"
            elif pressedKeys[pygame.K_LSHIFT]:
                vel += angleSpeed(self.speed * 2, self.angle + fAngle) * dt
                if self.stepcd <= 0:
                    self.steps[self.stepside % 2].play()
                    self.stepcd = 15
                    self.stepside += 1
                    self.state = "run"
            else:
                vel += angleSpeed(self.speed, self.angle + fAngle) * dt
                if self.stepcd <= 0:
                    self.steps[self.stepside % 2].play()
                    self.stepcd = 30
                    self.stepside += 1
                    self.state = "walk"
        if self.stepcd > 0:
            self.stepcd -= dt
        if gMap[int((self.pos + vel).y/scale)][int((self.pos + vel).x/scale)] == "1":
            if gMap[int((self.pos + vel).y/scale)][int(self.pos.x/scale)] != "1":
                vel.x = 0
            elif gMap[int(self.pos.y/scale)][int((self.pos + vel).x/scale)] != "1":
                vel.y = 0
            else:
                vel = pygame.Vector2(0, 0)
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.cut = True
                self.cutSound.play()
                self.sanity += 25
        if self.sanity - dt/30 > 0:
            self.sanity -= dt/30
        else:
            self.sanity = 0
        self.pos += vel
        self.situation = gMap[int(self.pos.y/scale)][int((self.pos + vel).x/scale)]

    def draw(self, window):
        pass
