import random

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *


move = True
game_over = False
shoot = False
shooter_x = random.choice((range(-170,170)))
shooter_y = -330
alien_speed = 0.1
fire_speed = 0.8
ball_y = -300
alien_box = []
alien_y = 330
alien_r = 12
alien_x =random.choice((range(-150,150)))
last_y = 330
score = 0
missed = 0
misfire = 0



def draw_circle(cx, cy, radius):
    glBegin(GL_POINTS)
    glColor3f(1.0, 0.75, 0.0)
    x = radius
    y = 0
    p = 1 - radius

    while x >= y:
        glVertex2f(x + cx, y + cy)
        glVertex2f(-x + cx, y + cy)
        glVertex2f(x + cx, -y + cy)
        glVertex2f(-x + cx, -y + cy)
        glVertex2f(y + cx, x + cy)
        glVertex2f(-y + cx, x + cy)
        glVertex2f(y + cx, -x + cy)
        glVertex2f(-y + cx, -x + cy)

        y += 1

        if p <= 0: #i
            p = p + 2 * y + 1
        else:   #o
            x -= 1
            p = p + 2 * y - 2 * x + 1

    glEnd()
class Alien_Position:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.r = random.choice((range(14,18)))


def create_alien(x,y):
        a = Alien_Position(x, y)
        alien_box.append(a)

create_alien(100, 330)


def attack():
    global speed, last_y, alien_box, shoot, ball_y, score, game_over, move
    if move:
        for a in alien_box:
            draw_circle(a.x, a.y, a.r)
            a.y -= alien_speed
            if alien_box[-1].y <= 250:
                alien_x = random.choice(range(-150, 150))
                alien_y = random.choice(range(400, 450))
                create_alien(alien_x, alien_y)

            if shoot:
                distance = (a.x - shooter_x) ** 2 + (a.y - ball_y) ** 2
                if distance <= (a.r + 5) ** 2:
                    score += 1
                    alien_box.remove(a)
                    shoot = False
                    ball_y = -300
                    print("Score", score)

            if ((a.y - shooter_y) ** 2 + (a.x - shooter_x) ** 2) <= (a.r + 10) ** 2:
                game_over = True
                move = False
                print("Game Over! Collision with shooter")
                print("Score", score)
        missed = [a.y for a in alien_box if a.y < -330]
        if len(missed) >= 3:
            game_over = True
            move = False
            print("Game Over! Missed 3 Alien.")
            print("Score:", score)
    else:
        if game_over is False:
            for a in alien_box:
                draw_circle(a.x, a.y, a.r)





def gameReset():
    global move, shoot ,shooter_x ,alien_x,fire_speed, alien_speed, shooter_y ,speed, alien_y, last_y, alien_box, shoot, ball_y, score, game_over, missed

    move = True
    game_over = False
    shoot = False
    shooter_x = random.choice((range(-170, 170)))
    shooter_y = -330
    alien_speed = 0.1
    fire_speed = 0.8
    ball_y = -300
    alien_box = []
    alien_y = 330
    alien_x = random.choice((range(-150, 150)))
    last_y = 330
    score = 0
    create_alien(100, 330)
    missed = 0


def shooter():
    global shooter_y, shooter_x
    draw_circle(shooter_x, shooter_y,10)

def fire_ball(x,y):

    global fire_speed,ball_y, shoot, missed, game_over, move
    draw_circle(x, y, 5)
    if ball_y < 330:
         ball_y += fire_speed
    else:
        shoot = False
        ball_y = -300
    if shoot and ball_y >= 330:
        missed += 1
        if missed >= 3:
            game_over = True
            move = False
            print("Game Over! Missfired 3 Times.")
            print("Score", score)

def KeyboardListener(key, x,y):

    global shooter_y, shooter_x, shoot, game_over, move
    if game_over is False and move is True:
        if key == b'a':
            if shooter_x + 20 <= 190:
                shooter_x += 25

        elif key == b'd':
            if shooter_x - 20 >= -190:
                shooter_x -= 25

        elif key == b' ':
            shoot = True


def draw_points(x, y,rgb):
    glColor3f(*rgb)
    glPointSize(2)
    glBegin(GL_POINTS)
    glVertex2f(x,y)
    glEnd()


