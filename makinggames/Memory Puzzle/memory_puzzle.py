# 这是一个示例 Python 脚本。
import random

import pygame, sys
from pygame.locals import *


FPS          = 30
WINDOWWIDTH  = 640
WINDOWHEIGTH = 480
REVEALSPEED  = 8
BOXSIZE      = 40
GAPSIZE      = 10
BOARDWIDTH   = 2
BOARDHEIGTH  = 2

assert (BOARDWIDTH*BOARDHEIGTH)%2 == 0, '需要偶数个输入'

XMARGIN = int((WINDOWWIDTH-(BOARDWIDTH*(BOXSIZE+GAPSIZE)))/2)
YMARGIN = int((WINDOWHEIGTH-(BOARDHEIGTH*(BOXSIZE+GAPSIZE)))/2)

#             R    G    B
GRAY    = ( 100, 100, 100)
NAVBLUE = (  60,  60, 100)
WHITE   = ( 255, 255, 255)
RED     = ( 255,    0,  0)
GREEN   = (   0, 255,   0)
BLUE    = (   0,   0, 255)
YELLOW  = ( 255, 255,   0)
ORANGE  = ( 255, 128,   0)
PURPLE  = ( 255,   0, 255)
CYAN    = (   0, 255, 255)

BGCOLOR        = NAVBLUE
LIGHTBGCOLOR   = GRAY
BOXCOLOR       = WHITE
HIGHLIGHTCOLOR = BLUE

DONUT   = 'donut'
SQUARE  = 'square'
DIAMOND = 'diamond'
LINES   = 'lines'
OVAL    = 'oval'

#元组存放所以的颜色和形状
ALLCOLORS = (RED, GREEN, BLUE, YELLOW, ORANGE, PURPLE, CYAN)
ALLSHAPES = (DONUT, SQUARE, DIAMOND, LINES, OVAL)
assert len(ALLCOLORS)*len(ALLSHAPES)*2 >= BOARDWIDTH*BOARDHEIGTH, '形状和颜色的组合比所显示的小'

def main():
    global FPSCLOCK, DISPLAYSURF
    pygame.init()
    FPSCLOCK =pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGTH))

    mousex = 0
    mousey = 0
    pygame.display.set_caption("Memory Game")

    mainBoard = getRandomizedBoard()
    revealedBoxes = generateRevealedBoxesData(False)

    firstSelection = None

    DISPLAYSURF.fill(BGCOLOR)
    startGameAnimation(mainBoard)

    while True:
        mouseClicked = False

        DISPLAYSURF.fill(BGCOLOR)
        drawBoard(mainBoard, revealedBoxes)
        #事件处理循环evet handing loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == KEYUP and event.type == K_ESCAPE):
                pygame.quit()
                exit()
            elif event.type == MOUSEMOTION:
                mousex ,mousey = event.pos
            elif event.type == MOUSEBUTTONUP:
                mousex ,mousey = event.pos
                mouseClicked = True
        boxx, boxy = getBoxAtPixel(mousex, mousey)
        if boxx != None and boxy != None:
            if not revealedBoxes[boxx][boxy]:
                drawHighlightBox(boxx,boxy)

            if not revealedBoxes[boxx][boxy] and mouseClicked:
                revealBoxesAnimation(mainBoard, [(boxx,boxy)])
                revealedBoxes[boxx][boxy] = True

                if firstSelection == None:
                    firstSelection = (boxx,boxy)
                else:
                    icon1shape, icon1color = getShapeAndColor(mainBoard,firstSelection[0],firstSelection[1])
                    icon2shape, icon2color = getShapeAndColor(mainBoard,boxx ,boxy)

                    if icon1shape != icon2shape or icon1color != icon2color:
                        pygame.time.wait(1000)
                        coverBoxesAnimation(mainBoard,[(firstSelection[0],firstSelection[1]), (boxx,boxy)])
                        revealedBoxes[firstSelection[0]][firstSelection[1]] = False
                        revealedBoxes[boxx][boxy] = False
                    elif hasWon(revealedBoxes):
                        gameWonAnimation(mainBoard)
                        pygame.time.wait(2000)

                        mainBoard = getRandomizedBoard()
                        revealedBoxes = generateRevealedBoxesData(False)

                        drawBoard(mainBoard, revealedBoxes)
                        pygame.display.update()
                        pygame.time.wait(1000)

                        startGameAnimation(mainBoard)
                    firstSelection = None

        pygame.display.update()
        FPSCLOCK.tick(FPS)


def generateRevealedBoxesData(val):
    revealedBoxes = []
    for i in range(BOARDWIDTH):
        revealedBoxes.append([val]*BOARDHEIGTH)
    #print(revealedBoxes)
    return revealedBoxes

def getRandomizedBoard():
    icons = []
    for color in ALLCOLORS:
        for shape in ALLSHAPES:
            icons.append((shape,color))
    random.shuffle(icons)
    numIconsUsed = int(BOARDWIDTH* BOARDHEIGTH/2)
    icons = icons[:numIconsUsed]*2
    random.shuffle(icons)
    borad = []
    for x in range(BOARDWIDTH):
        column = []
        for y in range(BOARDHEIGTH):
            column.append(icons[0])
            del icons[0]
        borad.append(column)
    return borad

