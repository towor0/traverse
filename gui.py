import pygame
import os
from helpers import getDistance, getAngle, drawRotatedImage
import random


class GameGUIController:
    def __init__(self, hole):
        self.compassWindow = pygame.Surface((720, 48)).convert_alpha()
        self.compass = pygame.image.load(os.path.join("assets", "compass.png")).convert_alpha()
        self.compassPointer = pygame.image.load(os.path.join("assets", "compass_pointer.png")).convert_alpha()
        self.enemyIndicator = pygame.image.load(os.path.join("assets", "enemy_indicator.png")).convert()
        self.holeIndicator = pygame.image.load(os.path.join("assets", "hole_indicator.png")).convert()
        self.blood = pygame.image.load(os.path.join("assets", "blood.png"))
        self.sanity = pygame.image.load(os.path.join("assets", "sanity.png")).convert_alpha()
        self.sanityBar = pygame.image.load(os.path.join("assets", "sanity_bar.png")).convert_alpha()
        self.bloodcd = 0
        self.compassPos = []
        self.enemyIndicators = []
        self.map = Map()
        self.enemies = []
        self.playerAngle = 0
        self.playerSanity = 0
        self.hole = hole
        self.holeInfo = (0, 0)
        self.sanityPanel = SanityPanel()

    def update(self, dt, events, player, enemies):
        self.enemies = enemies
        self.playerAngle = player["angle"]
        self.playerSanity = player["sanity"]
        self.enemyIndicators = []
        angle = round(player["angle"])
        self.compassPos = (-360 - angle * 2, 360 - angle * 2, 1080 - angle * 2)
        for enemy in enemies:
            if abs(getDistance(player["pos"], enemy["pos"])) < 600:
                self.enemyIndicators.append((getAngle(player["pos"], enemy["pos"]),
                                             (600 - abs(getDistance(player["pos"], enemy["pos"]))) / 600 * 255))
        if abs(getDistance(player["pos"], self.hole)) < 600:
            self.holeInfo = (getAngle(player["pos"], self.hole),
                             (600 - abs(getDistance(player["pos"], self.hole))) / 600 * 255)
        self.map.update(dt, events, player)
        if player["cut"]:
            self.bloodcd = 255
        if self.bloodcd > 0:
            self.bloodcd -= dt
        self.sanityPanel.update(player["sanity"])

    def draw(self, window, bloods):
        self.compassWindow.fill((0, 0, 0, 0))
        for x in self.compassPos:
            self.compassWindow.blit(self.compass, (x, 0))
        for enemy in self.enemyIndicators:
            self.enemyIndicator.set_alpha(enemy[1])
            drawRotatedImage(self.enemyIndicator, enemy[0] + self.playerAngle, (600, 450), window)
        self.holeIndicator.set_alpha(self.holeInfo[1])
        drawRotatedImage(self.holeIndicator, self.holeInfo[0] + self.playerAngle, (600, 450), window)
        self.compassWindow.blit(self.compassPointer, (352, 32))
        self.map.draw(window, self.enemies, bloods)
        window.blit(self.sanity, (10, 850))
        window.blit(self.sanityBar, (108, 848))
        pygame.draw.rect(window, (255, 255, 255), (110, 850, self.playerSanity * 5, 30))
        self.blood.set_alpha(self.bloodcd)
        window.blit(self.blood, (0, 0))
        window.blit(self.compassWindow, (240, 0))
        self.sanityPanel.draw(window)


