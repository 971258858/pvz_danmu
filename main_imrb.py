"""
    获取bilibili直播间弹幕
    房间号从网页源代码中获取
    打开直播画面后，按ctrl+u 打开网页源代码，按ctrl+f 搜索 room_id
    搜到的"room_id":1016中，1016就是房间号
    获取不同房间的弹幕:修改代码第26行的roomid的值为对应的房间号
"""
import random
import requests
import time
from zhuru import ZombieCall
import re
import pygame
from pvz_hack import PVZMemoryReader
from pygame_helper import PyGameHelper, fuchsia
import win32api
from fake_useragent import UserAgent

DEBUG = False
COLOR = (255, 255, 0)
GetAsyncKeyState = win32api.GetAsyncKeyState

roomid = "3502000"

class Danmu():
    def __init__(self):
        # 可召唤僵尸类型列表
        self.zombie_type_list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 14, 15, 16, 17, 18, 19, 20, 21, 23, 24]
        self.zombie_sum_list = {"0": 100, "1": 100, "2": 150, "3": 150, "4": 200, "5": 150, "6": 200, "7": 200, "8": 250, "9": 100, "10": 100, "11": 150, "12": 300, "13": 150, "14": 150, "15": 150, "16": 150, "17": 250, "18": 200, "19": 0, "20": 150, "21": 150, "22": 300, "23": 400, "24": 50, "25": 5000}
        # 弹幕url
        self.url = 'https://api.live.bilibili.com/xlive/web-room/v1/dM/gethistory'
        # 请求头
        self.headers = {
            'Host': 'api.live.bilibili.com',
            'Origin': 'bilibili.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.50'
        }
        # 定义POST传递的参数
        self.data = {
            'roomid': roomid,
            'csrf_token': '',
            'csrf': '',
            'visit_id': '',
        }
        # 读取日志


        # 日志写对象
        self.log_file_write = open('danmu.log', mode='a+', encoding='utf-8')
        self.integral_file = open('integral_imrb.txt', mode='r+', encoding='utf-8')
        self.log = open('danmu.log', mode='r', encoding='utf-8').readlines()
        self.integral = self.integral_file.readlines()


    def get_danmu(self, isInit = 0):
        # 获取直播间弹幕
        proxies = {
            'http': '221.176.14.72:80',
            'https': '118.244.239.2:3228'
        }
        ua = UserAgent().random
        # print(ua)
        self.headers = {
            'Host': 'api.live.bilibili.com',
            'Origin': 'bilibili.com',
            'User-Agent': ua
        }
        try:
            html = requests.post(url=self.url, headers=self.headers, data=self.data, timeout=6).json()
        except:
            print("请求超时,请稍等几秒")
            return
        # print(html)
        # 解析弹幕列表
        for content in html['data']['room']:
            # 获取昵称
            nickname = content['nickname']
            # 获取发言
            text = content['text']
            # 获取发言时间
            timeline = content['timeline']
            # 记录发言
            msg = timeline + ' ' + nickname + ':' + text
            # 判断对应消息是否存在于日志，如果和最后一条相同则打印并保存
            if msg + '\n' not in self.log:
                # 打印消息
                # print(msg)
                # 保存日志
                self.log_file_write.write(msg + '\n')
                # 添加到日志列表
                self.log.append(msg + '\n')
                # 初始化数据
                if isInit == 1:
                    continue
                # 初始化阳光
                now_mysun = smr.get_mysun()
                # 加入增加阳光
                if text == '加入':
                    i = 0
                    for item in self.integral:
                        if nickname.strip() == item:
                            return
                        i += 1
                    self.integral.append(nickname.strip())
                    ZombieCall(random.randint(0, 4), 10, 1)
                    self.integral_file.seek(0)
                    self.integral_file.write(self.list_to_str(self.integral))
                    self.integral_file.close()
                    self.integral_file = open('integral_imrb.txt', mode='r+', encoding='utf-8')
                    print(nickname, "加入成功！自动召唤一个小旗子僵尸~互动看顶部例子")
                # 礼物
                if len(text.split("个辣条")) > 1:
                    if nickname.strip() == "丑皇今天不加班":
                        gifts_num = re.findall(r"\d+", text)
                        temp = 25*int(gifts_num[len(gifts_num) - 1])
                        smr.set_mysun(int(now_mysun) + temp)
                        print("感谢辣条", nickname, "增加了", temp, "个阳光")
                    return
                if len(text.split("谢谢")) > 1:
                    if nickname.strip() == "丑皇今天不加班":
                        gifts_num = re.findall(r"\d+", text)
                        temp = 100*int(gifts_num[len(gifts_num) - 1])
                        smr.set_mysun(int(now_mysun) + temp)
                        print("感谢礼物", nickname, "增加了", temp, "个阳光")
                    return
                # 召唤僵尸
                # 蜘蛛僵尸
                if len(text.split("召唤僵尸20")) > 1:
                    call_type = re.findall(r"\d+", text.split("召唤僵尸20")[1])
                    if len(call_type) > 1:
                        i = 0
                        for item in self.integral:
                            if (nickname.strip() == item) or (nickname.strip() + "\n" == item):
                                if int(now_mysun) < self.zombie_sum_list["20"]:
                                    print(nickname, "阳光不足，可以赠送辣条增加阳光")
                                    return
                                now_integral = str(int(now_mysun) - self.zombie_sum_list["20"])
                                ZombieCall(int(call_type[0]), int(call_type[1]), 20)
                                smr.set_mysun(int(now_integral) + 25)
                                print(nickname, " 蜘蛛召唤成功，剩余阳光：", str(int(now_integral) + 25))
                                return
                            i += 1
                # 随机行出现
                if len(text.split("召唤僵尸")) > 1:
                    call_type = re.findall(r"\d+", text)
                    if len(call_type) == 1:
                        if int(call_type[0]) in self.zombie_type_list:
                            for item in self.integral:
                                if (nickname.strip() == item) or (nickname.strip() + "\n" == item):
                                    if int(now_mysun) < self.zombie_sum_list[str(int(call_type[0]))]:
                                        print(nickname, "阳光不足，可以赠送辣条增加阳光")
                                        return
                                    now_integral = str(int(now_mysun) - self.zombie_sum_list[str(int(call_type[0]))])
                                    ZombieCall(random.randint(0, 4), 5, int(call_type[0]))
                                    smr.set_mysun(int(now_integral) + 25)
                                    print(nickname, "随机召唤成功，剩余阳光：", str(int(now_integral) + 25))
                                    return
                    # # 指定行出现
                    if len(call_type) == 2:
                        if int(call_type[0]) in self.zombie_type_list and int(call_type[1]) in range(5):
                            for item in self.integral:
                                if (nickname.strip() == item) or (nickname.strip() + "\n" == item):
                                    print(str(int(call_type[0])))
                                    if int(now_mysun) < self.zombie_sum_list[str(int(call_type[0]))]:
                                        print(nickname, "阳光不足，可以赠送辣条增加阳光")
                                        return
                                    now_integral = str(int(now_mysun) - self.zombie_sum_list[str(int(call_type[0]))])

                                    ZombieCall(int(call_type[1]), 5, int(call_type[0]))
                                    smr.set_mysun(int(now_integral) + 25)
                                    print(nickname, "指定召唤成功，剩余阳光：", str(int(now_integral) + 25))
                                    return

            # 清空变量缓存
            self.log_file_write.close()
            self.log_file_write = open('danmu.log', mode='a+', encoding='utf-8')
            nickname = ''
            text = ''
            timeline = ''
            msg = ''

    def list_to_str(self, list):
        mystr=""
        for item in list:
            item = str(item)
            if item != "\n":
                mystr += item + '\n'
        return mystr

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
    # 创建bDanmu实例
    bDanmu = Danmu()
    # 初始化弹幕数据
    # bDanmu.get_danmu(1)
    # time.sleep(3)
    print("开始监听！")
    while True:
        # 暂停3s防止cpu占用过高
        time.sleep(1)
        # 获取弹幕
        bDanmu.get_danmu()

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
                        position = (actor.get('X坐标') + 35) * proportion_x, (actor.get('Y坐标') + 60) * proportion_y
                        # print("position", position)
                        # pygame.draw.circle(pgh.screen, COLOR, position, 10)
                        pygame.draw.rect(pgh.screen, COLOR, [position[0] - 25, position[1] - 45, 57, 120], 1)
                        if actor.get('血量上限'):
                            pygame.draw.rect(pgh.screen, (255, 0, 0), [position[0] + 35, position[1] - 45, 3,
                                                                       120 * (actor.get('当前血量') / actor.get('血量上限'))],
                                             0)
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
                        #                 (position[0] - 110, position[1] - 10))
                        # pgh.screen.blit(pgh.my_font.render(str(int(actor.get('Y坐标'))), False, COLOR),
                        #                 (position[0] - 110, position[1] - 50))
            pygame.display.update()