def splitIntoGroupsOf(groupSize, theList):
    result = []
    for i in range (0, len(theList), groupSize):
        result.append(theList[i:i+groupSize])
    return result

def leftTopCoordsOfBox(boxx,boxy):
    left = boxx * (BOXSIZE+GAPSIZE) + XMARGIN
    top = boxy * (BOXSIZE+GAPSIZE) + XMARGIN
    return (left,top)
#判断鼠标发生事件时是否在矩形的范围内
def getBoxAtPixel(x,y):
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGTH):
            left, top = leftTopCoordsOfBox(boxx,boxy)
            boxRect = pygame.Rect(left, top, BOXSIZE, BOXSIZE)
            if boxRect.collidepoint(x, y):
                return (boxx,boxy)

    return (None, None)

def drawIcon (shape, color, boxx, boxy):
    quarter = int(BOXSIZE * 0.25)
    half    = int(BOXSIZE * 0.5)
    left, top = leftTopCoordsOfBox(boxx, boxy)

    if shape == DONUT:
        pygame.draw.circle(DISPLAYSURF, color, (left + half, top + half), half - 5)
        pygame.draw.circle(DISPLAYSURF, BGCOLOR, (left + half, top + half), quarter - 5)
    elif shape == SQUARE:
        pygame.draw.rect(DISPLAYSURF, color, (left + quarter, top + quarter, BOXSIZE - half, BOXSIZE - half))
    elif shape == DIAMOND:
        pygame.draw.polygon(DISPLAYSURF, color, ((left + half, top), (left + BOXSIZE - 1, top + half), (half + left,top + BOXSIZE - 1),(left, top + half)))
    elif shape == LINES:
        for i in range(0, BOXSIZE, 4):
            pygame.draw.line(DISPLAYSURF, color, (left, top + i), (left + i,top))
            pygame.draw.line(DISPLAYSURF, color, (left + i, top + BOXSIZE - 1), (left + BOXSIZE - 1,top + 1))
    elif shape == OVAL:
        pygame.draw.ellipse(DISPLAYSURF, color, (left, top + quarter, BOXSIZE, half))

def getShapeAndColor(board, boxx, boxy):
    return board[boxx][boxy][0], board[boxx][boxy][1]

def drawBoxCovers(board, boxes, coverage):
    for box in boxes:
        left, top = leftTopCoordsOfBox(box[0], box[1])
        pygame.draw.rect(DISPLAYSURF, BGCOLOR, (left , top , BOXSIZE , BOXSIZE ))
        shape, color = getShapeAndColor(board, box[0], box[1])
        drawIcon(shape, color, box[0], box[1])
        if coverage >0:
            pygame.draw.rect(DISPLAYSURF, BOXCOLOR, (left , top , BOXSIZE , BOXSIZE ))

        pygame.display.update()
        FPSCLOCK.tick(FPS)

def revealBoxesAnimation(board, boxesToReveal):
    for coverage in range(BOXSIZE, -1, - REVEALSPEED):
        drawBoxCovers(board, boxesToReveal, coverage)

def coverBoxesAnimation(board, boxesToCover):
    for coverage in range(0, BOXSIZE - REVEALSPEED, REVEALSPEED):
        drawBoxCovers(board, boxesToCover, coverage)

def drawBoard(board, revealed):
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGTH):
            left, top = leftTopCoordsOfBox(boxx, boxy)
            if not revealed[boxx][boxy]:
                pygame.draw.rect(DISPLAYSURF, BOXCOLOR, (left , top , BOXSIZE , BOXSIZE ))
            else:
                shape, color = getShapeAndColor(board, boxx, boxy)
                drawIcon(shape, color, boxx, boxy)

def drawHighlightBox(boxx, boxy):
    left, top = leftTopCoordsOfBox(boxx,boxy)
    pygame.draw.rect(DISPLAYSURF, HIGHLIGHTCOLOR, (left - 5, top - 5, BOXSIZE + 10, BOXSIZE + 10), 4)

def startGameAnimation(board):
    coveredBoxes = generateRevealedBoxesData(False)
    boxes = []
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGTH):
            boxes.append((x, y))
    random.shuffle(boxes)
    boxGroups = splitIntoGroupsOf(8, boxes)
    drawBoard(board, coveredBoxes)
    for boxGroup in boxGroups:
        revealBoxesAnimation(board, boxGroup)
        coverBoxesAnimation(board, boxGroup)

def gameWonAnimation(board):
    coveredBoxes = generateRevealedBoxesData(True)
    color1 = LIGHTBGCOLOR
    color2 = BGCOLOR

    for i in range(13):
        color1, color2 = color2, color1
        DISPLAYSURF.fill(color1)
        drawBoard(board, coveredBoxes)
        pygame.display.update()
        pygame.time.wait(300)

def hasWon(revealedBoxes):
    for i in revealedBoxes:
        if False in i:
            return False
    return True

if __name__ == '__main__':
    main()















