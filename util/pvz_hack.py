import time
from .memory_helper import ReadMemory

class PVZMemoryReader:
    def __init__(self):
        self.run_info = []
        self.rm = ReadMemory("PlantsVsZombies.exe")
        base_address = self.rm.base_address
        offset1 = self.rm.read_ulong(base_address + 0x2A9EC0)
        self.offset2 =self.rm.read_ulong(offset1 + 1896)

        # 本局阳光
        self.sun = self.rm.read_int(self.offset2 + 21856)
        # print("阳光数：", self.sun)

        # 本局僵尸总数
        self.zombie_num = self.rm.read_int(self.offset2 + 148)
        self.zombie_now_num = self.rm.read_int(self.offset2 + 160)
        # print("本局僵尸总数：", self.zombie_num)

    def read_ZombieList(self):
        self.run_info = []
        for index in range(self.zombie_num):
            # 本局阳光
            self.sun = self.rm.read_int(self.offset2 + 21856)
            # print("阳光数：", self.sun)

            # 本局僵尸总数
            self.zombie_num = self.rm.read_int(self.offset2 + 148)
            self.zombie_now_num = self.rm.read_int(self.offset2 + 160)
            # print("本局僵尸总数：", self.zombie_num)

            # 僵尸实体，后面的+348是下一个僵尸
            zombie_entity = self.rm.read_ulong(self.offset2 + 144) + 348 * index
            # print("zombie_entity", zombie_entity)
            zombie_attribute = {
                '怪物基址': zombie_entity,
                # '怪物大小': self.rm.read_float(zombie_entity + 284),  # 初始1
                # '神秘消失': self.rm.read_ulong(zombie_entity + 236),
                '血量上限': self.rm.read_ulong(zombie_entity + 204),
                '当前血量': self.rm.read_ulong(zombie_entity + 200),
                # '是否魅惑': self.rm.read_ulong(zombie_entity + 184),  # 不等于65536时魅惑
                # '冰冻时间': self.rm.read_ulong(zombie_entity + 172),
                'Y坐标': self.rm.read_float(zombie_entity + 48),
                'X坐标': self.rm.read_float(zombie_entity + 44),
                # '状态': self.rm.read_ulong(zombie_entity + 40),  # 0为正常 1为消失 2为变黑 3为秒杀
                # '是否可见': self.rm.read_ulong(zombie_entity + 24),
                # '图像Y坐标': self.rm.read_ulong(zombie_entity + 12),
                # '图像X坐标': self.rm.read_ulong(zombie_entity + 8),
            }
            # print(zombie_attribute)
            self.run_info.append(zombie_attribute)
        # print(self.run_info)

    def set_mysun(self, changenum: int):
        if self.sun != 6646952:
            self.rm.set_int(self.offset2 + 21856, changenum)

    def change_memory(self):
        self.rm.set_bytes(self.rm.base_address + 0x1BA76, 1, 1)
        print("无限阳光修改成功！")

    def change_state(self, changenum: int):
        for zombie in self.run_info:
            self.rm.set_int(zombie.get('怪物基址') + 172, changenum)
        print("减速20秒成功！")

    def auto_pickup(self):
        self.rm.set_bytes(self.rm.base_address + 0x3158F, 1, 235)
        print("自动拾取修改成功！")

    def set_mysuntime(self):
        for i in range(25):
            self.rm.set_int(self.offset2 + 21816, 1)
            time.sleep(0.2)
        print("阳光掉落速度加快5秒修改成功！")
    def get_mysun(self):
        return self.sun
