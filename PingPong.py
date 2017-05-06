import pygame
import random
import sys

pygame.init() #initialize the pygame module

#game variables
gameWidth = 800 #Game window width
gameHeight = 600 #Game window height
gameDisplay = pygame.display.set_mode((gameWidth, gameHeight)) #the the WxH

pygame.display.set_caption("PING PONG") #defines screren name

clock = pygame.time.Clock() #tracks time of the game
gameRunning = True #defines that the game is running so I can run the loop

pHeight = 200 #bar height
#OBS: the bar height is here because its the same for both the enemy and player
myFont = pygame.font.Font("freesansbold.ttf", 20) #def the font and size

#colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

'''
Bar(): Class for the bars
variables:
    x and y are the initial position
    defY is the default Y position
    score is the amount of points the player has
    rect is the Rectangle for the bar
functions:
    keyHandler() checks what key was pressed and moves the bar accordingly
    showScore(): creates a text using the myLabel defined above as font and
    font-size, the text shows the Score of the player on the given coordinates
    when the function is called
    checkCollision(): check if the bar has collided with the Y axis of the game
    screen, if true, it stops the bar
    draw(): draws the bar on the screen
    cheapAI(): is only called for the bot, it's a cheap ai to follow the ball
    and always hit it back - I am still working on it
'''
class Bar():
    def __init__(self, x, y):
        self.x = x #defines initial position of the bar
        self.y = y
        self.defY = y
        self.score = 0
        self.rect = pygame.rect.Rect((self.x, self.y, 10, pHeight))

    def keyHandler(self, UP, DOWN): #Player movments
        key = pygame.key.get_pressed()
        if key[UP]:
            self.rect.move_ip(0, -2)
        if key[DOWN]:
            self.rect.move_ip(0, 2)

    def showScore(self, scrX, scrY):
        #defines the score as the text to display and the xy coordinates
        label = myFont.render(str(self.score), 1, (255, 255, 255))
        gameDisplay.blit(label, (scrX, scrY))

    def checkCollision(self): #checks collision with screen edges only
        if (self.rect.y <= 0):
            self.rect.y = 0
        if (self.rect.y + pHeight >= gameHeight):
            self.rect.y = gameHeight - pHeight

    def draw(self, surface):
        pygame.draw.rect(gameDisplay, WHITE, self.rect)

    def cheapAI(self):
        self.rect.y = ball.rect.y

player = Bar(0, ((gameHeight / 2) - (pHeight / 2)))
enemy = Bar((gameWidth - 10), ((gameHeight / 2) - (pHeight / 2)))

'''
Ball(): is the class for the ball, it initially defines the following
variables:
    dirX and dirY are the direction the ball is going
    defX and defY are the initial position of the ball(center of the screen)
    velocity is the speed of the ball
    and rect is the Rectangle of the ball
functions:
    draw(): draws the ball on the screen
    start(): start the ball movment towards the direction defined on the object
    creation
    collisionwalls(): checks if the ball is colliding with the Y walls, and if
    true, changes the Y direction of the ball
    collisionBars(): checks if the ball is colliding with the bars and if so,
    the ball dirX changes
    checkWin(): Checks if either player won the game and if so it gives a point
    to the winner and call the Restart() function
'''
class Ball():
    def __init__(self, dirX, dirY):
        self.dirX = dirX
        self.dirY = dirY
        self.defX = (gameWidth / 2 - 5)
        self.defY = (gameHeight / 2 - 5)
        self.velocity = 2
        self.rect = pygame.rect.Rect((self.defX,self.defY , 10, 10))

    def draw(self, surface):
        pygame.draw.rect(gameDisplay, WHITE, self.rect)

    def start(self):
        self.rect.move_ip(self.dirX, self.dirY)

    def collisionWalls(self):
        if (self.rect.y <= 0):
            self.dirY = self.velocity
        if (self.rect.y >= (gameHeight - 10)):
            self.dirY = -self.velocity

    def collisionBars(self):
        if (self.rect.colliderect(player)):
            self.dirX = self.velocity
        elif (self.rect.colliderect(enemy)):
            self.dirX = -self.velocity

    def checkWin(self):
        if (self.rect.x <= 0):
            enemy.score += 1
            Restart("Player")
        elif (self.rect.x >= (gameWidth - 10)):
            player.score += 1
            Restart("Enemy")

#Handles the events and keypress related to quitting the game
def exitHandler():
    global gameRunning

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameRunning = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                gameRunning = False

ball = Ball(-2, -2)

'''
Restart(): This funcion is called when the ball touches either edge of the
screen in the X axys, or, in other words, when either the player or the
machine(HA) loses. It will position both bars and the ball on the initial
position and will display "Lost" on the screen
'''
def Restart(who):
    youLose = myFont.render("{0} LOST!".format(who), 1, WHITE)
    gameDisplay.blit(youLose, (((gameWidth / 2) - (youLose.get_width() / 2)),
            gameHeight / 2))

    player.rect.y = ((gameHeight / 2) - (pHeight / 2))
    enemy.rect.y = ((gameHeight / 2) - (pHeight / 2))
    ball.rect.x = ball.defX
    ball.rect.y = ball.defY

while gameRunning:
    exitHandler()
    gameDisplay.fill((0, 0, 0))

    player.draw(gameDisplay)
    player.keyHandler(pygame.K_w, pygame.K_s)
    player.checkCollision()
    player.showScore(100, 100)

    enemy.draw(gameDisplay)
    enemy.cheapAI()
    enemy.checkCollision()
    enemy.showScore((gameWidth - 100), 100)

    ball.draw(gameDisplay)
    ball.start()
    ball.collisionWalls()
    ball.collisionBars()
    ball.checkWin()

    pygame.display.update() #update game display
    clock.tick(120) #game framerate

sys.exit()
