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

roomid = "3502000"

class Danmu():
    def __init__(self):
        # 可召唤僵尸类型列表
        self.zombie_type_list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 17, 19, 20, 21, 24, 25]
        self.zombie_sum_list = {"0": 100, "1": 100, "2": 150, "3": 150, "4": 200, "5": 150, "6": 200, "7": 200, "8": 250, "9": 100, "10": 100, "11": 150, "12": 300, "13": 150, "14": 150, "15": 150, "16": 150, "17": 250, "18": 200, "19": 0, "20": 150, "21": 150, "22": 300, "23": 400, "24": 50, "25": 5000}
        # 弹幕url
        self.url = 'https://api.live.bilibili.com/xlive/web-room/v1/dM/gethistory'
        # 请求头
        self.agent_num = 0
        self.headers = {
            'Host': 'api.live.bilibili.com',
            'Origin': 'bilibili.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.' + str(self.agent_num),
        }
        # 定义POST传递的参数
        self.data = {
            'roomid': roomid,
            'csrf_token': '',
            'csrf': '',
            'visit_id': '',
        }
        # 读取日志

        self.integral_file = open('integral.txt', mode='r+', encoding='utf-8')
        # 日志写对象
        self.log_file_write = open('danmu.log', mode='a+', encoding='utf-8')
        self.log = self.log_file_write.readlines()
        self.integral = self.integral_file.readlines()
        # print(self.integral)

    def get_danmu(self, isInit = 0):
        # 获取直播间弹幕
        proxies = {
            'http': '221.176.14.72:80',
            'https': '118.244.239.2:3228'
        }
        self.agent_num += 1
        self.headers = {
            'Host': 'api.live.bilibili.com',
            'Origin': 'bilibili.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.' + str(self.agent_num),
        }
        print(self.agent_num)
        try:
            html = requests.post(url=self.url, headers=self.headers, data=self.data, timeout=6).json()
        except:
            print("请求超时")
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
                # 加入增加阳光
                if text == '加入':
                    i = 0
                    for item in self.integral:
                        if nickname == item:
                            return
                        i += 1
                    self.integral.append(nickname)
                    self.integral[0] = str(int(self.integral[0]) + 1000)
                    self.integral_file.seek(0)
                    self.integral_file.write(self.list_to_str(self.integral))
                    self.integral_file.close()
                    self.integral_file = open('integral.txt', mode='r+', encoding='utf-8')
                    print(nickname, "加入成功！")
                # 礼物
                if len(text.split("个辣条")) > 1:
                    if nickname == "丑皇今天不加班":
                        gifts_num = re.findall(r"\d+", text)
                        temp = 25*int(gifts_num[len(gifts_num) - 1])
                        self.integral[0] = str(int(self.integral[0]) + temp)
                        self.integral_file.seek(0)
                        self.integral_file.write(self.list_to_str(self.integral))
                        self.integral_file.close()
                        self.integral_file = open('integral.txt', mode='r+', encoding='utf-8')
                        print("感谢", nickname, "增加了", temp, "个脑光")
                    return
                if len(text.split("谢谢")) > 1:
                    if nickname == "丑皇今天不加班":
                        gifts_num = re.findall(r"\d+", text)
                        temp = 100*int(gifts_num[len(gifts_num) - 1])
                        self.integral[0] = str(int(self.integral[0]) + temp)
                        self.integral_file.seek(0)
                        self.integral_file.write(self.list_to_str(self.integral))
                        self.integral_file.close()
                        self.integral_file = open('integral.txt', mode='r+', encoding='utf-8')
                        print("感谢", nickname, "增加了", temp, "个脑光")
                    return
                # 召唤僵尸
                # 蜘蛛僵尸
                if len(text.split("召唤僵尸20")) > 1:
                    call_type = re.findall(r"\d+", text.split("召唤僵尸20")[1])
                    if len(call_type) > 1:
                        i = 0
                        for item in self.integral:
                            if nickname == item:
                                if int(self.integral[0]) < self.zombie_sum_list["20"]:
                                    print(item.split(":")[0], "脑光不足")
                                    return
                                now_integral = str(int(self.integral[0]) - self.zombie_sum_list["20"])
                                self.integral[0] = now_integral
                                self.integral_file.seek(0)
                                self.integral_file.write(self.list_to_str(self.integral))
                                ZombieCall(int(call_type[0]), int(call_type[1]), 20)
                                print(item, " 蜘蛛召唤成功，剩余脑光：", now_integral)
                                return
                            i += 1
                # 随机行出现
                if len(text.split("召唤僵尸")) > 1:
                    call_type = re.findall(r"\d+", text)
                    if len(call_type) == 1:
                        if int(call_type[0]) in self.zombie_type_list:
                            i = 0
                            for item in self.integral:
                                if nickname == item:
                                    if int(self.integral[0]) < self.zombie_sum_list[text.split("召唤僵尸")[1][0]]:
                                        print(item, "脑光不足")
                                        return
                                    now_integral = str(int(self.integral[0]) - self.zombie_sum_list[call_type[0]])
                                    self.integral[0] = now_integral
                                    self.integral_file.seek(0)
                                    self.integral_file.write(self.list_to_str(self.integral))
                                    ZombieCall(random.randint(0, 4), 10, int(call_type[0]))
                                    print(item, "随机召唤成功，剩余脑光：", now_integral)
                                    return
                                i += 1
                    # # 指定行出现
                    if len(call_type) == 2:
                        if int(call_type[0]) in self.zombie_type_list and int(call_type[1]) in range(5):
                            i = 0
                            for item in self.integral:
                                if nickname == item:
                                    if int(self.integral[0]) < self.zombie_sum_list[text.split("召唤僵尸")[1][0]]:
                                        print(item, "脑光不足")
                                        return
                                    now_integral = str(int(self.integral[0]) - self.zombie_sum_list[call_type[0]])
                                    self.integral[0] = now_integral
                                    self.integral_file.seek(0)
                                    self.integral_file.write(self.list_to_str(self.integral))
                                    ZombieCall(int(call_type[1]), 10, int(call_type[0]))
                                    print(item, "指定召唤成功，剩余脑光：", now_integral)
                                    return
                                i += 1
            # 清空变量缓存
            nickname = ''
            text = ''
            timeline = ''
            msg = ''

    def list_to_str(self, list):
        mystr=""
        for item in list:
            if item != "\n":
                mystr += item + '\n'
        return mystr

if __name__ == '__main__':
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
