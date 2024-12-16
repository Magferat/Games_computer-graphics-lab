import random

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

diamond_x = random.choice((range(-170,170)))
diamond_y = 330
d_speed = 1
c_direction = 1
c_speed = 0.8
rgb = (random.uniform(0.6, 1.1) ** 3, random.uniform(0.6, 1.1) ** 3, random.uniform(0.7, 1) ** 3)
catcher_color = (1,1,1)
catcher_x = random.choice((range(-190,110)))
catcher_y = -340
score = 0
move = True
gameOver = False

def draw_points(x, y,rgb):
    glColor3f(*rgb)
    glPointSize(3)
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


def buildDiamond(x, y):
    global rgb, diamond_x, diamond_y, score, move, d_speed ,catcher_x, catcher_y, gameOver
    drawParts(x, y, x - 6, y - 8, rgb)
    drawParts(x, y, x + 6, y - 8, rgb)
    drawParts(x, y - 16, x - 6, y - 8, rgb)
    drawParts(x, y - 16, x + 6, y - 8, rgb)
    if move:
        diamond_y -= d_speed
        if diamond_y - 16 <= catcher_y:
                if catcher_x + 1 <= diamond_x <= catcher_x + 80:
                    score = score + 1
                    d_speed = d_speed + 0.05
                    print('score:', score)
                    diamond_y = 330
                    diamond_x = random.choice((range(-170, 170)))
                    rgb = (random.uniform(0.6, 1.1) ** 3, random.uniform(0.6, 1.1) ** 3, random.uniform(0.7, 1) ** 3)
                else:
                    print('Game Over! Score :', score)
                    move = False
                    gameOver = True
    else:
        diamond_y = diamond_y


def buildCatcher():
    global catcher_x, catcher_y, c_direction, c_speed, move,catcher_color, gameOver
    drawParts(catcher_x, catcher_y, catcher_x+80, catcher_y, catcher_color)
    drawParts(catcher_x + 79, catcher_y, catcher_x+70, catcher_y - 8,catcher_color)
    drawParts(catcher_x + 69, catcher_y - 8, catcher_x + 10, catcher_y - 8, catcher_color)
    drawParts(catcher_x + 9, catcher_y - 8, catcher_x+1, catcher_y,catcher_color)
    # if move:
    #     # catcher_x += 10 * c_direction
    #     if catcher_x <= -190 or catcher_x >= 110:
    #         c_direction = -c_direction

    if move is False:
        catcher_x = catcher_x
        if gameOver:
            catcher_color = (1, 0, 0)



def gameReset():
    global diamond_x, diamond_y, d_speed, catcher_x,catcher_y,c_speed, c_direction,rgb, move,score, catcher_color,gameOver
    diamond_x = random.choice((range(-170, 170)))
    diamond_y = 330
    d_speed = 1
    c_direction = 1
    c_speed = 0.8
    rgb = (random.uniform(0.6, 1.1) ** 3, random.uniform(0.6, 1.1) ** 3, random.uniform(0.7, 1) ** 3)
    catcher_color = (1, 1, 1)
    catcher_x = random.choice((range(-190, 110)))
    catcher_y = -340
    score = 0
    move = True
    gameOver = False


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


def KeyboardListener(key, x,y):

    global c_direction, catcher_x

    if key == GLUT_KEY_RIGHT :
        if catcher_x + 25 <= 115:
            c_direction = 1
            catcher_x += 25

    elif key == GLUT_KEY_LEFT:
        if catcher_x - 25 >= -205:
            c_direction = -1
            catcher_x -= 25


def animate():
    glutPostRedisplay()


def showScreen():
    global diamond_y, diamond_x, move, gameOver
    glClearColor(0,0,0,1)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()
    leftArrow()
    crossButton()
    buildCatcher()
    if move:
            pauseButton()
            buildDiamond(diamond_x, diamond_y)
    if move is False:
        if gameOver is False:
            buildDiamond(diamond_x, diamond_y)
        playButton()
    glutSwapBuffers()



glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(400, 700)
glutInitWindowPosition(500, 50)
wind = glutCreateWindow(b"Catch the Diamonds!")
glutDisplayFunc(showScreen)
glutIdleFunc(animate)
glutSpecialFunc(KeyboardListener)
glutMouseFunc(mouse)
glutMainLoop()