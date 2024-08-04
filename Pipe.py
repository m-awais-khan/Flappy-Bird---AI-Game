import pygame
import os
import random 

# Load Image for Pipe
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","pipe.png")))

class Pipe:
    GAP = 200
    VEL = 5

    def __init__(self,x):
        self.x = x
        self.height = 0

        self.top = 0
        self.bottom = 0
        self.PIPE_TOP = pygame.transform.flip(PIPE_IMG,False,True) # Flipping image for Top Pipe
        self.PIPE_BOTTOM = PIPE_IMG # Image for Bottom Pipe
        self.passed = False # bird passed pipe or not
        self.set_height()   

    def set_height(self):
        self.height = random.randrange(50,450)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP

    def move(self):
        self.x -= self.VEL
        
    def draw(self,surface):
        # Drawing Top and Bottom Pipe
        surface.blit(self.PIPE_TOP,(self.x,self.top))
        surface.blit(self.PIPE_BOTTOM,(self.x,self.bottom))

    def collide(self,bird):
        # Calculating that if bird collides pipe or not
        bird_mask = bird.getMask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)
        top_offset = (self.x-bird.x,self.top - round(bird.y))
        bottom_offset = (self.x-bird.x,self.bottom - round(bird.y))
        
        b_point = bird_mask.overlap(bottom_mask,bottom_offset)  # If not Collides its return None
        t_point = top_mask.overlap(top_mask,top_offset)  # If not Collides its return None

        if b_point or t_point:
            return True
        return False

