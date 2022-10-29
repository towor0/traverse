import pygame
import os
import json


class MapController:
    def __init__(self, level):
        with open(os.path.join("assets", "maps", f"{level}.json")) as f:
            self.datas = json.load(f)
        self.map = self.datas["Map"].split("|")
        for y in range(len(self.map)):
            for x in range(len(self.map[0])):
                if self.map[y][x] == "3":
                    self.hole = pygame.Vector2(x * self.datas["Size"]["scale"] + self.datas["Size"]["scale"]/2,
                                               y * self.datas["Size"]["scale"] + self.datas["Size"]["scale"]/2)