def findZone(x1, y1, x2,y2):
    dx = x2-x1
    dy = y2 - y1
    zone = 1000000
    if abs(dx)>= abs(dy):
        if dx >= 0 and dy>= 0:
            zone = 0
        if dx <= 0 and dy >= 0:
            zone = 3
        if dx <= 0 and dy<= 0:
            zone = 4
        if dx >= 0 and dy<= 0:
            zone = 7
    else:
        if dx >= 0 and dy>= 0:
            zone = 1
        if dx <= 0 and dy >= 0:
            zone = 2
        if dx <= 0 and dy<= 0:
            zone = 5
        if dx >= 0 and dy<= 0:
            zone = 6
    return zone


def convert_to_0(zone, x1, y1, x2, y2):
    if zone == 0:
        return x1, y1, x2, y2
    elif zone == 1:
        return y1, x1, y2, x2
    elif zone == 2:
        return y1, -x1, y2, -x2
    elif zone == 3:
        return -x1, y1, -x2, y2
    elif zone == 4:
        return -x1, -y1, -x2, -y2
    elif zone == 5:
        return -y1, -x1, -y2, -x2
    elif zone == 6:
        return -y1, x1, -y2, x2
    elif zone == 7:
        return x1, -y1, x2, -y2


def convert_to_original(original, x1, y1):
    if original == 0:
        return x1, y1
    elif original == 1:
        return y1, x1
    elif original == 2:
        return -y1, x1
    elif original == 3:
        return -x1, y1
    elif original == 4:
        return -x1, -y1
    elif original == 5:
        return -y1, -x1
    elif original == 6:
        return y1, -x1
    elif original == 7:
        return x1, -y1


def run_MPL(original, x1, y1, x2, y2, color):

    dx = x2 - x1
    dy = y2 - y1
    d = 2 * (dy - dx)
    delE = 2 * dy
    delNE = 2 * dx - dy
    x, y = x1, y1

    while x < x2:
        original_x, original_y = convert_to_original(original, x, y)
        draw_points(original_x, original_y, color)
        if d < 0:
            x += 1
            d += delE
        else:
            x += 1
            y += 1
            d += delNE


def drawParts(start_x,start_y, end_x, end_y,color):
    original_zone = findZone(start_x,start_y, end_x, end_y)
    x1,y1,x2,y2 = convert_to_0( original_zone,start_x,start_y, end_x, end_y)
    run_MPL(original_zone,x1,y1,x2,y2,color)


def crossButton():
    # global rgb
    rgb = (1,0,0)
    drawParts(150, 345, 180, 330,rgb )
    drawParts(180,345,150,330,rgb)


def leftArrow():
    rgb = (0.0, 1.0, 1.0)
    drawParts(-180,325, -140,325,rgb)
    drawParts(-180,326, -160,340,rgb)
    drawParts(-180,324, -160, 310,rgb)


def playButton():
    rgb = (1.0, 0.75, 0.0)
    drawParts(-5,340,-5,310,rgb)
    drawParts(-5,340,10,325,rgb)
    drawParts(10,325, -5,310,rgb)


def pauseButton():
    rgb = (1.0, 0.75, 0.0)
    drawParts(-5, 340, -5, 310,rgb)
    drawParts(5, 340, 5, 310,rgb)


def iterate():
    glViewport(0, 0, 400, 700)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-200, 200, -350, 350, 0.0, 1.0)
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()


def mouse(button, state, x,y):
    global move, score
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        a = x - 200
        b = 350 - y
        if -181 < a < -139 and 308 <= b <= 342:
                print('Starting Over!')
                gameReset()
        elif -6 <= a <= 11 and 309 <= b <= 342:
            if move :
                move = False
                print('Paused!')
            else:
                print('Play!')
                move = True
        elif 140 <= a <= 190 and 320 <= b <= 350 :
                print('Goodbye! Total Score : ', score)
                glutLeaveMainLoop()





def animate():
    glutPostRedisplay()


def showScreen():
    global shooter_y, shooter_x, shoot, game_over
    glClearColor(0,0,0,1)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()
    if move:
        pauseButton()
    if move is False:
        if game_over is False:
            playButton()

        else:
            pauseButton()

    if shoot:
        fire_ball(shooter_x, ball_y)
    shooter()
    attack()
    crossButton()
    leftArrow()
    glutSwapBuffers()



glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(400, 700)
glutInitWindowPosition(500, 50)
wind = glutCreateWindow(b"Shoot The Aliens!!")
glutDisplayFunc(showScreen)
glutIdleFunc(animate)
glutMouseFunc(mouse)
glutKeyboardFunc(KeyboardListener)

glutMainLoop()
