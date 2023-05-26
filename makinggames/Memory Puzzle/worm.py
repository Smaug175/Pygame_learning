# 这是一个示例 Python 脚本。
import pygame, sys
from pygame.locals import *

# 按 Shift+F10 执行或将其替换为您的代码。
# 按 双击 Shift 在所有地方搜索类、文件、工具窗口、操作和设置。

pygame.init()
# 创建一个对象Surface
screen = pygame.display.set_mode((500, 400), 0, 32)
pygame.display.set_caption('hellow')

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    pygame.display.update()
