import pygame

class Nutrient:
    def __init__(self, x, y, type):
        self.x = x
        self.y = y
        self.type = type
        if type == 'food':
            self.color = (0, 255, 0)
        else:
            self.color = (0, 0, 255)
        self.rect = pygame.Rect(self.x, self.y, 10, 10)
        self.consumed = False
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)