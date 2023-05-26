import pygame, sys, random
from pygame.locals import *

# 按 Shift+F10 执行或将其替换为您的代码。
# 按 双击 Shift 在所有地方搜索类、文件、工具窗口、操作和设置。
FPS          = 30
WINDOWWIDTH  = 640
WINDOWHEIGTH = 480
BOARDWIDTH   = 4
BOARDHEIGTH  = 4
TILESIZE     = 80
BLANK        = None

#             R    G    B
BLACK   = (   0,   0,   0)
WHITE   = ( 255, 255, 255)
BRIGHTBLUE= ( 0,   50,255)
GREEN   = (   0, 204,   0)
DARKTURQUOISE   = ( 3, 54, 73)

BGCOLOR        = DARKTURQUOISE
TILECOLOR      = GREEN
TEXTCOLOR      = WHITE
BORDERCOLOR    = BRIGHTBLUE
BASICFONTSIZE  = 20

BUTTONCOLOR    =WHITE
BUTTONTEXTCOLOR=BLACK
MESSAGECOLOR   =WHITE

XMARGIN = int((WINDOWWIDTH - (TILESIZE * BOARDWIDTH + (BOARDWIDTH - 1)))/2)
YMARGIN = int((WINDOWHEIGTH - (TILESIZE * BOARDHEIGTH + (BOARDHEIGTH - 1)))/2)

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'


def main ():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, RESET_SURF, RESET_RECT, NEW_SURF, NEW_RECT, SOLVE_SURF, SOLVE_RECT
    # 负责创建窗口，Clock对象，Font对象

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGTH))
    pygame.display.set_caption('Slide Puzzle')
    BASICFONT = pygame.font.Font('freesansbold.ttf', BASICFONTSIZE)
    #设置按钮
    RESET_SURF, RESET_RECT = makeText('Rest',TEXTCOLOR,TILECOLOR,WINDOWWIDTH - 120, WINDOWHEIGTH-90)
    NEW_SURF, NEW_RECT = makeText('New Game',TEXTCOLOR,TILECOLOR,WINDOWWIDTH - 120, WINDOWHEIGTH-60)
    SOLVE_SURF,SOLVE_RECT = makeText('Solve', TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 120, WINDOWHEIGTH - 30)

    mainBoard, solutioSeq = generateNewPuzzle(80)
    SOLVEDBOARD = getStartingBoard()#用来对比的，答案和最开始是一样的

    allMoves = []#记录所有的步数，解决的时候反向就可以了
    #主游戏循环
    while True:
        slideTo = None
        msg = 'Click tile or press arrow keys to slide.'
        if mainBoard == SOLVEDBOARD:
            msg = 'Solved'
        drawBoard(mainBoard, msg)
        #点击按钮
        checkForQuit()
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP:
                spotx, spoty = getSpotClicked(mainBoard, event.pos[0], event.pos[1])
                #检测是不是在按钮上点击了
                if (spotx,spoty) == (None,None):
                    #检测是不是点击到开始新的解决按钮
                    if RESET_RECT.collidepoint(event.pos):
                        resetAnimation(mainBoard, allMoves)
                        allMoves = []
                    elif NEW_RECT.collidepoint(event.pos):
                        mainBoard, solutioSeq = generateNewPuzzle(80)
                        allMoves = []
                    elif SOLVE_RECT.collidepoint(event.pos):
                        resetAnimation(mainBoard, solutioSeq + allMoves)
                        allMoves = []
                    #用鼠标点击滑动贴片
                else:
                        blankx, blanky = getBlankPosition(mainBoard)
                        if spotx == blankx + 1 and spoty == blanky:
                            slideTo = LEFT
                        elif spotx == blankx - 1 and spoty == blanky:
                            slideTo = RIGHT
                        elif spotx == blankx and spoty == blanky + 1:
                            slideTo = UP
                        elif spotx == blankx and spoty == blanky - 1:
                            slideTo = DOWN
            #用键盘滑动铁片
            elif event.type == KEYUP:
                if event.key in (K_LEFT, K_a) and isValidMove(mainBoard, LEFT):
                    slideTo = LEFT
                elif event.key in (K_RIGHT, K_d) and isValidMove(mainBoard, RIGHT):
                    slideTo = RIGHT
                elif event.key in (K_UP, K_w) and isValidMove(mainBoard, UP):
                    slideTo = UP
                elif event.key in (K_DOWN, K_s) and isValidMove(mainBoard, DOWN):
                    slideTo = DOWN
        #实际执行贴片移动
        if slideTo:
            slideAnimation(mainBoard, slideTo, 'Click tile or press arrow keys to slide.', 8)
            makeMove(mainBoard, slideTo)
            allMoves.append(slideTo)
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def terminate():#IDE和终止Pygame程序,这样就可以在程序中多处实现结束，而只用调用一个函数就行了
    pygame.quit()
    sys.exit()

