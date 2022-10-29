import pygame
from game_controller import GameController
from gui import GUIController


class Controller:
    def __init__(self):
        self.level = 0
        self.gameController = None
        self.guiController = GUIController()

    def update(self, dt, events):
        self.guiController.update(dt, events)
        if self.gameController:
            self.gameController.update(dt, events)
            if self.gameController.status == "win":
                if self.level + 1 > 3:
                    self.guiController.win = True
                    self.gameController = None
                else:
                    self.level += 1
                    self.guiController.land = True
                    self.guiController.alpha = 255
                    self.guiController.cd = 60
                    self.gameController = GameController(self.level)
            elif self.gameController.status == "sanity":
                self.guiController.alpha = 255
                self.guiController.earRingPlayed = False
                self.gameController = GameController(self.level)
            elif self.gameController.status == "killed":
                self.guiController.cd = 180
                self.guiController.killed = True
                self.gameController = None
        elif self.guiController.killed:
            pass
        else:
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pygame.mixer.music.play(-1)
                    self.gameController = GameController(self.level)

    def draw(self, window):
        if self.gameController:
            self.gameController.draw(window)
        self.guiController.draw(window)
