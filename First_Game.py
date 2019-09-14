import pygame

pygame.init()
screenwidth = 500
win = pygame.display.set_mode((screenwidth,screenwidth))
pygame.display.set_caption("First Game")

#Images

walkRight = [pygame.image.load('Data/R%s.png' % frame) for frame in range(1, 10)] 
walkLeft = [pygame.image.load('Data/L%s.png' % frame) for frame in range(1, 10)]

bg = pygame.image.load('Data/bg.jpg')
char = pygame.image.load('Data/standing.png')

class player(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.isJump = False
        self.jumpCount = 10
        self.left = False
        self.right = False
        self.walkCount = 0

    def draw(self, win):
        if self.walkCount + 1 >= 27:
            self.walkCount = 0

        if self.left:
            win.blit(walkLeft[self.walkCount//3], (self.x,self.y))
            self.walkCount +=1
        elif self.right:
            win.blit(walkRight[self.walkCount//3],(self.x,self.y))
            self.walkCount +=1
        else:
            win.blit(char, (self.x,self.y))






#List of parameters

clock = pygame.time.Clock()




def redrawGameWindow():
    global walkCount

    win.blit(bg, (0,0))
    Stef.draw(win)

    pygame.display.update()

#mainloop
Stef = player (300, 410, 64, 64) 
run = True
while run:
    clock.tick(27)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    keys = pygame.key.get_pressed() #return a list of booleans for the entire keyboard
    if keys[pygame.K_LEFT] and Stef.x > Stef.vel:
        Stef.x-= Stef.vel
        Stef.left = True
        Stef.right = False

    elif keys [pygame.K_RIGHT] and Stef.x < screenwidth - Stef.width - Stef.vel:
        Stef.x+= Stef.vel
        Stef.left = False
        Stef.right = True

    else:
        Stef.right = False
        Stef.left = False
        Stef.walkCount = 0

    if not(Stef.isJump):    
        if keys[pygame.K_SPACE]:
            Stef.isJump = True
            Stef.right = False
            Stef.left = False

    else:
        if Stef.jumpCount >= -10:
            neg = 1
            if Stef.jumpCount <0:
                neg = -1
            Stef.y-= (Stef.jumpCount ** 2) * 0.5 * neg
            Stef.jumpCount -= 1 
        else:
            Stef.isJump = False
            Stef.jumpCount = 10

    redrawGameWindow()

    

pygame.quit()