def checkForQuit():#检测特定的事件，并将事件添加到pygame的事件队列中
    for event in pygame.event.get(QUIT):#传递事件常量，如果发生则处理
        terminate()
    for event in pygame.event.get(KEYUP):
        if event.key == K_ESCAPE:
            terminate()
        pygame.event.post(event)#用自己的代码想pygame的事件队列添加event事件

def getStartingBoard():#创建游戏版数据结构
    counter = 1
    board = []
    for x in range(BOARDWIDTH):
        column = []
        for y in range(BOARDHEIGTH):
            column.append(counter)
            counter += BOARDWIDTH
        board.append(column)
        counter -= BOARDWIDTH*(BOARDHEIGTH-1)+BOARDWIDTH-1
    board[BOARDWIDTH-1][BOARDHEIGTH-1]=BLANK
    return board

def getBlankPosition(board):#不记录空白的位置,用函数来寻找空白的位置
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGTH):
            if board[x][y] == BLANK:
                return (x,y)

def makeMove(board, move):#通过更新移动版数据结构来移动
    blankx, blanky = getBlankPosition(board)
    #贴片的值和空白的值互换
    if move == UP:
        board[blankx][blanky], board[blankx][blanky+1] = board[blankx][blanky+1],board[blankx][blanky]
    elif move == DOWN:
        board[blankx][blanky], board[blankx][blanky - 1] = board[blankx][blanky - 1], board[blankx][blanky]
    elif move == LEFT:
        board[blankx][blanky], board[blankx+1][blanky] = board[blankx+1][blanky ], board[blankx][blanky]
    elif move == RIGHT:
        board[blankx][blanky], board[blankx-1][blanky ] = board[blankx-1][blanky  ], board[blankx][blanky]
    #没有返回值，因为board是列表引用能够直接改变内存的值

def isValidMove(board, move):#何时不适用断言,判断移动是否合理，可行则返回True
    blankx, blanky = getBlankPosition(board)
    return (move == UP and blanky != len(board[0])-1) or \
           (move == DOWN and blanky != 0) or \
           (move == LEFT and blankx != len(board)-1) or \
           (move == RIGHT and blankx != 0)

def getRandomMove(board, lastMove = None):#获取一次不是那么随机的移动
    validMoves = [UP,DOWN,LEFT,RIGHT]
    #防止函数做上一个动作
    if lastMove == UP or not isValidMove(board, DOWN):
        validMoves.remove(DOWN)
    if lastMove == DOWN or not isValidMove(board, UP):
        validMoves.remove(UP)
    if lastMove == LEFT or not isValidMove(board, RIGHT):
        validMoves.remove(RIGHT)
    if lastMove == RIGHT or not isValidMove(board, LEFT):
        validMoves.remove(LEFT)
    return random.choice(validMoves)

def getLeftTopOfTile(tileX, tileY):#将贴片坐标转化为像素坐标
    left = XMARGIN + (tileX*TILESIZE)+(tileX-1)
    top = YMARGIN + (tileY * TILESIZE) + (tileY - 1)
    return (left,top)

def getSpotClicked(board, x, y):#将像素坐标转换为游戏版坐标
    for tileX in range(len(board)):
        for tileY in range(len(board[0])):
            left, top = getLeftTopOfTile(tileX,tileY)
            tileRect = pygame.Rect(left,top,TILESIZE,TILESIZE)
            if tileRect.collidepoint(x,y):
                return (tileX,tileY)
    return (None,None)

