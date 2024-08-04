import pygame
import os

#  Loading Image for Base
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","base.png")))

class Base:
    VEL = 5
    WIDTH = BASE_IMG.get_width()
    IMG = BASE_IMG

    def __init__(self,y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self):
        # Moving base to left side of window
        self.x1 -= self.VEL
        self.x2 -= self.VEL    
        # Resetting bases when one base left out window
        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH
        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self,surface):
        surface.blit(self.IMG,(self.x1,self.y)) # Draw 1 Base
        surface.blit(self.IMG,(self.x2,self.y)) # Draw 2nd Base

            