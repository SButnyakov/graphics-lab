from PIL import Image
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys

TITLE = b"Butnyakov. Lab 2."

xRot = 0
yRot = 0
zRot = 1
red = 1
blue = 0


def specialkeys(key, x, y):
    global xRot
    global yRot
    global zRot
    global red
    global blue

    if key == GLUT_KEY_UP and xRot < 1:
        xRot += 1.0
    if key == GLUT_KEY_DOWN and xRot > -1:
        xRot -= 1
    if key == GLUT_KEY_LEFT and yRot > -1:
        yRot -= 1
    if key == GLUT_KEY_RIGHT and yRot < 1:
        yRot += 1
    if key == GLUT_KEY_F1 and zRot < 1:
        zRot += 1
    if key == GLUT_KEY_F2 and zRot > -1:
        zRot -= 1
    if key == GLUT_KEY_F3:
        red = 1
        blue = 0
    if key == GLUT_KEY_F4:
        red -= 0.2
        blue = 0
    if key == GLUT_KEY_F5:
        blue = 1
        red = 0
    if key == GLUT_KEY_F6:
        blue -= 0.2
        red = 0
    if key == GLUT_KEY_F6:
        blue = 1
        red = 1

    glutPostRedisplay()


def display():
    global xRot
    global yRot
    global zRot
    global red
    global blue

    glClearColor(0.5, 0.5, 0.5, 1)
    glClear(GL_COLOR_BUFFER_BIT)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_POSITION, [yRot, xRot, zRot, 1.0])
    light_diffuse = [red, blue, 0, 1.0]
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
    glLightfv(GL_LIGHT0, GL_SPECULAR, light_diffuse)
    glEnable(GL_DEPTH_TEST)

    # создание тетраэдра
    glPushMatrix()
    glDisable(GL_CULL_FACE)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, [1.0, 1.0, 1.0, 0.4])
    glMaterialfv(GL_FRONT, GL_AMBIENT, (0.5, 0.5, 0.5, 0.4))
    glMaterialfv(GL_FRONT, GL_SPECULAR, (0, 0, 0, 0.4))
    glMaterialfv(GL_FRONT, GL_SHININESS, 0)
    glRotatef(45, 1.0, 1.0, 1.0)
    glTranslatef(-0.4, 0.8, 0)
    glColor4f(1.0, 1.0, 1.0, 0.4)
    glScale(0.4, 0.4, 0.4)
    glutSolidTetrahedron()
    glPopMatrix()

    # создание сферы
    glPushMatrix()
    glEnable(GL_CULL_FACE)
    quadObj1 = gluNewQuadric()
    glColor3f(1.0, 1.0, 1.0)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, [1.0, 1.0, 1.0, 1.0])
    glMaterialfv(GL_FRONT, GL_AMBIENT, (0.2, 0.2, 0.2, 1.0))
    glMaterialfv(GL_FRONT, GL_SPECULAR, (0.2, 0.2, 0.2, 1.0))
    glMaterialfv(GL_FRONT, GL_SHININESS, 128)
    glTranslatef(0.5, 0.5, 0)
    gluSphere(quadObj1, 0.3, 100, 100)
    glPopMatrix()

    
    # создание чайника
    glLightfv(GL_LIGHT0, GL_POSITION, [yRot, xRot, -zRot, 0.0])
    glPushMatrix()
    texture = load_texture(r'E:\\projects\\graphics\\minecraft_dirt.jpg')
    glMaterialfv(GL_FRONT, GL_DIFFUSE, [1.0, 1.0, 1.0, 1.0])
    glMaterialfv(GL_FRONT, GL_AMBIENT, (0.2, 0.2, 0.2, 1.0))
    glMaterialfv(GL_FRONT, GL_SPECULAR, (0.2, 0.2, 0.2, 1.0))
    glMaterialfv(GL_FRONT, GL_SHININESS, 0)
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, texture)

    glTranslatef(-0.5, -0.5, 0)
    glColor3f(1.0, 0, 0)

    glutSolidTeapot(0.3)
    glDisable(GL_TEXTURE_2D)
    glPopMatrix()

    glutSwapBuffers()


def load_texture(filename):
    image = Image.open(filename)
    image = image.transpose(Image.FLIP_TOP_BOTTOM)
    width, height = image.size
    image_data = image.convert("RGBA").tobytes()

    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, image_data)

    return texture_id


if __name__ == '__main__':
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(1200, 800)
    glutInitWindowPosition(100, 100)
    glutInit(sys.argv)

    glutCreateWindow(TITLE)
    glutDisplayFunc(display)
    glutSpecialFunc(specialkeys)
    glutMainLoop()
