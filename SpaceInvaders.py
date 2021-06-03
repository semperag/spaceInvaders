from random import randrange
from typing import List

import pygame

pygame.init()

window = pygame.display.set_mode((600, 500))

pygame.display.set_caption('Space Invaders')

alienExplosion = pygame.image.load('spaceinvaders/Explosion2.png')

squids = [pygame.image.load('spaceinvaders/SquidStill.png'), pygame.image.load('spaceinvaders/SquidMove.png'),
          alienExplosion]
crabs = [pygame.image.load('spaceinvaders/CrabStill.png'), pygame.image.load('spaceinvaders/CrabMove.png'),
         alienExplosion]
octopuses = [pygame.image.load('spaceinvaders/OctopusStill.png'), pygame.image.load('spaceinvaders/OctopusMove.png'),
             alienExplosion]

ship = pygame.image.load("spaceinvaders/Spaceship.png")
shipDestroyed = pygame.image.load("spaceinvaders/shipDestroyed3.png")

clock = pygame.time.Clock()


def playGame(start):
    score = 0

    shootSound = pygame.mixer.Sound('./shoot.wav')
    deathSound = pygame.mixer.Sound('./explosion.wav')
    killSound = pygame.mixer.Sound('./invaderkilled.wav')

    class spaceShip(object):
        def __init__(self, x, y, width, height):
            self.x = x
            self.y = y
            self.width = width
            self.height = height
            self.vel = 3
            self.health = 3
            self.switch = 0
            self.isDead = False
            self.isHidden = False
            self.hitbox = (self.x, self.y, self.width, self.height)

        def draw(self):
            if not self.isHidden:
                window.blit(ship, (self.x, self.y))

                self.hitbox = (self.x, self.y, self.width, self.height)
                # pygame.draw.rect(window, (255, 0, 0), self.hitbox, 2)
            elif not self.switch % 5 == 0 and self.switch < 100:
                window.blit(shipDestroyed, (self.x, self.y))

                self.hitbox = (self.x, self.y, self.width, self.height)
                self.switch += 1
            else:
                self.switch += 1
                if self.switch == 180:
                    self.switch = 0


        def hit(self):
            self.health -= 1
            if self.health == 0:
                self.isDead = True

    class bullet(object):
        def __init__(self, x, y, width, height):
            self.x = x
            self.y = y
            self.width = width
            self.height = height
            self.vel = 5

        def draw(self):
            pygame.draw.line(window, (255, 255, 255), (self.x + round(self.width / 2), self.y),
                             (self.x + round(self.width / 2), self.y - 6), 2)

    class alien(object):
        def __init__(self, x, y, width, height, category):
            self.x = x
            self.y = y
            self.width = width
            self.height = height
            self.vel = 11
            self.type = category
            self.isVisible = True
            self.isDying = False
            self.deathCount = 0
            self.hitbox = (self.x, self.y, self.width, self.height)

        def draw(self):
            if not self.isDying and self.isVisible:
                window.blit(self.type[move], (self.x, self.y))
            elif self.deathCount < 10:
                window.blit(self.type[2], (self.x, self.y))
                self.deathCount += 1
            else:
                self.isVisible = False

            if self.type == squids:
                self.hitbox = (self.x + 5, self.y, self.width, self.height)
            else:
                self.hitbox = (self.x, self.y, self.width, self.height)

            # if not self.isDying:
            #    pygame.draw.rect(window, (255, 0, 0), self.hitbox, 2)

        def hit(self):
            self.isDying = True

    def redrawGameWindow():
        window.fill((0, 0, 0))
        for foe in aliens:
            if foe.isVisible:
                foe.draw()
        for shot in shipBullets:
            shot.draw()
        for shot in enemyBullets:
            shot.draw()
        spaceShip.draw()
        pygame.draw.line(window, (255, 255, 255), (0, spaceShip.y + spaceShip.width),
                         (600, spaceShip.y + spaceShip.width),
                         1)
        text = font.render(str(spaceShip.health), 1, (255, 255, 255))
        window.blit(text, (25, 470))
        text = font.render("SCORE  " + str(score), 1, (255, 255, 255))
        window.blit(text, (400, 470))
        for x in range(int(spaceShip.health - 1)):
            x_pos = 60 + (x * 40)
            window.blit(ship, (x_pos, 470))

        pygame.display.update()

    def gameOverWindow(endTitle, firstOption, firstPosition):
        while True:

            for ev in pygame.event.get():

                if ev.type == pygame.QUIT:
                    pygame.quit()

                    # checks if a mouse is clicked
                if ev.type == pygame.MOUSEBUTTONDOWN and width / 2 - 50 <= mouse[0] <= width / 2 + 90 and height / 2 + \
                        50 <= mouse[1] <= height / 2 + 90:

                    # if the mouse is clicked on the
                    # button the game is terminated
                    if width / 2 - 50 <= mouse[0] <= width / 2 + 90 and height / 2 + 50 <= mouse[1] <= height / 2 + 90:
                        pygame.quit()

                if ev.type == pygame.MOUSEBUTTONDOWN and width / 2 - 50 <= mouse[0] <= width / 2 + 90 and height / 2 - \
                        50 <= mouse[1] <= height / 2 - 10:

                    # if the mouse is clicked on the
                    # button the game is terminated
                    if width / 2 - 50 <= mouse[0] <= width / 2 + 90 and height / 2 - 50 <= mouse[1] <= height / 2 - 10:
                        playGame(False)

                        # fills the screen with a color
            window.fill((5, 5, 5))

            # stores the (x,y) coordinates into
            # the variable as a tuple
            mouse = pygame.mouse.get_pos()

            # if mouse is hovered on a button it
            # changes to lighter shade
            if width / 2 - 50 <= mouse[0] <= width / 2 + 90 and height / 2 + 50 <= mouse[1] <= height / 2 + 90:
                pygame.draw.rect(window, color_light, [int(width / 2) - 50, int(height / 2) + 50, 160, 40])
                pygame.draw.rect(window, color_dark, [int(width / 2) - 50, int(height / 2) - 50, 160, 40])

            elif width / 2 - 50 <= mouse[0] <= width / 2 + 90 and height / 2 - 50 <= mouse[1] <= height / 2 - 10:
                pygame.draw.rect(window, color_dark, [int(width / 2) - 50, int(height / 2) + 50, 160, 40])
                pygame.draw.rect(window, color_light, [int(width / 2) - 50, int(height / 2) - 50, 160, 40])

            else:
                pygame.draw.rect(window, color_dark, [int(width / 2) - 50, int(height / 2) + 50, 160, 40])
                pygame.draw.rect(window, color_dark, [int(width / 2) - 50, int(height / 2) - 50, 160, 40])

                # superimposing the text onto our button
            window.blit(quitText, (int(width / 2), int(height / 2) + 50))
            window.blit(firstOption, (firstPosition, int(height / 2) - 50))
            window.blit(endTitle, (int(width / 2) - 75, int(height / 2) - 150))

            # updates the frames of the game
            pygame.display.update()

    # Main Loop
    run = True
    font = pygame.font.SysFont('comicsans', 40)
    spaceShip = spaceShip(250, 425, 34, 21)
    Rows = [[], [], [], [], [], [], [], [], [], []]
    aliens = []
    speed = 0
    numberOfAliens = 50
    originalNumber = numberOfAliens
    faster = 11
    for i in range(1, 11):
        x_axis = i * 45
        aliens.append(alien(x_axis, 5, 25, 21, squids))
        Rows[i - 1].append(aliens[-1])
        aliens.append(alien(x_axis, 50, 34, 21, crabs))
        Rows[i - 1].append(aliens[-1])
        aliens.append(alien(x_axis, 95, 34, 21, crabs))
        Rows[i - 1].append(aliens[-1])
        aliens.append(alien(x_axis, 140, 34, 22, octopuses))
        Rows[i - 1].append(aliens[-1])
        aliens.append(alien(x_axis, 185, 34, 22, octopuses))
        Rows[i - 1].append(aliens[-1])
    counter = 0
    deathCounter = 0
    shootLoop = 0
    shipShootLoop = 0
    move = 0
    shipBullets = []
    enemyBullets: List[bullet] = []
    facingRight = True
    facingLeft = False
    facingDown = False
    shots = 0

    if start:
        gameOverWindow(spaceInvadersTitle, startText, int(width / 2))

    while run:
        clock.tick(100)
        counter += 1
        shootLoop += 1
        shipShootLoop += 1

        for enemy in aliens:
            while enemy.isVisible and enemy.y >= 400:
                gameOverWindow(lostTitle, startOverText, int(width / 2.3))

        # Aliens move here
        if not spaceShip.isHidden:
            if counter >= 90 - round(speed):
                if move == 0:
                    move = 1
                else:
                    move = 0
                for enemy in aliens:
                    if enemy.isVisible:
                        if facingRight and enemy.x + enemy.width > 600 - 10:
                            facingDown = True
                            facingLeft = True
                            facingRight = False
                        elif facingLeft and enemy.x < 10:
                            facingDown = True
                            facingRight = True
                            facingLeft = False

                for enemy in aliens:
                    if enemy.isVisible:
                        if facingDown:
                            enemy.y += 21

                        if facingRight and not enemy.isDying:
                            enemy.x += enemy.vel
                        elif facingLeft and not enemy.isDying:
                            enemy.x -= enemy.vel

                facingDown = False
                counter = 0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            if shootLoop >= 90 and Rows:
                random = int(randrange(0, len(Rows)))
                while not Rows[random]:
                    del Rows[random]
                    random = int(randrange(0, len(Rows)))
                enemy = Rows[random][-1]
                while not enemy.isVisible and Rows:
                    shots += 1
                    del Rows[random][-1]
                    if not Rows[random]:
                        del Rows[random]
                    if Rows:
                        random = int(randrange(0, len(Rows)))
                        enemy = Rows[random][-1]
                if enemy.isVisible:
                    enemyBullets.append(bullet(enemy.x, enemy.y + 6, enemy.width, enemy.height))

                shootLoop = 0

            keys = pygame.key.get_pressed()

            if keys[pygame.K_SPACE] and shipShootLoop >= 90:
                shootSound.play()
                shipBullets.append(bullet(spaceShip.x, spaceShip.y, int(spaceShip.width), int(spaceShip.height)))
                shipShootLoop = 0

            if keys[pygame.K_RIGHT] and spaceShip.x + 37 < 600:
                spaceShip.x += spaceShip.vel
            elif keys[pygame.K_LEFT] and spaceShip.x > 0:
                spaceShip.x -= spaceShip.vel

            if shipBullets:

                index = 0
                for enemy in aliens:
                    if enemy.isVisible:
                        if shipBullets and shipBullets[0].y - 6 < enemy.hitbox[1] + enemy.hitbox[3] and shipBullets[0].y > \
                                enemy.hitbox[1]:
                            if enemy.hitbox[0] + enemy.hitbox[2] > shipBullets[0].x + round(shipBullets[0].width / 2) > \
                                    enemy.hitbox[0]:
                                killSound.play()
                                if enemy.type == octopuses:
                                    score += 10
                                elif enemy.type == crabs:
                                    score += 20
                                elif enemy.type == squids:
                                    score += 30

                                numberOfAliens -= 1
                                enemy.hit()
                                del shipBullets[0]

                                if numberOfAliens == 1:
                                    speed = 87
                                elif numberOfAliens <= round(originalNumber * 0.87):
                                    speed += faster
                                    if faster > 2:
                                        faster -= 1
                                    originalNumber = numberOfAliens

                if shipBullets:
                    if shipBullets[0].y <= 0:
                        del shipBullets[0]
                    else:
                        shipBullets[0].y -= shipBullets[0].vel

            if enemyBullets:
                index = 0
                for i in range(len(enemyBullets)):
                    if enemyBullets[index].y > spaceShip.y + spaceShip.width:
                        del enemyBullets[index]
                        index -= 1
                    else:
                        enemyBullets[index].y += (enemyBullets[index].vel - 2)

                        if enemyBullets[index].y + 6 < spaceShip.hitbox[1] + spaceShip.hitbox[3] and enemyBullets[index].y > \
                                spaceShip.hitbox[1]:
                            if spaceShip.hitbox[0] + \
                                    spaceShip.hitbox[2] > enemyBullets[index].x + round(enemyBullets[index].width / 2) > \
                                    spaceShip.hitbox[0]:
                                deathSound.play()
                                spaceShip.isHidden = True
                                deathCounter += 1
                                del enemyBullets[index]
                                index -= 1
                                spaceShip.hit()

                    index += 1

            while numberOfAliens == 0:
                gameOverWindow(winnerTitle, startOverText, int(width / 2.3))
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
        else:
            deathCounter += 1
            if deathCounter == 180:
                spaceShip.isHidden = False
                deathCounter = 0

        if deathCounter == 0:
            while spaceShip.isDead:
                gameOverWindow(lostTitle, startOverText, int(width / 2.3))
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()

        if run:
            redrawGameWindow()

    pass


# white color
color = (255, 255, 255)

# light shade of the button
color_light = (170, 170, 170)

# dark shade of the button
color_dark = (100, 100, 100)

# stores the width of the
# screen into a variable
width = window.get_width()

# stores the height of the
# screen into a variable
height = window.get_height()

# defining a font
smallfont = pygame.font.SysFont('Corbel', 35)

# rendering a text written in
quitText = smallfont.render('quit', True, color)
startText = smallfont.render('start', True, color)
startOverText = smallfont.render('play again', True, color)
spaceInvadersTitle = smallfont.render('Space Invaders', True, color)
lostTitle = smallfont.render('You Have Lost', True, color)
winnerTitle = smallfont.render('You Have Won!', True, color)

playGame(True)
