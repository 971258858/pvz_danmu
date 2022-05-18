import re
import random
from util.shellcode_helper import ZombieCall
from util.pvz_hack import PVZMemoryReader
# 初始化玩家列表
player_list = []
class Analyse:
    """
    初始化函数，内含初始化必要数据和弹幕的主要判断逻辑
    :param up_name: up主的昵称
    :param name: 弹幕发送者的昵称
    :param data: 弹幕发送的内容
    :param mr: 修改游戏的工具类
    :param zombie_type_list: 可以召唤的怪物列表
    :param zombie_sum_list: 怪物消耗阳光的数据表
    """
    def __init__(self, up_name, name, data, zombie_type_list, zombie_sum_list):
        # 初始化工具类
        self.mr = PVZMemoryReader()
        # 初始化阳光
        self.now_mysun = int(self.mr.get_mysun())
        # 初始化僵尸数据
        self.zombie_type_list = zombie_type_list
        self.zombie_sum_list = zombie_sum_list
        # 初始化弹幕数据
        self.data = data.strip()
        self.name = name
        number_list = re.findall(r"\d+", self.data)
        # print(self.data)

        """ ----------------弹幕判断逻辑在这里写---------------- """
        # 加入游戏
        if self.data == '加入':
            if self.player_judge() == 0:
                player_list.append(self.name)
                self.join_Game()
        # 赠送礼物，需要配合弹幕姬插件(自动回复：感谢XXX的X个XX）
        if self.data[0:2] == '感谢' and len(number_list) > 0:
            if self.name == up_name:
                gifts_num = int(number_list[len(number_list) - 1])
                temp = 25 * gifts_num
                name = self.data[2:self.data.index('的')]
                self.gift_feedback(name, temp)
        # 召唤僵尸
        if self.player_judge() == 1:
            if self.data[0:2] == '召唤' and len(number_list) > 0:
                if number_list[0] == '20' and len(number_list) == 3:
                    self.join_Zombie(number_list[2], number_list[1], number_list[0])
                elif len(number_list) == 2:
                    self.join_Zombie(9, number_list[1], number_list[0])
                elif len(number_list) == 1:
                    self.join_Zombie(9, random.randint(0, 4), number_list[0])
        elif self.data[0:2] == '召唤' and len(number_list) > 0:
            print(self.name, "请先输入'加入'才能召唤~")
        """ ----------------主要判断逻辑在这里写---------------- """

    """
    判断是否在玩家列表(可以优化下，这样判断增加一个玩家就增加了一次判断循环)
    """
    def player_judge(self):
        for item in player_list:
            if self.name == item:
                return 1
        return 0

    """
    加入游戏对游戏执行的操作
    """
    def join_Game(self):
        ZombieCall(random.randint(0, 4), 9, 1)
        print(self.name, "加入到游戏~自动召唤一只旗子僵尸")

    """
    赠送礼物对游戏执行的操作
    :param number: 用户昵称
    :param number: 增加的阳光数量
    """
    def gift_feedback(self, name, number):
        now_sun = self.now_mysun + int(number)
        self.mr.set_mysun(now_sun)
        print("感谢", name, "赠送的", number, "个阳光，目前阳光：", now_sun)

    """
    赠送礼物对游戏执行的操作
    :param x: 召唤僵尸的x坐标
    :param y: 召唤僵尸的y坐标
    :param z_type: 召唤僵尸的类型
    """
    def join_Zombie(self, x, y, z_type):
        if self.now_mysun < int(self.zombie_sum_list[z_type]):
            print(self.name, "阳光不足，可以赠送任意礼物增加阳光")
            return
        if int(y) in range(5):
            if int(z_type) in self.zombie_type_list:
                nowsun = self.now_mysun - int(self.zombie_sum_list[z_type])
                if nowsun < 50:
                    ZombieCall(random.randint(0, 4), 9, 1)
                    print("阳光快没了~", nowsun)
                ZombieCall(y, x, z_type)
                self.mr.set_mysun(nowsun)
                print(self.name, "召唤成功~花费了", self.zombie_sum_list[z_type])
            else:
                print(self.name, "编号", z_type, "的僵尸目前关卡不可召唤")
        else:
            print(self.name, "您输入的行数为", y, "请输入0~4")
