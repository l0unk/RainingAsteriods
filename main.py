import random
import pygame
import pyautogui

timers = []
meteorites = []
hearts = []
powerups = []
pygame.font.init()
mainfont = pygame.font.Font("/usr/share/fonts/adobe-source-code-pro/SourceCodePro-Regular.otf", 25)
smallfont = pygame.font.Font("/usr/share/fonts/adobe-source-code-pro/SourceCodePro-Regular.otf", 22)

class Timer(object):
    def __init__(self, time):
        self.time = 0
        self.goal = time

    def update(self):
        if not self.time >= self.goal:
            self.time += 1

    def reset(self):
        self.time = 0

    def get(self):
        return self.time >= self.goal

class Meteorite(object):
    def __init__(self, x, y, size, vel):
        self.x = x
        self.y = y
        self.size = size
        self.vel = vel

    def draw(self, window):
        pygame.draw.circle(window, (255, 255, 255), (self.x, self.y), self.size)
    
    def move(self):
        if self.y < (GROUND + random.randint(50, 80)):
            self.y += self.vel
            return True
        else:
            return False 

class Heart(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image_file = pygame.image.load('assets/heart.png')
        self.width = 20
        self.height = 29
        self.image = pygame.transform.scale(self.image_file, (self.width, self.height))
        self.vel = 0
        self.bounce = 25
        self.gravity = 1 
        self.falling = False
    
    def move(self):
        if self.falling:
            if self.vel > self.bounce * 0.1:
                self.vel *= 0.9
            else:
                self.vel = 0
        else:
            self.vel = self.bounce
        self.y -= self.vel
        #gravity
        if self.y < GROUND:
            self.falling = True
            self.y += 9
        else:
            self.falling = False
    
    def draw(self, window):
        window.blit(self.image, (self.x, self.y))

class Powerup(object):
    def __init__(self, x, y):
        self.width = 300
        self.height = 0
        self.x = x + (player.width / 2) - (self.width / 2)
        self.maxheight = y
        self.y = y
    
    def move(self):
        rect = pygame.rect.Rect(self.x, self.y, self.width, self.height)
        #remove meteorites
        if self.height >= self.maxheight:
            powerups.remove(self)
        self.height = self.maxheight - self.y
        self.y -= 10
        for meteorite in meteorites:
            meteoriterect = pygame.rect.Rect(meteorite.x, meteorite.y, meteorite.size, meteorite.size)
            if rect.colliderect(meteoriterect):
                meteorites.remove(meteorite)
        

    def draw(self, window):
        rect = pygame.rect.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(window, (255, 255, 255, 0), rect)
class Player(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 70
        self.speed = 7
        self.jumpspeed = 35
        self.image_file = pygame.image.load('assets/player.png')
        self.image = pygame.transform.scale(self.image_file, (self.width, self.height))
        self.falling = False
        self.jumpvel = 0
        self.gravity = 9 
        self.lives = 5
        self.points = 0
        self.powerup = 0

    def draw(self, window):
        window.blit(self.image, (self.x, self.y))

    def hit(self):
        self.lives -= 1

    def move(self):
        #update points every second
        if pointstimer.get():
            self.points += 1
            pointstimer.reset()
        #update powerup every 0.5 seconds
        if poweruptimer.get():
            if not self.powerup >= 100:
                self.powerup += 2
            if self.powerup > 100:
                self.powerup = 100
            poweruptimer.reset()
        #check for collisions with the asteriods
        playerrect = pygame.rect.Rect(self.x, self.y, self.width, self.height)
        for meteorite in meteorites:
            meteoriterect = pygame.rect.Rect(meteorite.x, meteorite.y, meteorite.size, meteorite.size)
            if playerrect.colliderect(meteoriterect):
                self.hit()
                meteorites.remove(meteorite)
        #check for collisions with hearts
        for heart in hearts:
            heartrect = pygame.rect.Rect(heart.x, heart.y, heart.width, heart.height)
            if playerrect.colliderect(heartrect):
                self.lives += 1
                hearts.remove(heart)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and not self.falling:
            self.jumpvel = self.jumpspeed

        if self.falling:
            if self.jumpvel > self.jumpspeed * 0.1:
                self.jumpvel *= 0.9
            else:
                self.jumpvel = 0
        self.y -= self.jumpvel


        #moving right 
        if keys[pygame.K_d]:
            self.x += self.speed
        #moving left
        if keys[pygame.K_a]:
            self.x -= self.speed
        #powerup
        if keys[pygame.K_RETURN] and self.powerup >= 100:
            powerups.append(Powerup(self.x, self.y))
            self.powerup = 0

        #gravity
        if self.y < GROUND:
            self.falling = True
            self.y += self.gravity
        else:
            self.falling = False


#initiate pygame window of 1280x720
pygame.init()
WIDTH = 1280
HEIGHT = 720
GROUND = 550
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Louk's game")
run = True
player = Player(200, 200)
meteoritetimer = Timer(random.randint(20, 30))
pointstimer = Timer(60)
hearttimer = Timer(random.randint(600, 1800))
poweruptimer = Timer(15)
timers.append(meteoritetimer)
timers.append(pointstimer)
timers.append(hearttimer)
timers.append(poweruptimer)
gameover = False
gamestart = False



def redraw_window():
    #draw a dark grey background
    window.fill((20, 20, 20))
    #draw the player
    player.draw(window)
    for meteorite in meteorites:
        meteorite.draw(window)
    
    for heart in hearts:
        heart.draw(window)
    
    for powerup in powerups:
        powerup.draw(window)
    #draw points
    pointslabel = mainfont.render(f"{player.points}", 1, (255, 255, 255))
    window.blit(pointslabel, ((WIDTH / 2) - (pointslabel.get_width() / 2), 100))

    #draw lives top left
    healthlabel = mainfont.render(f"❤ {player.lives}", 1, (255, 255, 255))
    window.blit(healthlabel, (50, 70))

    #powerup percentage
    powerlabel = smallfont.render(f'{player.powerup}%', 1, (255, 255, 255))
    powerimage = pygame.image.load("assets/power.png")
    power = pygame.transform.scale(powerimage, (20, 20))
    window.blit(power, (WIDTH -195, 70))
    window.blit(powerlabel, (WIDTH - 65, 65))
    poweruprect = pygame.rect.Rect(WIDTH - 170, 70, player.powerup, 20)
    pygame.draw.rect(window, (255, 255, 255), poweruprect)

    #ground
    ground = pygame.rect.Rect(0, GROUND + player.height, WIDTH, GROUND)
    pygame.draw.rect(window, (30, 30, 30), ground)

def spawn_meteorite():
    if meteoritetimer.get():
        meteorite = Meteorite(random.randint(0, WIDTH), 0, random.randint(9, 25), random.randint(3, 6))
        meteorites.append(meteorite)
        timers.remove(meteoritetimer);
        diff = player.points / 6
        if diff > 30:
            diff = 30
        newtimer = Timer(random.randint(20, 30) - diff)
        timers.append(newtimer)
        return newtimer
    else:
        return meteoritetimer

def spawn_heart():
    if hearttimer.get():
        heart = Heart(random.randint(0, WIDTH), 0)
        hearts.append(heart)
        timers.remove(hearttimer)
        newtimer = Timer(random.randint(600, 1800))
        timers.append(newtimer)
        return newtimer
    else:
        return hearttimer

while run:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if not gamestart:
                gamestart = True
                for timer in timers:
                    timer.reset();
                player.points = 0
                player.powerup = 0
    if not gamestart:
        clock = pygame.time.Clock()
        clock.tick(60)
        
        label = mainfont.render(f"Neppe tetris", 1, (255, 255, 255))
        label1 = smallfont.render(f"Druk op een toets om te beginnen", 1, (255, 255, 255))
        label2 = smallfont.render(f"'A' en 'D' om te bewegen, Spatie om te springen en Enter voor een powerup", 1, (255, 255, 255))

        window.blit(label,((WIDTH / 2) - (label.get_width() / 2), (HEIGHT / 2) - (label.get_height() / 2) -30))
        window.blit(label1,((WIDTH / 2) - (label1.get_width() / 2), (HEIGHT / 2) - (label1.get_height() / 2)))
        window.blit(label2,((WIDTH / 2) - (label2.get_width() / 2), (HEIGHT / 2) - (label2.get_height() / 2) + 30))


    elif not player.lives <= 0:
        #set the game to 60fps
        clock = pygame.time.Clock()
        clock.tick(60)

        meteoritetimer = spawn_meteorite()
        hearttimer = spawn_heart()
        #update timers
        for timer in timers:
            timer.update()

        for meteorite in meteorites:
            if not meteorite.move():
                meteorites.remove(meteorite)

        for heart in hearts:
            heart.move()
        
        for powerup in powerups:
            powerup.move()
        player.move()
        redraw_window()
    else:
        gameoverlabel = mainfont.render(f"Game over, you had {player.points} points.", 1, (255,255,255))
        window.blit(gameoverlabel,((WIDTH / 2) - (gameoverlabel.get_width() / 2), (HEIGHT / 2) - (gameoverlabel.get_height() / 2)))


    pygame.display.update()

pygame.quit()