class Map:
    def __init__(self):
        self.mapWindow = pygame.Surface((296, 296)).convert_alpha()
        self.mapDisplay = pygame.Surface((600, 600)).convert_alpha()
        self.trails = []
        self.trailcd = 0
        self.playerPos = None
        self.waterMarks = []
        self.angle = 0

    def update(self, dt, events, player):
        self.playerPos = player["pos"]
        self.angle = player["angle"]
        if self.trailcd <= 0:
            self.trails.append(pygame.Vector3(self.playerPos.x, self.playerPos.y, 255))
            self.trailcd = 10
            if player["situation"] == "2":
                self.waterMarks.append(pygame.Vector2(self.playerPos.x, self.playerPos.y))
        else:
            self.trailcd -= dt
        for trail in self.trails:
            if trail.z > 0:
                trail.z -= dt * 3
            if trail.z < 0:
                self.trails.pop(self.trails.index(trail))

    def draw(self, window, enemies, bloods):
        pygame.draw.rect(window, (255, 255, 255), (900, 600, 300, 300))
        pygame.draw.rect(window, (0, 0, 0), (902, 602, 296, 296))
        self.mapDisplay.fill((0, 0, 0))
        for trail in self.trails:
            if trail:
                pygame.draw.rect(self.mapDisplay, (255, 255, 255, trail.z),
                                 (trail.x - self.playerPos.x + 298, self.playerPos.y - trail.y + 298, 4, 4))
        for watermark in self.waterMarks:
            pygame.draw.rect(self.mapDisplay, (0, 0, 255),
                             (watermark.x - self.playerPos.x + 298, self.playerPos.y - watermark.y + 298, 4, 4))
        for blood in bloods:
            pygame.draw.rect(self.mapDisplay, (255, 0, 0),
                             (blood.x - self.playerPos.x + 298, self.playerPos.y - blood.y + 298, 4, 4))
        pygame.draw.circle(self.mapDisplay, (255, 255, 255), (300, 300), 6)
        rotated_image = pygame.transform.rotate(self.mapDisplay, self.angle)
        new_rect = rotated_image.get_rect(center=self.mapDisplay.get_rect(center=(150, 150)).center)
        self.mapWindow.blit(rotated_image, new_rect)
        window.blit(self.mapWindow, (902, 602))


class SanityPanel:
    def __init__(self):
        self.cPixel = []

    def update(self, sanity):
        while len(self.cPixel) < sanity * 25:
            self.cPixel.append((random.randint(0, 119), random.randint(0, 89)))
        while len(self.cPixel) > sanity * 25:
            self.cPixel.pop(0)

    def draw(self, window):
        for pixel in self.cPixel:
            rdc = random.randint(0, 255)
            pygame.draw.rect(window, (rdc, rdc, rdc), (pixel[0] * 10, pixel[1] * 10, 10, 10))


class GUIController:
    def __init__(self):
        font = pygame.font.SysFont("arial", 40)
        self.startText = font.render("Click Any Where to Start", True, (255, 255, 255))
        self.start = False
        self.alpha = 255
        self.startGame = False
        self.surf = pygame.Surface((1200, 900)).convert()
        self.cd = 0
        self.land = False
        self.landing = pygame.mixer.Sound(os.path.join("assets", "landing.wav"))
        self.landingPlayed = False
        self.jsSound = pygame.mixer.Sound(os.path.join("assets", "monster_jumpscare.wav"))
        self.earRing = pygame.mixer.Sound(os.path.join("assets", "ear_ring.wav"))
        self.earRingPlayed = True
        self.jsPlayed = False
        self.killed = False
        self.win = False
        self.winText = font.render("YOU WON! :D", True, (255, 255, 255))

    def update(self, dt, events):
        if self.win:
            pass
        elif self.killed:
            if self.cd < 20 and not self.jsPlayed:
                self.jsPlayed = True
                self.jsSound.play()
            if self.cd - dt <= 0:
                pygame.quit()
        elif self.land:
            if self.cd < 10 and not self.landingPlayed:
                self.landing.play()
                self.landingPlayed = True
            if self.cd < 0:
                self.land = False
                self.landingPlayed = False
        else:
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.start = True
            if self.start:
                if self.alpha > 0:
                    self.alpha -= dt
            if not self.earRingPlayed:
                self.earRingPlayed = True
                self.earRing.play()
        self.cd -= dt

    def draw(self, window):
        if self.win:
            window.blit(self.winText, self.winText.get_rect(center=(600, 450)))
        elif self.start:
            self.surf.set_alpha(self.alpha)
            self.surf.fill((0, 0, 0))
            window.blit(self.surf, (0, 0))
        else:
            window.blit(self.startText, self.startText.get_rect(center=(600, 800)))
