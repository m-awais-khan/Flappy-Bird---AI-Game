import pygame
import neat
import os
import time
import random
from Bird import*
from Pipe import*
from Base import*

# initializing Pygame
pygame.font.init()

WIN_WIDTH = 500
WIN_HEIGHT = 800
GEN = 0 # Generation Counter
STAT_FONT = pygame.font.SysFont("Arial",30) # Font for text

# Load image for Background
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bg.png")))

# Drawing Window and objects on it
def draw_surface(surface,birds,pipes,base,score,gen,alive):
    surface.blit(BG_IMG,(0,0))
    for pipe in pipes:
        pipe.draw(surface)
    # Display Info
    text = STAT_FONT.render("Score : " + str(score),1,(255,255,255))
    surface.blit(text,(WIN_WIDTH - 10 - text.get_width(),10))  
    text = STAT_FONT.render("Gen : " + str(gen),1,(255,255,255))
    surface.blit(text,(10,10))
    text = STAT_FONT.render("Alive : " + str(alive),1,(255,255,255))
    surface.blit(text,(10,50))    
    base.draw(surface)
    for bird in birds: # Drawing Birds
        bird.draw(surface)
    pygame.display.update()

def main(genomes,config):
    global GEN
    GEN += 1    
    # Empty Collections of nets, genomes and birds
    nets = []
    ge = []
    birds = []
    # For All Genomes Passed Create A New Neural Network
    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g,config)
        nets.append(net)
        birds.append(Bird(230,350))
        g.fitness = 0
        ge.append(g)


    base = Base(730)
    pipes = [Pipe(600)]
    run = True
    
    surface = pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT))
    score = 0
    clock = pygame.time.Clock()
    while run:
        clock.tick(30) # 30 FPS
        for event in pygame.event.get():
            # Exit on Quit Event
            if event.type == pygame.QUIT:
                run = False
                pygame.QUIT()
                quit()     
        rem =  []       
        
        pipe_ind = 0
        if len(birds) > 0:
            if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width():
                pipe_ind = 1
        else:
            run = False
            break
        # Increasing Fitness if Bird does not collide
        for x,bird in enumerate(birds):
            bird.move()
            ge[x].fitness += 1
            ouptut = nets[x].activate((bird.y,abs(bird.y - pipes[pipe_ind].height),abs(bird.y - pipes[pipe_ind].bottom)))

            if ouptut[0] > 0.5:
                bird.jump()

        add_pipe = False
        for pipe in pipes:
            for x,bird in  enumerate(birds):
                if pipe.collide(bird):
                    # ge[x].fitness -= 1
                    birds.pop(x)
                    nets.pop(x)
                    ge.pop(x)
                    
 
                if not pipe.passed and pipe.x < bird.x:
                    pipe.passed = True
                    add_pipe = True    
            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe)         
            pipe.move()
        if add_pipe:
            score += 1
            for g in ge:
                g.fitness += 5
            pipes.append(Pipe(600))
        for r in rem:
            pipes.remove(r)
        for x,bird in enumerate(birds):
            if bird.y + bird.img.get_height() >= 730 or bird.y < 0:
                birds.pop(x)
                nets.pop(x)
                ge.pop(x)


        base.move()
        draw_surface(surface,birds,pipes,base,score,GEN,len(birds))
    
           


def run(config_path):
    config = neat.config.Config(neat.DefaultGenome,neat.DefaultReproduction,neat.DefaultSpeciesSet,
                                neat.DefaultStagnation,config_path)
    # Create Population and Add Reporters
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    # Run Simulation for Maximum of 50 Generations
    winner = p.run(main,50)



if __name__ == "__main__":
    # Load Config File
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir,"config.txt")
    run(config_path)