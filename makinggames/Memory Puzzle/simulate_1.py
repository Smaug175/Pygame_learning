import time

import pygame, sys, random


from pygame.locals import *

# 按 Shift+F10 执行或将其替换为您的代码。
# 按 双击 Shift 在所有地方搜索类、文件、工具窗口、操作和设置。
FPS          = 30
WINDOWWIDTH  = 640
WINDOWHEIGTH = 480
FLASHSPEED   = 500
FLASHDELAY   = 200
BUTTONSIZE   = 200
BUTTONGAPSIZE= 20
TIMEOUT      = 4

#             R    G    B
BLACK   = (   0,   0,   0)
WHITE   = ( 255, 255, 255)
BRIGHTBLUE= ( 0,   0,255)
BLUE=(0,0,155)
BRIGHTRED = (255,0,0)
RED = (155,0,0)
BRIGHTGREEN = (0,255,0)
BRIGHTYELLOW=(255,255,0)
GREEN=(0,155,0)
YELLOW=(155,155,0)
DARKGRAY = (40,40,40)
bgColor=BLACK



GREEN   = (   0, 204,   0)
DARKTURQUOISE   = ( 3, 54, 73)

XMARGIN = int((WINDOWWIDTH - (2*BUTTONSIZE)-BUTTONGAPSIZE)/2)
YMARGIN = int((WINDOWHEIGTH - (2*BUTTONSIZE)-BUTTONGAPSIZE)/2)

#设置按钮
YELLOWRECT = pygame.Rect(XMARGIN,YMARGIN,BUTTONSIZE,BUTTONSIZE)
BLUERECT= pygame.Rect(XMARGIN+BUTTONSIZE+BUTTONGAPSIZE,YMARGIN,BUTTONSIZE,BUTTONSIZE)
REDRECT= pygame.Rect(XMARGIN,YMARGIN+BUTTONSIZE+BUTTONGAPSIZE,BUTTONSIZE,BUTTONSIZE)
GREENRECT= pygame.Rect(XMARGIN+BUTTONSIZE+BUTTONGAPSIZE,YMARGIN+BUTTONSIZE+BUTTONGAPSIZE,BUTTONSIZE,BUTTONSIZE)
#临时的全局变量
global FPSCLOCK, DISPLAYSURF, BASICFONT,BEEP1,BEEP2,BEEP3,BEEP4

#复用旧的函数
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

def flashButtonAnimation(color,animationSpeed=50):#实现贴片滑动动画
    if color == YELLOW:
        sound = BEEP1
        flashColor = BRIGHTYELLOW
        rectangle = YELLOWRECT
    elif color == BLUE:
        sound = BEEP2
        flashColor = BRIGHTBLUE
        rectangle = BLUERECT
    elif color == RED:
        sound = BEEP3
        flashColor = BRIGHTRED
        rectangle = REDRECT
    elif color == GREEN:
        sound = BEEP4
        flashColor = BRIGHTGREEN
        rectangle = GREENRECT
    #实现按钮闪烁
    origSurf = DISPLAYSURF.copy()
    flashSurf=pygame.Surface((BUTTONSIZE,BUTTONSIZE))
    flashSurf=flashSurf.convert_alpha()#绘制透明颜色
    r,g,b=flashColor
    sound.play()
    #使得图片变亮然后再变暗
    for start, end,step in ((0,255,1),(255,0,-1)):
        for alpha in range(start,end,step*animationSpeed):
            checkForQuit()
            DISPLAYSURF.blit(origSurf,(0,0))
            flashSurf.fill((r,g,b,alpha))
            DISPLAYSURF.blit(flashSurf,rectangle.topleft)
            pygame.display.update()
            FPSCLOCK.tick(FPS)
    DISPLAYSURF.blit(origSurf,(0,0))
#绘制按钮
def drawButtons():
    pygame.draw.rect(DISPLAYSURF,YELLOW,YELLOWRECT)
    pygame.draw.rect(DISPLAYSURF,BLUE,BLUERECT)
    pygame.draw.rect(DISPLAYSURF,RED,REDRECT)
    pygame.draw.rect(DISPLAYSURF,GREEN,GREENRECT)
#实现背景改变的动画
def changeBackgroundAnimation(animationSpeed=40):
    global bgColor
    newBgColor = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
    newBgSurf=pygame.Surface((WINDOWWIDTH,WINDOWHEIGTH))
    newBgSurf=newBgSurf.convert_alpha()
    r,g,b=newBgColor
    for alpha in range(0,255,animationSpeed):
        checkForQuit()
        DISPLAYSURF.fill(bgColor)
        newBgSurf.fill((r, g, b, alpha))
        DISPLAYSURF.blit(newBgSurf,(0,0))
        drawButtons()
        pygame.display.update()
        FPSCLOCK.tick(FPS)
    bgColor=newBgColor
