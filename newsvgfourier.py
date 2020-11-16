import pygame
import sys
import numpy as np
import pathsModule as pm
from svg.path import Path, parse_path

width, height = 1024, 768
imgwidth = 800
imgheight = 600



BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
no_points = 2000

lineMemory = False

def toCentralCoords(wh):
    return (int(wh.real - width/2), int(wh.imag - height/2))


def toNormalCoords(wh):
    return (int(wh.real + width/2), int(wh.imag + height/2))

def svgToNormalCoords(wh):
    return (wh.real - imgwidth + (wh.imag - imgheight)*(1j))
def getThePowerThing(n, t):
    ''' return e^(-n*2*pi)'''
    return np.power(np.e, n * 2 * np.pi * 1j * t)

def calcToDraw(t):
    coords = 0
    i = int(round(t/delta))
    for c in clist:
        x = c[0] * getThePowerThing(-c[1], t)
        xs[i].append(x)
        coords += x
        if(c[1]*2 >= current_depth):
            break
    todraw.append(coords)
def draw(screen, t):

    coords = 0
    prevTodraw = todraw[len(todraw)-1]
    i = int(round(t/delta))
    if i == len(xs):
        i = len(xs) -1
    if i >= len(xs):
        x = 0
    xses = xs[i]
    for x in xses:
        if int(np.absolute(x)) > 10:
            pygame.draw.circle(screen, BLUE, toNormalCoords(
                coords), int(np.absolute(x)), 1)
        line = (toNormalCoords(coords), toNormalCoords(coords + x))
        pygame.draw.line(screen, RED, line[0], line[1], 2)
        coords +=x
    n1 = int(delta_1 / 80)
    n2 = int(n1*3)
    if lineMemory == False:
        if i + n1 < delta_1:
            l = todraw[:i]
        else:
            l = todraw[n1 - delta_1 + i:i]
            prevTodraw = todraw[n1 - delta_1 + i -1]
    elif i + n1 < delta_1:
        l = todraw[:i] + todraw[i + n1:]
    elif i + n1 >= delta_1:
        l = todraw[n1 - delta_1 + i:i]
        prevTodraw = todraw[n1 - delta_1 + i -1]
    c = 0
    for count, xy in enumerate(l):
        if count > i and count < i + n2 - n1:
            c = fadin1(count, n1,n2, i)
        elif i + n1 > delta_1 and count < n2-n1:
            c = fadin2(count,n1,n2,i, delta_1)
        else:
            c = 0
        if not count == i:
            pygame.draw.line(screen, (c,c,c), toNormalCoords(prevTodraw), toNormalCoords(xy),4)
        prevTodraw = xy
def fadin1(count, n1,n2, i):
    return 255 - int(255*(count - i)/(n2-n1))
def fadin2(count, n1, n2, i, d):
    return int(255*(n2-n1-count)/(n2-n1))
def drawDotOnly(screen):
    for xy in todraw:
        pygame.draw.circle(screen, (0, 0, 0), toNormalCoords(xy), 2)

def drawBackground(bg):
    bg.fill((255,255,255))
    for i in range(no_points):
        pygame.draw.circle(bg, GREEN, toNormalCoords(points[i]), 3)
def drawInfo(screen):
    text1 = "No. Cirles: " + str(current_depth)
    text2 = "Speed: " + str(deltaMul) + "x"
    text1 = font.render(text1, True, (0,0,0))
    text2 = font.render(text2, True, (0,0,0))
    screen.blit(text1,(0,0))
    screen.blit(text2,(0,50))
def allTodraw():
    global xs
    xs = []
    global todraw
    todraw = []
    global lineMemory
    lineMemory = False
    for i in range(delta_1):
        xs.append([])
        calcToDraw(i*delta)

def fourierToNormal(wh):
    return (wh.real - 1000 + (wh.imag - imgheight)*(1j))/1.5

def setFourier():
    global points
    global no_points
    global depth
    depth = 250
    no_points = 2000
    path = parse_path(pm.d)
    points = [fourierToNormal(path.point(i/no_points, error=1e-1))
          for i in range(no_points)]
def rectToNormal(wh):
    return (wh.real - imgwidth/2 + (wh.imag)*(1j))

def setRect():
    global points
    global no_points
    global depth
    depth = 250
    no_points = 1000
    path = parse_path(pm.rectPath)
    points = [rectToNormal(path.point(i/no_points, error=1e-1))
          for i in range(no_points)]
