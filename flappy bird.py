import pygame
from pygame.locals import*
import random

pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_weidth = 664
screen_heigth = 675

#define font
font = pygame.font.SysFont("Lemon Milk", 50)

#define colours
white = (255, 255, 255)

ground_scroll = 0
scroll_speed = 4
flying = False
game_over = False
pipe_gap = 150
pipe_frequency = 1500 #miliseconds
last_pipe = pygame.time.get_ticks() - pipe_frequency
score = 0
pass_pipe = False

screen = pygame.display.set_mode((screen_weidth,screen_heigth))
pygame.display.set_caption("Flappy Bird")

#image load
bg = pygame.image.load("Python/PyGame/images/backgroundimage.jpg").convert()
ground = pygame.image.load("Python/PyGame/images/groundimage.jpg").convert()
button_image = pygame.image.load("Python/PyGame/images/restart1.png").convert_alpha()

def draw_text(text, font, text_color, x,y):
    img = font.render(text, True, text_color)
    screen.blit(img, (x,y))

def reset_game():
    pipe_group.empty()
    flappy.rect.x = 100
    flappy.rect.y = int(screen_heigth / 2)
    score = 0
    return score


class Bird(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        for num in range(1, 4):
            img = pygame.image.load(f"Python/PyGame/images/birdbig{num}.png").convert_alpha()
            self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center  = [x, y]
        self.vel = 0
        self.clciked = False

    def update(self):

        #gravity
        if flying == True:
            self.vel += 0.5
            if self.vel > 8:
                self.vel = 8
            print(self.vel)
            if self.rect.bottom < 612:
                self.rect.y += int(self.vel)

        #jump
        if game_over == False:
            if pygame.mouse.get_pressed()[0] == 1 and self.clciked == False:
                self.clciked = True
                self.vel = -10
            if pygame.mouse.get_pressed()[0] == 0:
                self.clciked = False



            #handle animation        
            self.counter +=1
            flap_coutdown = 5

            if self.counter > flap_coutdown:
                self.counter = 0
                self.index +=1
                if self.index >= len(self.images):
                    self.index = 0
            self.image = self.images[self.index]

            #rotate bird
            self.image = pygame.transform.rotate(self.images[self.index], self.vel * -2)
        else:
            self.image = pygame.transform.rotate(self.images[self.index], -90)

class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Python/PyGame/images/pipe1.png").convert_alpha()
        self.rect = self.image.get_rect()
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - pipe_gap / 2]
        if position == -1:
            self.rect.topleft = [x, y + pipe_gap / 2]

    def update(self):
        self.rect.x -= scroll_speed
        if self.rect.right < 0:
            self.kill()

class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self):

        action = False

        #get mouse cole
        pos = pygame.mouse.get_pos()

        #check mouse cole
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True

        screen.blit(self.image, (self.rect.x, self.rect.y))

        return action


bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()

flappy = Bird(100,int(screen_heigth / 2))

bird_group.add(flappy)

#create restart button
button = Button(screen_weidth // 2 - 50, screen_heigth // 2 - 100, button_image)



run = True

while run:

    clock.tick(fps)


    screen.blit(bg,(0,0))

    bird_group.draw(screen)
    bird_group.update()
    pipe_group.draw(screen)

    #draw the ground
    screen.blit(ground,(ground_scroll,618))

    #check score
    if len(pipe_group) > 0:
        if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left\
            and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right\
            and pass_pipe == False:
            pass_pipe = True
        if pass_pipe == True:
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                score += 1
                pass_pipe = False


    draw_text(str(score), font, white, (screen_weidth / 2), 20)

    #look colision
    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top < 0:
        game_over = True


    #bird hit the ground
    if flappy.rect.bottom >= 610:
        game_over = True
        flying = False


    if game_over == False and flying == True:
        time_now = pygame.time.get_ticks()
        pipe_height = random.randint(-100, 100)
        if time_now - last_pipe > pipe_frequency:
            btm_pipe = Pipe(screen_weidth, int(screen_heigth / 2) + pipe_height, -1)
            top_pipe = Pipe(screen_weidth, int(screen_heigth / 2) + pipe_height, 1)
            pipe_group.add(btm_pipe)
            pipe_group.add(top_pipe)
            last_pipe = time_now


        ground_scroll -= scroll_speed
        if abs(ground_scroll) > 30:
            ground_scroll = 0

        pipe_group.update()

    if game_over == True:
        if button.draw() == True:
            game_over = False
            score = reset_game()


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and flying == False and game_over == False:
            flying = True

    pygame.display.update()

pygame.quit()