#结束游戏动画
def gameOverAmination(color=WHITE,animationSpeed=50):
    origSurf = DISPLAYSURF.copy()
    flashSurf=pygame.Surface(DISPLAYSURF.get_size())
    flashSurf=flashSurf.convert_alpha()
    BEEP1.play()
    BEEP2.play()
    BEEP3.play()
    BEEP4.play()
    r,g,b=color
    for i in range(3):
        for start,end,step in ((0,255,1),(255,0,-1)):
            for alpha in range(start,end,animationSpeed*step):
                checkForQuit()
                flashSurf.fill((r, g, b, alpha))
                DISPLAYSURF.bilt(origSurf,(0,0))
                DISPLAYSURF.blit(flashSurf,(0,0))
                drawButtons()
                pygame.display.update()
                FPSCLOCK.tick(FPS)
#将像素坐标转换为按钮
def getButtonClicked(x,y):
    if YELLOWRECT.collidepoint((x,y)):
        return YELLOW
    elif BLUERECT.collidepoint((x,y)):
        return BLUE
    elif REDRECT.collidepoint((x,y)):
        return RED
    elif GREENRECT.collidepoint((x,y)):
        return GREEN
    return None

def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, BEEP1, BEEP2, BEEP3, BEEP4

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGTH))
    pygame.display.set_caption('Simulate')
    BASICFONT = pygame.font.Font('freesansbold.ttf', 16)

    infoSurf = BASICFONT.render('QWAS,Using',1,DARKGRAY)
    infoRect = infoSurf.get_rect()
    infoRect.topleft = (10,WINDOWHEIGTH-25)

    BEEP1=pygame.mixer.Sound('beep1.ogg')
    BEEP2 = pygame.mixer.Sound('beep2.ogg')
    BEEP3 = pygame.mixer.Sound('beep3.ogg')
    BEEP4 = pygame.mixer.Sound('beep4.ogg')

    #局部变量
    pattern = []#记录点击顺序
    currentStep=0#记录必须点击的，如果点错了那么游戏就结束了
    laskClickTime=0#在规定的时间点击结束，否则游戏结束
    score=0#记录分数
    waitingForInput=False
    #绘制游戏板并处理输入
    while True:
        clickedButton=None
        DISPLAYSURF.fill(bgColor)
        drawButtons()
        #在文本中更改输入
        scoreSurf=BASICFONT.render('SCORE: '+ str(score),1,WHITE)
        scoreRect=scoreSurf.get_rect()
        scoreRect.topleft=(WINDOWWIDTH-100,10)
        DISPLAYSURF.blit(scoreSurf,scoreRect)

        DISPLAYSURF.blit(infoSurf,infoRect)
        #检查鼠标点击
        checkForQuit()
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP:
                mousex, mousey =event.pos
                clickedButton = getButtonClicked(mousex,mousey)
            #检查键盘按下
            elif event.type == K_DOWN:
                if event.key == K_q:
                    clickedButton=YELLOW
                elif event.key == K_w:
                    clickedButton=BLUE
                elif event.key == K_a:
                    clickedButton=RED
                elif event.key == K_s:
                    clickedButton=GREEN
        #游戏循环的两种状态
        if not waitingForInput:
            pygame.display.update()
            pygame.time.wait(1000)
            pattern.append(random.choice((YELLOW,BLUE,RED,GREEN)))
            for button in pattern:
                flashButtonAnimation(button)
                pygame.time.wait(FLASHDELAY)
            waitingForInput=True
        else :#判断是不是点对了对的按钮
            if clickedButton and clickedButton ==pattern[currentStep]:
                flashButtonAnimation(clickedButton)
                currentStep +=1
                laskClickTime=time.time()#返回新纪元时间UNIX1970年1月1日到现在经历了多少秒
                if currentStep == len(pattern):
                    changeBackgroundAnimation()
                    score +=1
                    waitingForInput = False
                    currentStep=0
            elif (clickedButton and clickedButton != pattern[currentStep])or(currentStep !=0 and time.time()-TIMEOUT>laskClickTime):
                gameOverAmination()
                pattern = []
                currentStep=0
                waitingForInput=False
                score=0
                pygame.time.wait(1000)
                changeBackgroundAnimation()

        pygame.display.update()
        FPSCLOCK.tick(FPS)

if __name__ == '__main__':
    main()

