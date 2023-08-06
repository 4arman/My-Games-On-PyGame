import pygame
import random

clock = pygame.time.Clock()
pygame.init()
screen = pygame.display.set_mode((600, 360))
pygame.display.set_caption("Skelet Walk")
icon = pygame.image.load("Python/PyGame/images/1r.png").convert_alpha()
pygame.display.set_icon(icon)
bg = pygame.image.load("Python/PyGame/images/bg.jpg").convert()
bgsound = pygame.mixer.Sound("Python/PyGame/sound/music.mp3")
bgsound.play()
jumpsound = pygame.mixer.Sound("Python/PyGame/sound/jump.mp3")
losesound = pygame.mixer.Sound("Python/PyGame/sound/lose.mp3")
bgx = 0
playanco =  0
playerx = 150
playery = 213
playerspeed = 5
isjump = False
jumpcount = 7.5
run = True
label1 = pygame.font.Font("Python/PyGame/fonts/salma.otf", 40)
label = pygame.font.Font("Python/PyGame/fonts/salma.otf", 60)
restartlabel = label1.render("RESTART", True, "Black",)
reslabrec = restartlabel.get_rect(topleft=(247,215))
loselabel = label.render("GAME OVER", True, "Black",)
alien = pygame.image.load("Python/PyGame/images/alien.png").convert_alpha()
alienlist = []
alientime = pygame.USEREVENT +1
pygame.time.set_timer(alientime, 1000)
gameplay = True
walkleft = [
    pygame.image.load("Python/PyGame/images/left/1l.png").convert_alpha(),
    pygame.image.load("Python/PyGame/images/left/2l.png").convert_alpha(),
    pygame.image.load("Python/PyGame/images/left/3l.png").convert_alpha(),
    pygame.image.load("Python/PyGame/images/left/4l.png").convert_alpha(),
    pygame.image.load("Python/PyGame/images/left/5l.png").convert_alpha(),
    pygame.image.load("Python/PyGame/images/left/6l.png").convert_alpha(),
    pygame.image.load("Python/PyGame/images/left/7l.png").convert_alpha(),
    pygame.image.load("Python/PyGame/images/left/8l.png").convert_alpha(),
    pygame.image.load("Python/PyGame/images/left/9l.png").convert_alpha(),
]
walkright = [
    pygame.image.load("Python/PyGame/images/right/1r.png").convert_alpha(),
    pygame.image.load("Python/PyGame/images/right/2r.png").convert_alpha(),
    pygame.image.load("Python/PyGame/images/right/3r.png").convert_alpha(),
    pygame.image.load("Python/PyGame/images/right/4r.png").convert_alpha(),
    pygame.image.load("Python/PyGame/images/right/5r.png").convert_alpha(),
    pygame.image.load("Python/PyGame/images/right/6r.png").convert_alpha(),
    pygame.image.load("Python/PyGame/images/right/7r.png").convert_alpha(),
    pygame.image.load("Python/PyGame/images/right/8r.png").convert_alpha(),
    pygame.image.load("Python/PyGame/images/right/9r.png").convert_alpha(),
]
bullet = pygame.image.load("Python/PyGame/images/k.png").convert_alpha()
bullets = []
bulletsound = pygame.mixer.Sound("Python/PyGame/sound/cr.mp3")
bulletsleft = 10
while run:

    screen.blit(bg,(bgx, 0))
    screen.blit(bg,(bgx + 600,0))
    if gameplay:
        playerrec = walkleft[0].get_rect(topleft=(playerx,playery))

        if alienlist:
            
            for (i,el) in enumerate(alienlist):
                screen.blit(alien,el)
                el.x -=10

                if el.x < -10:
                    alienlist.pop(i)

                if playerrec.colliderect(el):
                    losesound.play()
                    gameplay = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            screen.blit(walkleft[playanco], (playerx, playery))
        else:
            screen.blit(walkright[playanco], (playerx, playery))

        if keys[pygame.K_LEFT] and playerx > 3:
            playerx -= playerspeed
        elif keys [pygame.K_RIGHT] and playerx < 557:
            playerx += playerspeed

        if not isjump:
            if keys[pygame.K_SPACE]:
                jumpsound.play()
                isjump = True
        else:
            if jumpcount >= -7.5:
                if jumpcount > 0:
                    playery -= (jumpcount ** 2) / 2
                else:
                    playery += (jumpcount ** 2) / 2
                jumpcount -=1
            else:
                isjump = False
                jumpcount = 7.5






        if playanco == 8:
            playanco = 0
        else:
            playanco +=1 

        bgx -=2
        if bgx == -600:
            bgx = 0

        

        if bullets:
            for (i, el) in enumerate (bullets):
                screen.blit(bullet, (el.x, el.y))
                el.x +=4

                if el.x > 605:
                    bullets.pop(i)

                if alienlist:
                    for (index, alien_e) in enumerate(alienlist):
                        if el.colliderect(alien_e):
                            bulletsound.play()
                            alienlist.pop(index)
                            bullets.pop(i)
    else:
        screen.fill((255,255,255))
        screen.blit(loselabel,(197,80))
        screen.blit(restartlabel, reslabrec)
        bullets.clear()


    mouse = pygame.mouse.get_pos()
    if reslabrec.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
        gameplay = True
        playerx = 150
        alienlist.clear()
        bulletsleft = 10

    
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
        if event.type == alientime:
            alienlist.append(alien.get_rect(topleft=(600,227)))
        if gameplay and event.type == pygame.KEYUP and event.key==pygame.K_x and bulletsleft > 0:
            bullets.append(bullet.get_rect(topleft=(playerx+30,playery+10)))
            bulletsleft -=1


    clock.tick(60)