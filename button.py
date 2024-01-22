import pygame
    
class Button:

    def __init__(self, text, x, y, font_name, font_size, button_color, clickable):
        self.text = text
        self.x = x
        self.y = y
        self.font = pygame.font.Font(font_name, font_size)
        self.normal_color = button_color
        self.clickable = clickable
        self.render_text()

    def render_text(self):
        self.text_surface = self.font.render(self.text, True, (0, 0, 0))
        self.text_rect = self.text_surface.get_rect()
        self.text_rect.x = self.x
        self.text_rect.y = self.y

    def draw(self, screen):
        text_surface = self.text_surface
        text_rect = self.text_rect
        screen.blit(text_surface, text_rect)

    def check_click(self, mouse_pos):
        return self.text_rect.collidepoint(mouse_pos) if self.clickable else False
    
    def check_hover(self, mouse_pos, screen):
        if self.text_rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, (0, 0, 0), self.text_rect, 1)
        else:
            pygame.draw.rect(screen, (255, 255, 255), self.text_rect, 1)