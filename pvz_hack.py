"""
@Author https://github.com/DougTheDruid
@Source https://github.com/DougTheDruid/SoT-ESP-Framework
For community support, please contact me on Discord: DougTheDruid#2784
"""


from memory_helper import ReadMemory

class PVZMemoryReader:
    def __init__(self):
        self.run_info = []

        self.rm = ReadMemory("PlantsVsZombies.exe")
        base_address = self.rm.base_address
        # print('base_address', base_address)

        offset1 = self.rm.read_ulong(base_address + 0x2A9EC0)
        # print("offset1", offset1)
        self.offset2 =self.rm.read_ulong(offset1 + 1896)
        # print("offset2", offset2)


    def read_ZombieList(self):
        self.run_info = []
        # 本局僵尸总数
        self.zombie_num = self.rm.read_int(self.offset2 + 148)
        self.zombie_now_num = self.rm.read_int(self.offset2 + 160)
        # print("本局僵尸总数：", self.zombie_num)

        for index in range(self.zombie_num):
            # 僵尸实体，后面的+348是下一个僵尸
            zombie_entity = self.rm.read_ulong(self.offset2 + 144) + 348 * index
            # print("zombie_entity", zombie_entity)
            zombie_attribute = {
                '怪物大小': self.rm.read_float(zombie_entity + 284),  # 初始1
                '神秘消失': self.rm.read_ulong(zombie_entity + 236),
                '血量上限': self.rm.read_ulong(zombie_entity + 204),
                '当前血量': self.rm.read_ulong(zombie_entity + 200),
                '是否魅惑': self.rm.read_ulong(zombie_entity + 184),  # 不等于65536时魅惑
                '冰冻时间': self.rm.read_ulong(zombie_entity + 172),
                'Y坐标': self.rm.read_float(zombie_entity + 48),
                'X坐标': self.rm.read_float(zombie_entity + 44),
                '状态': self.rm.read_ulong(zombie_entity + 40),  # 0为正常 1为消失 2为变黑 3为秒杀
                '是否可见': self.rm.read_ulong(zombie_entity + 24),
                '图像Y坐标': self.rm.read_ulong(zombie_entity + 12),
                '图像X坐标': self.rm.read_ulong(zombie_entity + 8),

            }
            # print(zombie_attribute)
            self.run_info.append(zombie_attribute)
        # print(self.run_info)
