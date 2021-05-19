import sys, pygame, os
import numpy as np
import threading
from pygame.locals import *
from pygame.constants import *
from OpenGL.GL import *
from OpenGL.GLU import *
from objloader import *

pygame.init()
viewport = (800,600)
hx = viewport[0]/2
hy = viewport[1]/2
srf = pygame.display.set_mode(viewport, OPENGL | DOUBLEBUF)
glLightfv(GL_LIGHT0, GL_POSITION,  (-40, 200, 100, 0.0))
glLightfv(GL_LIGHT0, GL_AMBIENT, (0.2, 0.2, 0.2, 1.0))
glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.5, 0.5, 0.5, 1.0))
glEnable(GL_LIGHT0)
glEnable(GL_LIGHTING)
glEnable(GL_COLOR_MATERIAL)
glEnable(GL_DEPTH_TEST)
glShadeModel(GL_SMOOTH)

os.chdir("OBJ")
matrix = OBJ("matrix.obj", swapyz = True)

Blue = []
Blue_call = []
Red = []
Red_call = []
Numbers = []
Numbers_call = []

for i in range(27):
    Blue.append(OBJ(str("cube" + str(i+1) + ".obj"), swapyz = False))
    Blue_call.append(False)
    Red.append(OBJ(str("red" + str(i+1) + ".obj"), swapyz = False))
    Red_call.append(False)
    Numbers.append(OBJ(str("number" + str(i+1) + ".obj"), swapyz = False))
    Numbers_call.append(True)

clock = pygame.time.Clock()
glMatrixMode(GL_PROJECTION)
glLoadIdentity()
width, height = viewport
gluPerspective(90, width/float(height), 1, 100.0)
glEnable(GL_DEPTH_TEST)
glMatrixMode(GL_MODELVIEW)
rx, ry = (0,0)
tx, ty = (0,0)
zpos = 30
rotate = move = False

def CHECK():
    player1 = np.array(Blue_call).reshape((3, 3, 3))
    player2 = np.array(Red_call).reshape((3, 3, 3))
    p1_x_sum = np.sum(player1, axis = 0).reshape((9, 1))
    if(3 in p1_x_sum):
        print("Player 1 wins !")
        return 0
    p2_x_sum = np.sum(player2, axis = 0).reshape((9, 1))
    if(3 in p2_x_sum):
        print("Player 2 wins !")
        return 0
    p1_y_sum = np.sum(player1, axis = 1).reshape((9, 1))
    if(3 in p1_y_sum):
        print("Player 1 wins !")
        return 0
    p2_y_sum = np.sum(player2, axis = 1).reshape((9, 1))
    if(3 in p2_y_sum):
        print("Player 2 wins !")
        return 0
    p1_z_sum = np.sum(player1, axis = 2).reshape((9, 1))
    if(3 in p1_z_sum):
        print("Player 1 wins !")
        return 0
    p2_z_sum = np.sum(player2, axis = 2).reshape((9, 1))
    if(3 in p2_z_sum):
        print("Player 2 wins !")
        return 0 
    for i in range(3):
        temp = player1[i,:,:]
        if(np.trace(temp) == 3 or np.trace(np.fliplr(temp)) == 3):
            print("Player 1 wins !")
            return 0
        temp = player2[i,:,:]
        if(np.trace(temp) == 3 or np.trace(np.fliplr(temp)) == 3):
            print("Player 2 wins !")
            return 0
    for i in range(3):
        temp = player1[:,i,:]
        if(np.trace(temp) == 3 or np.trace(np.fliplr(temp)) == 3):
            print("Player 1 wins !")
            return 0
        temp = player2[:,i,:]
        if(np.trace(temp) == 3 or np.trace(np.fliplr(temp)) == 3):
            print("Player 2 wins !")
            return 0
    for i in range(3):
        temp = player1[:,:,i]
        if(np.trace(temp) == 3 or np.trace(np.fliplr(temp)) == 3):
            print("Player 1 wins !")
            return 0
        temp = player2[:,:,i]
        if(np.trace(temp) == 3 or np.trace(np.fliplr(temp)) == 3):
            print("Player 2 wins !")
            return 0
    if(3 in [np.trace(np.diagonal(player1)), np.trace(np.fliplr(np.diagonal(player1))), np.trace(np.diagonal(np.fliplr(player1))), np.trace(np.fliplr(np.diagonal(np.fliplr(player1))))]):
        print("Player 1 wins !")
        return 0
    if(3 in [np.trace(np.diagonal(player2)), np.trace(np.fliplr(np.diagonal(player2))), np.trace(np.diagonal(np.fliplr(player2))), np.trace(np.fliplr(np.diagonal(np.fliplr(player2))))]):
        print("Player 2 wins !")
        return 0
    
    return 1

def INPUT():
    condition = 1
    turn = 1
    while(condition):
        if(turn == 1):
            x = int(input("Player 1 Enter : "))
            Blue_call[x-1] = True
            Numbers_call[x-1] = False
        else:
            x = int(input("Player 2 Enter : "))
            Red_call[x-1] = True
            Numbers_call[x-1] = False    
        turn*=-1
        condition = CHECK()
input_thread = threading.Thread(target = INPUT)
input_thread.start()

while 1:
    clock.tick(60)
    for e in pygame.event.get():
        if e.type == QUIT:
            sys.exit()
        elif e.type == KEYDOWN and e.key == K_ESCAPE:
            sys.exit()
        elif e.type == MOUSEBUTTONDOWN:
            if e.button == 4: zpos = max(1, zpos-1)
            elif e.button == 5: zpos += 1
            elif e.button == 1: rotate = True
            elif e.button == 3: move = True
        elif e.type == MOUSEBUTTONUP:
            if e.button == 1: rotate = False
            elif e.button == 3: move = False
        elif e.type == MOUSEMOTION:
            i, j = e.rel
            if rotate:
                rx += i
                ry += j
            if move:
                tx += i
                ty -= j
    
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glTranslate(tx/20., ty/20., - zpos)
    glRotate(ry, 1, 0, 0)
    glRotate(rx, 0, 1, 0)
    glCallList(matrix.gl_list)
    
    for i in range(len(Numbers_call)):
        if(Numbers_call[i]):
          glCallList(Numbers[i].gl_list)
    for i in range(len(Blue_call)):
        if(Blue_call[i]):
          glCallList(Blue[i].gl_list)
    for i in range(len(Red_call)):
        if(Red_call[i]):
          glCallList(Red[i].gl_list)

    pygame.display.flip()
    
input_thread.join()