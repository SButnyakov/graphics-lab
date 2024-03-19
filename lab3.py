import math
from math import *

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from PIL import Image as Image
import numpy


start = False
angle_cone = 185
angle_diff = 0
tr_z = -2.3
change_angle = False
angl_e = 0
x_cord = 3.2
y_cord = 4
z_cord = 3.2
y_diff = 0
a = 1.73205 * 0.8
b = 1 * 0.8
c = 0.577350 * 0.8
d = 1.638304 * 0.8

octCos = (a * a - b * b + 0) / sqrt(pow(a, 2) + pow(b, 2) + 0) / sqrt(pow(a, 2) + pow(b, 2) + 0)
global texture1, texture2


def init():
    global texture1, texture2
    # текстура для "пола"
    texture2 = get_texture(
        r"E:\\projects\\graphics\\minecraft_dirt.jpg ")
    # текстура для конуса
    texture1 = get_texture(
        r"E:\\projects\\graphics\\minecraft_dirt.jpg")
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    glShadeModel(GL_FLAT)
    glEnable(GL_AUTO_NORMAL)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)


def get_texture(filename):
    img = Image.open(filename)
    img_data = numpy.array(list(img.getdata())).astype(numpy.int8)
    text_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, text_id)
    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img.size[0], img.size[1], 0, GL_RGB,
                 GL_UNSIGNED_BYTE, img_data)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    img.close()
    return text_id


def special(key, x, y):
    global angle_diff, start
    if key == GLUT_KEY_LEFT:
        angle_diff = 1.5
        start = True


def reshape(w: int, h: int):
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    if w <= h:
        glOrtho(-10, 10, -10 * h / w, 10 * h / w, -10, 10)
    else:
        glOrtho(-10 * w / h, 10 * w / h, -10, 10, -10, 10)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(
        1.0, 1.0, 0.8,
        0.0, 0.0, 0.0,
        -1.0, -1.0, 0.0)


def rotate_cone():
    global angle_diff, tr_z, start, angle_cone
    tmp = 1 / 30
    tmp2 = math.fabs((2.3 - 2.0) / 1000)
    if math.fabs(angle_diff) < 0.00001:
        angle_diff = 0
        start = False
    else:
        angle_diff -= tmp
        tr_z += tmp2


def display():
    global angle_cone, change_angle, tr_z, angl_e
    global z_cord, y_diff

    lightPosition = (15, 20.0, 30, 1.0)
    lightColor = (1.0, 1.0, 1.0, 1.0)
    lightAmbient = (0.1, 0.1, 0.1, 1.0)
    glEnable(GL_DEPTH_TEST)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glClearColor(0, 0, 0, 0)

    glPushMatrix()
    glLightfv(GL_LIGHT0, GL_DIFFUSE, lightColor)
    glLightfv(GL_LIGHT0, GL_SPECULAR, lightColor)
    glLightfv(GL_LIGHT0, GL_AMBIENT, lightAmbient)
    glLightfv(GL_LIGHT0, GL_POSITION, lightPosition)
    glPopMatrix()

    angl_e = angl_e + 0.04 if change_angle else 0
    if start:
        rotate_cone()
    angle_cone += angle_diff

    drawFloor()

    glPushMatrix()

    glTranslatef(x_cord, y_cord + y_diff, z_cord)
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, texture1)
    glMaterialfv(GL_FRONT, GL_SPECULAR, [0, 0, 0, 1])
    glMaterialfv(GL_FRONT, GL_SHININESS, 128)
    glScalef(0.3, 0.3, 0.3)
    glRotatef(-90, 0, 1, 0)
    glRotatef(90, -1, 0, 0)
    glRotatef(angle_cone, -0.8, 0, 0)
    glRotatef(27, 0, 1, 0)
    glRotatef(angle_cone * 2.3, 0, 0, 1)
    glTranslatef(0, 0, 4)
    qobj = gluNewQuadric()
    gluCylinder(qobj, 0, 2.0, 4.0, 64, 64)
    glDisable(GL_TEXTURE_2D)

    glPopMatrix()
    glFlush()


def drawFloor():
    glCullFace(GL_BACK)
    glColor3f(0.0, 0.0, 0.0)

    glPushMatrix()
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, texture2)

    glBegin(GL_POLYGON)
    glNormal3f(0, 0, 1)
    glTexCoord2f(0, 0)
    glVertex3f(-7.2, 7.2, -0.2)
    glTexCoord2f(0, 3)
    glVertex3f(7.2, 7.2, -0.2)
    glTexCoord2f(3, 3)
    glVertex3f(7.2, -7.2, -0.2)
    glTexCoord2f(3, 0)
    glVertex3f(-7.2, -7.2, -0.2)
    glEnd()

    glDisable(GL_TEXTURE_2D)
    glPopMatrix()


def timer(value):
    glutPostRedisplay()
    glutTimerFunc(35, timer, 0)


glutInit()
glutInitDisplayMode(GLUT_SINGLE | GLUT_RGBA | GLUT_DEPTH)
glutInitWindowSize(1000, 1000)
glutInitWindowPosition(220, 0)
glutCreateWindow(b"lab3")

glEnable(GL_NORMALIZE)
glutReshapeFunc(reshape)
glutDisplayFunc(display)
glutSpecialFunc(special)
init()
glutTimerFunc(50, timer, 0)
glutMainLoop()
