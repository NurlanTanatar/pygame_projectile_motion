try:
    import pygame
    import math
except:
    import install_requirements  # install packages

    import pygame
    import math

width = 640
height = 480

gravity = 4.9
#setting up screen set-s
win = pygame.display.set_mode((width, height))

#the "characteristics" of ball, where it will be placed, radius and color of that ball
class projectile:
    def __init__(self, x, y, radius, color):
        super().__init__()
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
    #adding like a "shell" of the ball, that is black
    def draw(self, win):
        pygame.draw.circle(win, (0,0,0), (self.x, self.y), self.radius)
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius - 1)
    #applying projectile motion equation to find range and height of the ball
    #the word power here means just a velocity
    @staticmethod
    def trajectory(startx, starty, power, angle, time):
        velx = math.cos(angle) * power
        vely = math.sin(angle) * power

        distX = velx * time
        distY = (vely * time) + ((-1) * gravity * (time ** 2)/2)

        newx = round(startx + distX)
        newy = round(starty - distY)

        return (newx, newy)
#adding background and line that goes from pos-n of ball to pos-n of cursor
def redraw():
    win.fill((64,64,64))
    pygame.draw.line(win, (255,255,255), line[0], line[1])
    bullet.draw(win)
    pygame.display.update()
#applying trigonometry to find at which quarter the cursor placed to find relativly to pos-ns of ball
def findAngle(sX, sY):
    try:
        angle = math.atan((sY - posCursor[1]) / (sX - posCursor[0]))
    except:
        angle = math.pi / 2
    if posCursor[1] < sY and posCursor[0] > sX:
        angle = abs(angle)
    elif posCursor[1] < sY and posCursor[0] < sX:
        angle = math.pi - angle
    elif posCursor[1] > sY and posCursor[0] < sX:
        angle = math.pi + abs(angle)
    elif posCursor[1] > sY and posCursor[0] > sX:
        angle = (math.pi * 2) - angle
    return angle
#creating testing ball
bullet = projectile(int(width / 3), height - 5, 4, (255,255,255))

x = 0
y = 0
time = 0
power = 0
angle = 0
shoot = False
#running while to draw all of it
running = True
while running:
    #finding boundaries of screen to make that ball doesn't fall off from it
    if shoot:
        if bullet.y < height - bullet.radius:
            time += 0.025
            posBall = projectile.trajectory(x, y, power, angle, time)
            bullet.x = posBall[0]
            bullet.y = posBall[1]
        else:
            shoot = False
            bullet.y = height - bullet.radius - 1
    #position of cursor
    posCursor = pygame.mouse.get_pos()
    #line that goes off from ball's pos-n and cursor's pos-n
    line = [(bullet.x, bullet.y), posCursor]

    redraw()
    #events for tracking when mouse is clicked and when close button is pressed
    for event in pygame.event.get():

        if event.type == pygame.MOUSEBUTTONDOWN:
            if shoot == False:
                shoot = True
                x = bullet.x
                y = bullet.y
                time = 0
                power = math.sqrt( (line[1][1] - line[0][1])**2 + (line[1][0] - line[1][0])**2) / 8
                angle = findAngle(bullet.x, bullet.y)
        
        if event.type == pygame.QUIT:
            running = False
pygame.quit()