def triangleToNormal(wh):
    return (wh.real - imgwidth/2 + (wh.imag)*(1j))

def setTriangle():
    global points
    global no_points
    global depth
    depth = 250
    no_points = 1000
    path = parse_path(pm.trianglePath)
    points = [rectToNormal(path.point(i/no_points, error=1e-1))
          for i in range(no_points)]
def plToNormal(wh):
    return (wh.real - imgwidth/2 + (wh.imag)*(1j))/10

def setPlPath():
    global points
    global no_points
    global depth
    depth = 1000
    no_points = 10000
    path = parse_path(pm.plLogo)
    points = [plToNormal(path.point(i/no_points, error=1e-1))
          for i in range(no_points)]
def mathUpToNormal(wh):
    return (wh.real - imgwidth/2.6 + (wh.imag - imgwidth/2.6 )*(1j))
def setMathUp():
    global points
    global no_points
    global depth
    depth = 1000
    no_points = 10000
    path = parse_path(pm.mathUp)
    points = [mathUpToNormal(path.point(i/no_points, error=1e-1))
          for i in range(no_points)]

def calcFourier():
    clist2 = np.fft.fft(points)/no_points
    global clist
    clist = [(clist2[0],0)]
    for i in range(1, depth+1):
        clist.append((clist2[i], i))
        clist.append((clist2[len(clist2)-i], -i))
    allTodraw()
pygame.init()

font = pygame.font.SysFont('arial', 20)
time = pygame.time.get_ticks()

drawingMathUp=False
setMathUp()

myimage = pygame.image.load("logo.png")
imgRect = myimage.get_rect()
w,h = imgRect.width, imgRect.height
imgRect = pygame.Rect(width/2 -w /2,height/2 -h/2,w, h)

t = 0
delta = 0.001
delta_1 = int(1/delta)
todraw = []
xs = []


depth = 250
current_depth = 1
calcFourier()

#clist = [(200,0),(-100j,1),(100j,-1),(50,2),(-50,-2)]


screen = pygame.display.set_mode((width, height))
#background = pygame.Surface(screen.get_size())
#drawBackground(background)
deltaMul = 2
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()	
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                current_depth = 1
                allTodraw()
                t = 0
            elif event.key == pygame.K_2:
                current_depth = 5
                allTodraw()
                t = 0
            elif event.key == pygame.K_3:
                current_depth = 10
                allTodraw()
                t = 0
            elif event.key == pygame.K_4:
                current_depth = 20
                allTodraw()
                t = 0
            elif event.key == pygame.K_5:
                current_depth = 50
                allTodraw()
                t = 0
            elif event.key == pygame.K_6:
                current_depth = 100
                allTodraw()
                t = 0
            elif event.key == pygame.K_7:
                current_depth = 150
                allTodraw()
                t = 0
            elif event.key == pygame.K_8:
                current_depth = 250
                allTodraw()
                t = 0
            elif event.key == pygame.K_9:
                current_depth = 1000
                allTodraw()
                t = 0
            elif event.key == pygame.K_z:
                drawingMathUp = False
                setRect()
                calcFourier()
                t = 0
            elif event.key == pygame.K_x:
                drawingMathUp = False
                setTriangle()
                calcFourier()
                t = 0
            elif event.key == pygame.K_c:
                drawingMathUp = False
                setFourier()
                calcFourier()
                t = 0
            elif event.key == pygame.K_v:
                drawingMathUp = False
                setMathUp()
                calcFourier()
                t = 0
            elif event.key == pygame.K_n:
                current_depth += 2
                allTodraw()
                t = 0
            elif event.key == pygame.K_b:
                current_depth -= 2
                allTodraw()
                t = 0
            elif event.key == pygame.K_m:
                drawingMathUp = not drawingMathUp
            elif event.key == pygame.K_t:
                deltaMul -=1
            elif event.key == pygame.K_y:
                deltaMul +=1
            elif event.key == pygame.K_g:
                deltaMul /=2
            elif event.key == pygame.K_h:
                deltaMul *=2
            

    screen.fill((255,255,255))
    
    if drawingMathUp:
        screen.blit(myimage,imgRect)
    draw(screen, t)
        

    drawInfo(screen)
    t += delta*deltaMul
    if t > 1:
        t = 0
        lineMemory = True
    pygame.display.flip()