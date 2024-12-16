import random

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# ===============Global Variables ==================
# tiles
t_speed = 2
h1 = -50
h2 = -100
h3 = -150
h4 = -200
count = 0
tiles_box = []
t_rgb = (0.45, 0.80, 0.45)

# timer
time = 0

# shooter
shooter_x = 625
shooter_y = h1 + 12
shooter_r = 8
fall = True
sfall_y = 0
jump_count = 0
press = False
xmove_s = 0
j_dir = 1

# bullet
bullets = []

# diamond
diamond_x = random.choice((range(0, 550)))
diamond_y = 355
d_speed = 0.7

# game variables
score = 0
move = True
gameOver = False

# enemy
enemy_x = random.choice((range(-2000, -1500)))
enemy_y = 200
enemy_speed = 1
enemy_hit = 0
e_rgb = (0.90, 0.50, 0.25)
enemy_miss = 0

class Tiles_Position:
    def __init__(self, x, y):
        self.start = x
        self.h = y


# ==============================================
# ================ Algorithms =================
# ==============================================
def draw_points(x, y, rgb):
    glColor3f(*rgb)
    glPointSize(3)
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()


def drawLine(start_x, start_y, end_x, end_y, color):
    original_zone = findZone(start_x, start_y, end_x, end_y)
    x1, y1, x2, y2 = convert_to_0(original_zone, start_x, start_y, end_x, end_y)
    run_MPL(original_zone, x1, y1, x2, y2, color)


