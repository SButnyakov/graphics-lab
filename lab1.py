import time

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

WINDOW = None
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

TITLE = b"Butnyakov. Lab 1."

STATES = {
    "FIRST_PART_INIT": 0,
    "FIRST_PART_TEAPOT_MOVE": 1,
    "FIRST_PART_SPHERE_MOVE": 2,
    "SECOND_PART_INIT": 3,
    "SECOND_PART_CONE_SCALE": 4
}
CURRENT_STATE = 0

CAMERA_SPEED = 0.2
CAMERA_ZOOM_SPEED = 0.05
CAMERA_POS = [0.0, 0.0, 5.0]
CAMERA_FRONT = [0.0, 0.0, -1.0]
CAMERA_UP = [0.0, 1.0, 3.0]
CAMERA_ZOOM = 0.0
CAMERA_MAX_ZOOM = -0.94

MOVE_TEAPOT_MAX = 2.5
MOVE_SPHERE_MIN = -3.0
SCALE_CONE_MAX = 3.0

MOVE_TEAPOT = 0.0
MOVE_SPHERE = 0.0
SCALE_CONE = 1.0

ANGLE = 0


def idle():
    global ANGLE
    ANGLE = (ANGLE + 1) % 360
    glutPostRedisplay()
    time.sleep(0.025)


def keyboard(*args):
    global CURRENT_STATE
    global WINDOW
    match(args[0]):
        case b'w':
            CAMERA_POS[1] += CAMERA_SPEED
        case b's':
            CAMERA_POS[1] -= CAMERA_SPEED
        case b'a':
            CAMERA_POS[0] -= CAMERA_SPEED
        case b'd':
            CAMERA_POS[0] += CAMERA_SPEED
        case b' ':
            if CURRENT_STATE == STATES["SECOND_PART_CONE_SCALE"]:
                glutDestroyWindow(WINDOW)
            else:
                CURRENT_STATE += 1
        case b'\x1b':
            glutDestroyWindow(WINDOW)


def mouse(*args):
    global CAMERA_ZOOM
    match(args[0]):
        case 3:
            if CAMERA_ZOOM > CAMERA_MAX_ZOOM:
                CAMERA_ZOOM -= CAMERA_ZOOM_SPEED
        case 4:
            CAMERA_ZOOM += CAMERA_ZOOM_SPEED


def display():
    global MOVE_SPHERE
    global MOVE_TEAPOT
    global SCALE_CONE
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    frustum = 1. + CAMERA_ZOOM
    glFrustum(-frustum, frustum, -frustum, frustum, 1.5, 20.)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    gluLookAt(
        CAMERA_POS[0], CAMERA_POS[1], CAMERA_POS[2],
        CAMERA_POS[0] + CAMERA_FRONT[0], CAMERA_POS[1] + CAMERA_FRONT[1], CAMERA_POS[2] + CAMERA_FRONT[2],
        CAMERA_UP[0], CAMERA_UP[1], CAMERA_UP[2])

    if STATES["FIRST_PART_INIT"] <= CURRENT_STATE < STATES["SECOND_PART_INIT"]:
        glPushMatrix()
        glColor3f(0., 1., 0.)
        glTranslatef(0., 0. + MOVE_SPHERE, 0.)
        if MOVE_SPHERE > MOVE_SPHERE_MIN and CURRENT_STATE == STATES["FIRST_PART_SPHERE_MOVE"]:
            MOVE_SPHERE -= 0.1
        glutWireSphere(1.0, 20, 20)
        glPopMatrix()

        glPushMatrix()
        glTranslatef(0. + MOVE_TEAPOT, 0., 0.)
        if MOVE_TEAPOT < MOVE_TEAPOT_MAX and CURRENT_STATE == STATES["FIRST_PART_TEAPOT_MOVE"]:
            MOVE_TEAPOT += 0.1
        glColor3f(1., 0., 0.)
        glutWireTeapot(1.)
        glPopMatrix()
    elif CURRENT_STATE >= STATES["SECOND_PART_INIT"]:
        glPushMatrix()
        glColor3f(0., 1., 0.)
        glTranslatef(-1.5, 1., 0.)
        glutWireTetrahedron()
        glPopMatrix()

        glPushMatrix()
        glColor3f(1., 0., 0.)
        glRotatef(90., -1., 0., 0.)
        glTranslatef(1., 0., -0.5)
        glScalef(SCALE_CONE, SCALE_CONE, SCALE_CONE)
        if SCALE_CONE < SCALE_CONE_MAX and CURRENT_STATE == STATES["SECOND_PART_CONE_SCALE"]:
            SCALE_CONE += 0.1
        glutWireCone(0.5, 1.5, 10, 10)
        glPopMatrix()

    glutSwapBuffers()


def main():
    global WINDOW
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
    glutInitWindowPosition(int((glutGet(GLUT_SCREEN_WIDTH) - WINDOW_WIDTH) / 2),
                           int((glutGet(GLUT_SCREEN_HEIGHT) - WINDOW_HEIGHT) / 2))

    WINDOW = glutCreateWindow(TITLE)
    glutDisplayFunc(display)
    glutKeyboardFunc(keyboard)
    glutMouseFunc(mouse)
    glutIdleFunc(idle)

    glutMainLoop()


if __name__ == '__main__':
    main()
