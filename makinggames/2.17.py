# 这是一个示例 Python 脚本。
import pygame, sys
from pygame.locals import *

# 按 Shift+F10 执行或将其替换为您的代码。
# 按 双击 Shift 在所有地方搜索类、文件、工具窗口、操作和设置。

pygame.init()
# 创建一个对象Surface

FPS = 60
fpsClock = pygame.time.Clock()


screen = pygame.display.set_mode((400,300), 0, 32)
pygame.display.set_caption('AN')

white = (255,255,255,255)
catImg = pygame.image.load('cat.png')
catx = 10
caty = 10
direction = 'right'


while True:
    screen.fill(white)

    if direction == 'right':
        catx += 5
        if catx == 280:
            direction = 'down'
    if direction == 'down':
        caty += 5
        if caty == 220:
            direction = 'left'
    if direction == 'left':
        catx -= 5
        if catx == 10:
            direction = 'up'
    if direction == 'up':
        caty -= 5
        if caty == 10:
            direction = 'right'

    screen.blit(catImg,(catx,caty))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    pygame.display.update()
    fpsClock.tick(FPS)
