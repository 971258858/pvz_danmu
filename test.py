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

class Danmu():
    def __init__(self):
        # 可召唤僵尸类型列表
        self.zombie_type_list = [0, 1, 2, 4, 5, 6]
        self.zombie_sum_list = {"0": 100, "1": 100, "2": 200, "4": 400, "5": 600, "6": 800}
        # 弹幕url
        self.url = 'https://api.live.bilibili.com/xlive/web-room/v1/dM/gethistory'
        # 请求头
        self.headers = {
            'Host': 'api.live.bilibili.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0',
        }
        # 定义POST传递的参数
        self.data = {
            'roomid': '3502000',
            'csrf_token': '',
            'csrf': '',
            'visit_id': '',
        }
        # 读取日志

        self.integral_file = open('integral.txt', mode='r+', encoding='utf-8')
        # 日志写对象
        self.log_file_write = open('danmu.log', mode='a', encoding='utf-8')
        log_file_read = open('danmu.log', mode='r', encoding='utf-8')
        self.log = log_file_read.readlines()
        self.integral = self.integral_file.readlines()
        print(self.integral)
    def get_danmu(self, isInit = 0):
        # 获取直播间弹幕
        html = requests.post(url=self.url, headers=self.headers, data=self.data).json()
        # 解析弹幕列表
        for content in html['data']['room']:
            # 获取昵称
            nickname = content['nickname']
            # 获取发言
            text = content['text']
            # 获取发言时间
            timeline = content['timeline']
            # 记录发言
            msg = timeline + ' ' + nickname + ': ' + text
            # 判断对应消息是否存在于日志，如果和最后一条相同则打印并保存
            if msg + '\n' not in self.log:
                # 打印消息
                print(msg)
                # 保存日志
                self.log_file_write.write(msg + '\n')
                # 添加到日志列表
                self.log.append(msg + '\n')
                # 初始化数据
                if isInit == 1:
                    continue
                # 签到领取阳光
                if text == '领取阳光':
                    i = 0
                    for item in self.integral:
                        if nickname == item.split(":")[0]:
                            self.integral[i] = item.split(":")[0] + ":" + str(int(item.split(":")[1])+1000)
                            self.integral_file.seek(0)
                            self.integral_file.write(self.list_to_str(self.integral))
                            return
                        i += 1
                    self.integral.append(nickname + ':1000')
                    self.integral_file.write(self.list_to_str(self.integral))
                # 召唤僵尸
                if len(text.split("召唤僵尸")) > 1:
                    if int(text.split("召唤僵尸")[1][0]) in self.zombie_type_list:
                        i = 0
                        for item in self.integral:
                            if nickname == item.split(":")[0]:
                                if int(item.split(":")[1]) < self.zombie_sum_list[text.split("召唤僵尸")[1][0]]:
                                    print("阳光不足")
                                    return
                                self.integral[i] = item.split(":")[0] + ":" + str(int(item.split(":")[1]) - self.zombie_sum_list[text.split("召唤僵尸")[1][0]])
                                self.integral_file.seek(0)
                                self.integral_file.write(self.list_to_str(self.integral))
                                ZombieCall(random.randint(0, 4), 10, int(text.split("召唤僵尸")[1][0]))
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
            mystr += '\n'+ item
        return mystr

if __name__ == '__main__':
    # 创建bDanmu实例
    bDanmu = Danmu()
    # bDanmu.get_danmu(1)
    # time.sleep(10)
    # print("开始监听！")
    while True:
        # 暂停0.5防止cpu占用过高
        time.sleep(1)
        # 获取弹幕
        bDanmu.get_danmu()