def findZone(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    zone = 1000000
    if abs(dx) >= abs(dy):
        if dx >= 0 and dy >= 0:
            zone = 0
        if dx <= 0 and dy >= 0:
            zone = 3
        if dx <= 0 and dy <= 0:
            zone = 4
        if dx >= 0 and dy <= 0:
            zone = 7
    else:
        if dx >= 0 and dy >= 0:
            zone = 1
        if dx <= 0 and dy >= 0:
            zone = 2
        if dx <= 0 and dy <= 0:
            zone = 5
        if dx >= 0 and dy <= 0:
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


def draw_circle(cx, cy, radius, color):
    glBegin(GL_POINTS)
    glColor3f(*color)
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

        if p <= 0:  # i
            p = p + 2 * y + 1
        else:  # o
            x -= 1
            p = p + 2 * y - 2 * x + 1

    glEnd()


# =================================================
# =============== Shapes  & Functions =======================
# ===============================================


def create_tile(x, h):
    global tiles_box
    a = Tiles_Position(x, h)
    tiles_box.append(a)


create_tile(600, h1)
create_tile(600, h3)


def tiles():
    global t_speed, move, tiles_box, count, h1, h2, h3, h4, shooter_x, shooter_y, gameOver
    if move:
        for tile in tiles_box:
            drawLine(tile.start, tile.h, tile.start + 50, tile.h, t_rgb)
            drawLine(tile.start, tile.h, tile.start + 25, tile.h - 5, t_rgb)
            drawLine(tile.start + 50, tile.h, tile.start + 25, tile.h - 5, t_rgb)

            tile.start -= t_speed
            if count % 2 == 0 and tiles_box[-1].start <= 450:
                create_tile(600, h2)
                random_x = random.randint(20, 50)
                create_tile(600 + random_x, h4)
                count += 1
            elif count % 2 != 0 and tiles_box[-1].start <= 450:
                random_x = random.randint(20, 50)
                create_tile(600 + random_x, h1)
                create_tile(600, h3)
                count += 1

            if tile.start + 50 < -600:
                tiles_box.remove(tile)
    else:
        for tile in tiles_box:
            drawLine(tile.start, tile.h, tile.start + 50, tile.h, t_rgb)
            drawLine(tile.start, tile.h, tile.start + 25, tile.h - 5, t_rgb)
            drawLine(tile.start + 50, tile.h, tile.start + 25, tile.h - 5, t_rgb)


def shooter():
    global shooter_r, sfall_y, t_speed, shooter_x, shooter_y, move
    if move:
        shooter_x = shooter_x - t_speed + xmove_s
        shooter_y += sfall_y
        draw_circle(shooter_x, shooter_y, shooter_r, (0.8, 0, 0.5))
    else:
        draw_circle(shooter_x, shooter_y, shooter_r, (0.8, 0, 0.5))


def bullet(x, y):
    global bullets
    bullets.append([x, y, 4])  # x, y, radius


def diamond(x, y):
    global diamond_x, diamond_y, score, move, d_speed, shooter_x, shooter_y, shooter_r, gameOver
    rgb = (1, 1, 0.8)
    drawLine(x, y, x - 12, y - 16, rgb)
    drawLine(x, y, x + 12, y - 16, rgb)
    drawLine(x, y - 32, x - 12, y - 16, rgb)
    drawLine(x, y - 32, x + 12, y - 16, rgb)

    if move:
        diamond_y -= d_speed
        if (diamond_x - 12 <= shooter_x <= diamond_x + 12) and (diamond_y - 32 <= shooter_y <= diamond_y):
            score += 1
            print('Score:', score)
            diamond_x = random.randint(-550, 550)
            diamond_y = 330
        if diamond_y <= -250 :
            diamond_x = random.randint(-550, 550)
            diamond_y = 330
    else:
        diamond_y = diamond_y



#
def enemy(x, y):
    global enemy_x, enemy_y, score, move, enemy_speed, gameOver, e_rgb
    drawLine(x, y, x - 70, y, e_rgb)
    drawLine(x, y, x - 30, y + 57, e_rgb)
    drawLine(x, y, x - 70, y + 5, e_rgb)
    drawLine(x - 55, y, x - 55, y + 57, e_rgb)
    drawLine(x - 70, y, x - 70, y + 57, e_rgb)
    if move and gameOver == False:
        enemy_x += enemy_speed
        if enemy_x > 700:
            enemy_x = random.choice((range(-2000, -1500)))


def jump():
    global shooter_x, shooter_y, fall, sfall_y, press, jump_count, xmove_s
    if abs(j_dir) == 1:
        if press and jump_count < 7:
            shooter_x += (11 * j_dir)
            shooter_y += 16
            jump_count += 1
        elif jump_count == 7:
            press = False
            jump_count = 0
            sfall_y -= 0.5
            xmove_s += (0.5 * j_dir)
    elif j_dir == 0:
        if press and jump_count < 26:
            shooter_y += 5
            jump_count += 1
            sfall_y = 0
        elif jump_count == 26:
            press = False
            jump_count = 0
            sfall_y -= 0.5

def collision_check():
    global tiles_box, shooter_x, shooter_r, shooter_y, sfall_y, xmove_s, time, gameOver, move, t_speed, enemy_x, enemy_y, e_rgb, enemy_hit, enemy_miss, score, bullets
    idx = -1
    if ((shooter_x - shooter_r) <= -600 or (shooter_y + shooter_r) >= 350) and not gameOver: # left wall, upper wall check
        print(f"Collision with Wall. Game Over! Final score: {score}")
        gameOver = True
        time = 0
        move = False
    if xmove_s != 0 and (shooter_x + shooter_r) >= 600 and not gameOver:
        print(f"Collision with Wall. Game Over! Final score: {score}")
        gameOver = True
        time = 0
        move = False
    if (shooter_y - shooter_r) <= -265 and not gameOver:
        print(f"Fell into Lava. Game Over! Final score: {score}")
        gameOver = True
        time = 0
        move = False
    for t in tiles_box:
        idx += 1
        tile_left = t.start + 5
        tile_right = t.start + 45
        tile_bottom = t.h
        tile_top = t.h + 15

        if (tile_left <= shooter_x <= tile_right and tile_bottom <= shooter_y <= tile_top):
            if time < 600:
                shooter_y = t.h + 12
                sfall_y = 0
                xmove_s = 0
                break
            else:
                tiles_box.remove(t)
                sfall_y -= 0.5
            time = 0

    else:       # to fall off tiles
        sfall_y -= 0.01


    vanish_b = []
    # bullet hitting enemy condition
    for j in range(len(bullets)):
        x_b, y_b, r_b = bullets[j]
        if (enemy_x - 70) <= x_b + r_b <= enemy_x or (enemy_x - 70) <= x_b - r_b <= enemy_x:
            if enemy_y <= y_b + r_b:
                e_rgb = (0.99, 0.10, 0.05)
                enemy_hit += 1
                print(f"Shot enemy {enemy_hit}/2 time(s)!")
                vanish_b.append(j)
                if enemy_hit > 1:
                    enemy_hit = 0
                    e_rgb = (0.90, 0.50, 0.25)
                    enemy_x = random.choice((range(-2000, -1500)))
                    print("Enemy is dead!")
                    score += 3
                    print('Score:', score)
    for i in vanish_b:
        bullets.pop(i)
    # enemy miss
    if 680 > enemy_x - 70 > 600 and not gameOver:
        enemy_miss += 1
        enemy_x = random.choice((range(-2000, -1500)))
        enemy_hit = 0
        e_rgb = (0.90, 0.50, 0.25)
        print(f"Enemy missed {enemy_miss}/2 times")
        if enemy_miss == 2 and not gameOver:
            print(f"Game Over! Final score: {score}")
            gameOver = True
            time = 0
            move = False
    # clash w enemy
    if (enemy_x - 70) < shooter_x < (enemy_x + 70) and (enemy_y + 60) > shooter_y > enemy_y and not gameOver:
        print(f"Clash with enemy! Game Over! Final score: {score}")
        gameOver = True
        time = 0
        move = False



def gameReset():
    global tiles_box, h1, h2, h3, h4, tiles_box, t_rgb, j_dir, bullets, enemy_x, enemy_y, enemy_speed, enemy_hit, enemy_miss, e_rgb, t_speed, count, shooter_y, shooter_r, shooter_x, fall, sfall_y, jump_count, press, xmove_s, diamond_y, diamond_x, d_speed, score, move, gameOver, time
    # tiles
    count = 0
    tiles_box = []
    t_rgb = (0.45, 0.80, 0.45)
    create_tile(600, h1)
    create_tile(600, h3)

    # timer
    time = 0
    # shooter
    shooter_x = 625
    shooter_y = h1 + 12
    shooter_r = 8
    fall = True
    sfall_y = 0
    jump_count = 0
    press = False
    xmove_s = 0
    j_dir = 1
    bullets = []

    # diamond
    diamond_x = random.choice((range(0, 550)))
    diamond_y = 355
    score = 0
    move = True
    gameOver = False

    # enemy
    enemy_x = random.choice((range(-2000, -1500)))
    enemy_y = 200
    enemy_hit = 0
    e_rgb = (0.90, 0.50, 0.25)
    enemy_miss = 0


def lava():
    rgb = (1.0, 0.45, 0.0)
    rgb_new = (1.0, 0.25, 0.10)
    r = random.random()
    g = random.random()
    if 0.4 < r:
        rgb_new = (r, 0.15, 0.05)
    if 0.2 < g < 0.4:
        rgb = (r, g, 0.0)

    drawLine(-600, -270, -400, -270, rgb)
    drawLine(-400, -265, -200, -265, rgb_new)
    drawLine(-200, -270, 0, -270, rgb)
    drawLine(0, -265, 200, -265, rgb_new)
    drawLine(200, -270, 400, -270, rgb)
    drawLine(400, -265, 600, -265, rgb_new)


# =========================================================
# ===================Buttons================================
# =========================================================

def crossButton():
    global rgb
    rgb = (1, 0, 0)
    drawLine(530, 340, 580, 300, rgb)
    drawLine(580, 340, 530, 300, rgb)


def leftArrow():
    global rgb
    rgb = (0.0, 1.0, 1.0)
    drawLine(-510, 310, -570, 310, rgb)
    drawLine(-570, 310, -550, 340, rgb)
    drawLine(-570, 310, -550, 280, rgb)

def playButton():
    rgb = (1.0, 0.75, 0.0)
    drawLine(-5, 340, -5, 290, rgb)
    drawLine(-5, 340, 20, 315, rgb)
    drawLine(19, 315, -5, 290, rgb)


def pauseButton():
    global rgb
    rgb = (1.0, 0.75, 0.0)
    drawLine(-5, 340, -5, 290, rgb)
    drawLine(10, 340, 10, 290, rgb)


# =======================================================


def mouse(button, state, x, y):
    global move, score

    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        if -565 <= x - 600 <= -505 and 280 <= 350 - y <= 340:
            print('Starting Over!')
            gameReset()
        elif -5 <= x - 600 <= 20 and 290 <= 350 - y <= 340:
            if move and not gameOver:
                move = False
                print('Paused!')
            elif not move:
                if not gameOver:
                    print('Play!')
                    move = True
        elif 530 <= x - 600 <= 580 and 300 <= 350 - y <= 340:
            print('Goodbye! Total Score:', score)
            glutLeaveMainLoop()


def keyboardListener(key, x, y):
    global shooter_x, shooter_y, sfall_y, shooter_r, time, bullets, press, j_dir, jump_count
    time = 0
    if move and not gameOver:
        if sfall_y == 0:
            if key == b'a':
                shooter_x -= 2
            elif key == b'd':
                shooter_x += 2
        else:
            if key == b'a':
                shooter_x -= 3
            elif key == b'd':
                shooter_x += 3
        if key == b' ':
            bullet(shooter_x - 4, shooter_y + 9)
            jump_count = 0
        if key == b'c':
            press = True
            j_dir = 0
            jump_count = 0


def specialKey(key, x, y):
    global shooter_x, shooter_y, shooter_r, press, j_dir, time, jump_count
    time = 0
    jump_count = 0
    if key == GLUT_KEY_UP:
        press = True
        j_dir = 1
    elif key == GLUT_KEY_DOWN:
        press = True
        j_dir = -1


def iterate():
    glViewport(0, 0, 1200, 700)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-600, 600, -350, 350, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def animate():
    global time, move, sfall_y, press, bullets
    if move and not press and sfall_y == 0:
        time += 1
    if move:
        if len(bullets) > 0: # handling bullets
            i = 0
            while i < len(bullets):
                x, y, r = bullets[i]
                draw_circle(x, y, r, (0.7, 0.8, 0.9))
                bullets[i][1] += 4
                if bullets[i][1] > 400:
                    bullets.pop(i)
                    i -= 1
                i += 1

    glutPostRedisplay()


def showScreen():
    global diamond_x, diamond_y, move, gameOver, enemy_x, enemy_y, shooter_x, shooter_y
    glClearColor(0, 0, 0, 1)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()
    crossButton()
    leftArrow()

    if move:
        if not gameOver:
            tiles()
            shooter()
            pauseButton()
            enemy(enemy_x, enemy_y)
            diamond(diamond_x, diamond_y)
    if move is False:
        if gameOver is False:
            tiles()
            shooter()
            enemy(enemy_x, enemy_y)
            diamond(diamond_x, diamond_y)
        else:
            tiles()

        playButton()


    collision_check()
    jump()
    lava()
    animate()
    glutSwapBuffers()


glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(1200, 700)
glutInitWindowPosition(0, 0)
wind = glutCreateWindow(b"THE FLOOR IS LAVA!")
glutDisplayFunc(showScreen)
glutIdleFunc(animate)
glutMouseFunc(mouse)
glutKeyboardFunc(keyboardListener)
glutSpecialFunc(specialKey)
glutMainLoop()
