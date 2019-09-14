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
        self.standing = True

    def draw(self, win):
        if self.walkCount + 1 >= 27:
            self.walkCount = 0

        if not(self.standing):
            if self.left:
                win.blit(walkLeft[self.walkCount//3], (self.x,self.y))
                self.walkCount +=1
            elif self.right:
                win.blit(walkRight[self.walkCount//3],(self.x,self.y))
                self.walkCount +=1
        else:
            if self.right:
                win.blit(walkRight[0], (self.x, self.y))
            else:
                win.blit(walkLeft[0], (self.x, self.y))


class projectile(object):
    def __init__(self, x, y, radius, color, facing):
        self.x=x
        self.y=y
        self.radius=radius
        self.color=color
        self.facing=facing
        self.vel= 8 * facing

    def draw(self, win):
        pygame.draw.circle(win,self.color, (self.x, self.y), self.radius) 





#List of parameters

clock = pygame.time.Clock()




def redrawGameWindow():
    global walkCount

    win.blit(bg, (0,0))
    Stef.draw(win)

    for bullet in bullets:
        bullet.draw(win)

    pygame.display.update()

#mainloop
Stef = player (300, 410, 64, 64) 
bullets = []
run = True
while run:
    clock.tick(27)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    for bullet in bullets:
        if bullet.x < 500 and bullet.x >0:
            bullet.x +=bullet.vel
        else:
            bullets.pop(bullets.index(bullet))


    
    keys = pygame.key.get_pressed() #return a list of booleans for the entire keyboard

    if keys[pygame.K_SPACE]:
        if Stef.left:
            facing = -1
        else:
            facing = 1
        if len(bullets)<5:
            bullets.append(projectile(round(Stef.x + Stef.width//2), round(Stef.y + Stef.height//2), 6, (0,0,0), facing))


    if keys[pygame.K_LEFT] and Stef.x > Stef.vel:
        Stef.x-= Stef.vel
        Stef.left = True
        Stef.right = False
        Stef.standing = False

    elif keys [pygame.K_RIGHT] and Stef.x < screenwidth - Stef.width - Stef.vel:
        Stef.x+= Stef.vel
        Stef.left = False
        Stef.right = True
        Stef.standing = False

    else:
        Stef.standing = True
        Stef.walkCount = 0

    if not(Stef.isJump):    
        if keys[pygame.K_UP]:
            Stef.isJump = True
        

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

