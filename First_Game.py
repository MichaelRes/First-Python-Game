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
clock = pygame.time.Clock()

score = 0

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
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)

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
        
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)
        #pygame.draw.rect (win, (255,0,0), self.hitbox,2)


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


class enemy(object):
    walkRight = [pygame.image.load('Data/R%sE.png' % frame) for frame in range(1, 12)] 
    walkLeft = [pygame.image.load('Data/L%sE.png' % frame) for frame in range(1, 12)]

    def __init__(self, x, y, width, height, end):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.end=end
        self.path = [self.x, self.end]
        self.walkCount=0
        self.vel = 3
        self.hitbox = (self.x + 17, self.y + 2, 31, 57)
        self.health = 10
        self.visible = True
    
    def draw(self, win):
        self.move()
        if self.visible:
            if self.walkCount + 1 >= 33:
                self.walkCount = 0
            
            if self.vel > 0:
                win.blit(self.walkRight[self.walkCount //3], (self.x, self.y))
                self.walkCount +=1
            else:
                win.blit(self.walkLeft[self.walkCount //3], (self.x, self.y))
                self.walkCount +=1
            
            pygame.draw.rect (win, (255,0,0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))
            pygame.draw.rect (win, (0,128,0), (self.hitbox[0], self.hitbox[1] - 20, 50 - (5 * (10 - self.health)), 10))
            self.hitbox = (self.x + 17, self.y + 2, 31, 57)
            #pygame.draw.rect(win, (255,0,0), self.hitbox, 2)


    def move(self):
        if self.vel>0:
            if self.x + self.vel < self.path[1]:
                self.x += self.vel

            else:
                self.vel = self.vel * -1
                self.walkcount = 0
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel 
            else:
                self.vel = self.vel * -1
                self.walkcount = 0

    def hit(self):
        if self.health >1:
            self.health -=1
        else:
            self.visible = False
        print("hit")

def redrawGameWindow():
    win.blit(bg, (0,0))
    text = font.render('Score: ' + str(score), 1, (0,0,0))
    win.blit(text, (390,10))
    Stef.draw(win)
    goblin.draw(win)

    for bullet in bullets:
        bullet.draw(win)

    pygame.display.update()

#mainloop

font = pygame.font.SysFont('comicsans', 30, True)
Stef = player (300, 410, 64, 64) 
goblin = enemy (100, 410, 64, 64, 450)
shootLoop = 0
bullets = []
run = True
while run:
    clock.tick(27)

    if shootLoop > 0:
        shootLoop +=1
    if shootLoop >3:
        shootLoop=0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    for bullet in bullets:
        if bullet.y - bullet.radius < goblin.hitbox[1] + goblin.hitbox[3] and bullet.y + bullet.radius > goblin.hitbox[1]:
            if bullet.x + bullet.radius > goblin.hitbox[0] and bullet.x - bullet.radius < goblin.hitbox[0] + goblin.hitbox[2]:
                goblin.hit()
                score +=1
                bullets.pop(bullets.index(bullet))

        if bullet.x < 500 and bullet.x >0:
            bullet.x +=bullet.vel
        else:
            bullets.pop(bullets.index(bullet))


    
    keys = pygame.key.get_pressed() #return a list of booleans for the entire keyboard

    if keys[pygame.K_SPACE] and shootLoop ==0:
        if Stef.left:
            facing = -1
        else:
            facing = 1
        if len(bullets)<5:
            bullets.append(projectile(round(Stef.x + Stef.width//2), round(Stef.y + Stef.height//2), 6, (0,0,0), facing))
        shootLoop = 1

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

