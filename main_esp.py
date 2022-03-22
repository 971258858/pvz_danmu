"""
@Author https://github.com/DougTheDruid
@Source https://github.com/DougTheDruid/SoT-ESP-Framework
For community support, please contact me on Discord: DougTheDruid#2784
"""


import pygame
from pvz_hack import PVZMemoryReader
from pygame_helper import PyGameHelper, fuchsia
import win32api
DEBUG = False
COLOR = (255,255,0)
GetAsyncKeyState = win32api.GetAsyncKeyState

if __name__ == '__main__':
    print("F1减速僵尸20秒 F2自动拾取阳光 F6修改阳光2000 F7无限阳光")
    # Initialize our SoT Hack object, and do a first run of reading actors
    # 初始化我们的SoT Hack对象，并进行第一次读取
    smr = PVZMemoryReader()
    done = False
    loops = []
    smr.read_ZombieList()
    # print("smr", smr.run_info)
    # We only want to make the PyGame resources if we aren't running in Debug
    # mode (otherwise we will get a black screen during debug)
    # 我们只想在没有在Debug中运行的情况下生成PyGame资源模式（否则调试时会出现黑屏）
    if not DEBUG:
        pgh = PyGameHelper()

    # 缩放比例
    proportion_x = (pgh.windows_area[2] - pgh.windows_area[0]) / 785
    proportion_y = (pgh.windows_area[3] - pgh.windows_area[1] - 60) / 560

    # 循环获取数据渲染
    while not done:
        smr.read_ZombieList()

        if not DEBUG:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # pylint: disable=no-member
                    done = True

        if not DEBUG:

            if (GetAsyncKeyState(0x75) & 0x8000):  # 'F6' key
                # 修改阳光:
                smr.set_mysun(2000)

            if (GetAsyncKeyState(0x76) & 0x8000):  # 'F7' key
                # 无限阳光:
                smr.change_memory()

            if (GetAsyncKeyState(0x70) & 0x8000):  # 'F1' key
                # 减速场上僵尸:
                smr.change_state(2000)

            if (GetAsyncKeyState(0x71) & 0x8000):  # 'F2' key
                # 自动拾取阳光
                smr.auto_pickup()
            if (GetAsyncKeyState(0x72) & 0x8000):  # 'F3' key
                # 阳光加速掉落5秒
                smr.set_mysuntime()
            # Fill the screen with the transparent color we set in PyGameHelper
            # 用我们在PyGameHelper中设置的透明颜色填充屏幕
            pgh.screen.fill(fuchsia)

            # If there is actor data from read_actors(), display the info
            # to screen
            # 如果有来自read_actors（）的actor数据，则将信息显示到屏幕
            if smr.run_info:
                for actor in smr.run_info:
                    # print("actor", actor)
                    # 显示僵尸数量
                    # pgh.screen.blit(pgh.my_font.render('ALL:' + str(smr.zombie_num), False, COLOR),
                    #                 (pgh.windows_area[2] - pgh.windows_area[0] - 60, 40))
                    pgh.screen.blit(pgh.my_font.render('Now_Zombie:' + str(smr.zombie_now_num), False, COLOR),
                                    (pgh.windows_area[2] - pgh.windows_area[0] - 110, 40))
                    # if actor['状态'] == 0 and actor['是否魅惑'] != 65536:
                    if actor['当前血量']:
                        # 计算实际屏幕坐标
                        position = (actor.get('X坐标') + 35)*proportion_x, (actor.get('Y坐标')+60)*proportion_y
                        # print("position", position)
                        # pygame.draw.circle(pgh.screen, COLOR, position, 10)
                        pygame.draw.rect(pgh.screen, COLOR, [position[0] - 25, position[1]-45, 57, 120], 1)
                        if actor.get('血量上限'):
                            pygame.draw.rect(pgh.screen, (255,0,0), [position[0] + 35, position[1]-45, 3, 120*(actor.get('当前血量') / actor.get('血量上限'))], 0)
                        # pgh.screen.blit(pgh.my_font.render('health:' + str(actor.get('当前血量')), False, COLOR),
                        #                 (position[0] - 20, position[1]+75))
                        # pgh.screen.blit(pgh.my_font.render('display:' + str(actor.get('是否可见')), False, COLOR),
                        #                 (position[0] - 20, position[1] + 75))
                        # pgh.screen.blit(pgh.my_font.render('state:' + str(actor.get('神秘消失')), False, COLOR),
                        #                 (position[0] - 20, position[1] + 92))
                        # if actor.get('冰冻时间'):
                        #     pgh.screen.blit(pgh.my_font.render('debuff:' + str(actor.get('冰冻时间')), False, COLOR),
                        #                     (position[0] - 20, position[1] + 109))
                        # pgh.screen.blit(pgh.my_font.render(str(int(actor.get('X坐标'))), False, COLOR),
                        #                 (position[0] + 40, position[1] - 10))
            pygame.display.update()
