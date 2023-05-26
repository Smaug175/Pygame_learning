# 这是一个示例 Python 脚本。
import time

import pygame, sys
from pygame.locals import *

# 按 Shift+F10 执行或将其替换为您的代码。
# 按 双击 Shift 在所有地方搜索类、文件、工具窗口、操作和设置。

pygame.init()
# 创建一个对象Surface
screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption('hellow')

white = (255,255,255)
GREEN = (0,255,255)
BLUE = (0,0,255)

fontObj = pygame.font.SysFont("华文中宋",32)
textSurfaceObj = fontObj.render('hellow world', True ,GREEN,BLUE)#字体颜色，背景颜色
texeRectObj = textSurfaceObj.get_rect()
texeRectObj.center = (200,150)
soundObj = pygame.mixer.Sound('badswap.wav')


while True:
    screen.fill(white)
    screen.blit(textSurfaceObj,texeRectObj)
    soundObj.play()
    time.sleep(2)
    soundObj.stop()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    pygame.display.update()
