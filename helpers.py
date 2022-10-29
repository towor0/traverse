import math
import pygame


def angleSpeed(speed, angle):
    rad = math.radians(angle)
    return pygame.Vector2(math.sin(rad) * speed, math.cos(rad) * speed)


def posSpeed(initial, final, speed):
    d = getDistance(initial, final)
    return pygame.Vector2(speed / d * (final.x - initial.x), speed / d * (final.y - initial.y))


def getDistance(p1, p2):
    return math.sqrt(math.pow(p2.x - p1.x, 2) + math.pow(p2.y - p1.y, 2))


def getAngle(p1, p2):
    np = p1 - p2
    angle = math.degrees(math.atan2(np.y, np.x) - math.radians(270))
    return angle


def drawRotatedImage(img, angle, center, surface):
    rotated_image = pygame.transform.rotate(img, angle)
    new_rect = rotated_image.get_rect(center=img.get_rect(center=(center[0], center[1])).center)
    surface.blit(rotated_image, new_rect)