def drawTile(tilex, tiley, number, adjx=0, adjy=0):#绘制一个贴片
    left ,top = getLeftTopOfTile(tilex,tiley)
    pygame.draw.rect(DISPLAYSURF,TILECOLOR,(left+adjx,top+adjy,TILESIZE,TILESIZE))
    textSurf = BASICFONT.render(str(number),True,TEXTCOLOR)
    textRect = textSurf.get_rect()
    textRect.center = left+int(TILESIZE/2)+adjx,top+int(TILESIZE/2)+adjy
    DISPLAYSURF.blit(textSurf,textRect)

def makeText(text, color, bgcolor, top, left):#让文本显示在屏幕上
    textSurf = BASICFONT.render(text, True, color, bgcolor)
    textRect = textSurf.get_rect()
    textRect.topleft=(top,left)
    return (textSurf, textRect)

def drawBoard(board, message):#绘制游戏版
    DISPLAYSURF.fill(BGCOLOR)
    if message:
        textSurf, textRect= makeText(message,MESSAGECOLOR,BGCOLOR,5,5)
        DISPLAYSURF.blit(textSurf, textRect)
    for tilex in range(len(board)):
        for tiley in range(len(board[0])):
            if board[tilex][tiley]:
                drawTile(tilex,tiley,board[tilex][tiley])

    left, top = getLeftTopOfTile(0,0)
    width = BOARDWIDTH*TILESIZE
    height = BOARDHEIGTH*TILESIZE
    pygame.draw.rect(DISPLAYSURF,BORDERCOLOR,(left-5,top-5,width+11,height+11),4)
    #绘制按钮
    DISPLAYSURF.blit(RESET_SURF,RESET_RECT)
    DISPLAYSURF.blit(NEW_SURF,NEW_RECT)
    DISPLAYSURF.blit(SOLVE_SURF,SOLVE_RECT)

def slideAnimation(board, direction, message, animationSpeed):#实现贴片滑动动画
    blankx, blanky = getBlankPosition(board)
    if direction == UP:
        movex = blankx
        movey = blanky+1
    elif direction == DOWN:
        movex = blankx
        movey = blanky - 1
    elif direction == LEFT:
        movex = blankx +1
        movey = blanky
    elif direction == RIGHT:
        movex = blankx -1
        movey = blanky

    drawBoard(board,message)
    baseSurf = DISPLAYSURF.copy()#复制一个对象使得移动能够更加真实的实现
    moveLeft,moveTop=getLeftTopOfTile(movex,movey)
    pygame.draw.rect(baseSurf,BGCOLOR,(moveLeft,moveTop,TILESIZE,TILESIZE))
    for i in range(0,TILESIZE,animationSpeed):
        checkForQuit()
        DISPLAYSURF.blit(baseSurf,(0,0))
        if direction ==UP:
            drawTile(movex,movey,board[movex][movey],0,-i)
        if direction ==DOWN:
            drawTile(movex,movey,board[movex][movey],0,i)
        if direction ==LEFT:
            drawTile(movex,movey,board[movex][movey],-i,0)
        if direction ==RIGHT:
            drawTile(movex,movey,board[movex][movey],i,0)

        pygame.display.update()
        FPSCLOCK.tick(FPS)

def generateNewPuzzle(numSlides):#创建新的游戏
    sequence= []
    board = getStartingBoard()
    drawBoard(board,'')
    pygame.display.update()
    pygame.time.wait(500)

    lastMove = None
    for i in range(numSlides):
        move = getRandomMove(board,lastMove)
        slideAnimation(board,move,'Generatiing new puzzle...',int(TILESIZE/3))
        makeMove(board,move)
        sequence.append(move)
        lastMove = move
    return (board,sequence)


def resetAnimation(board, allMoves):#实现游戏重置动画
    revAllMoves=allMoves[:]#生产列表的副本而不是引用
    revAllMoves.reverse()#反向列表中的元素

    for move in revAllMoves:
        if move == UP:
            oppositMove = DOWN
        elif move == DOWN:
            oppositMove =  UP
        elif move == LEFT:
            oppositMove = RIGHT
        elif move == RIGHT:
            oppositMove = LEFT
        slideAnimation(board,oppositMove,'',animationSpeed=int(TILESIZE/2))
        makeMove(board,oppositMove)




if __name__ == '__main__':
    main()