import pygame
from gui import GameGUIController
from player import Player
from map import MapController
from enemies import *


class GameController:
    def __init__(self, level):
        self.map = MapController(level)
        self.gui = GameGUIController(self.map.hole)
        self.enemies = []
        self.bloods = []
        for enemyName, enemyData in self.map.datas["Enemies"].items():
            if "Trailer" in enemyName:
                self.enemies.append(Trailer(enemyData["x"], enemyData["y"], self.map.datas["Size"]["scale"]))
        self.player = Player(self.map.datas["Player"]["x"], self.map.datas["Player"]["y"], self.map.datas["Size"]["scale"])
        pygame.mouse.set_pos(600, 450)
        self.status = "in"

    def update(self, dt, events):
        self.player.update(dt, events, self.map.map, self.map.datas["Size"]["scale"])
        playerData = self.player.getData()
        if playerData["cut"]:
            self.bloods.append(pygame.Vector3(playerData["pos"].x, playerData["pos"].y, 255))
        for enemy in self.enemies:
            enemy.update(dt, events, self.map.map, self.map.datas["Size"]["scale"], playerData, self.bloods)
            if enemy.onBlood:
                for i in range(len(self.bloods)):
                    if enemy.rect.collidepoint(self.bloods[i].x, self.bloods[i].y):
                        self.bloods[i].z -= dt
                    if self.bloods[i].z <= 0:
                        self.bloods.pop(i)
            if enemy.inRange:
                self.player.sanity += dt/20
            if enemy.rect.collidepoint(playerData["pos"]):
                self.status = "killed"
        if playerData["sanity"] >= 100:
            self.status = "sanity"
        if playerData["situation"] == "3":
            self.status = "win"
        self.gui.update(dt, events, playerData, [enemy.getData() for enemy in self.enemies])

    def draw(self, window):
        self.player.draw(window)
        self.gui.draw(window, self.bloods)
