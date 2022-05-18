
import asyncio
import time
from util.pvz_hack import PVZMemoryReader
import danmaku
from danmu_analyse import Analyse
# 直播间信息
up_name = "丑皇今天不加班"
up_roomid = "3502000"
# 可召唤僵尸类型列表
zombie_type_list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 14, 15, 16, 17, 18, 19, 20, 21, 23, 24]
# 僵尸类型对应的花费
zombie_sum_list = {"0": 100, "1": 100, "2": 150, "3": 150, "4": 200, "5": 150, "6": 200, "7": 200,
                   "8": 250, "9": 100, "10": 100, "11": 150, "12": 300, "13": 150, "14": 150, "15": 150,
                   "16": 150, "17": 250, "18": 200, "19": 0, "20": 150, "21": 150, "22": 300, "23": 400,
                   "24": 50, "25": 5000}
async def printer(q):
    mr = PVZMemoryReader()
    mr.auto_pickup()  # 开启自动拾取
    while True:
        m = await q.get()
        # 部分文字被过滤掉了，猜测是danmuku过滤掉了，需要排查
        if m['msg_type'] == 'danmaku':
            # print(f'{m["name"]}：{m["content"]}')
            Analyse(up_name, m["name"], m["content"], zombie_type_list, zombie_sum_list)
async def main(url):
    q = asyncio.Queue()
    dmc = danmaku.DanmakuClient(url, q)
    asyncio.create_task(printer(q))
    await dmc.start()


# a = input('请输入直播间地址：\n')
a = "https://live.bilibili.com/" + up_roomid
print("开始监听直播间:", a)
asyncio.run(main(a))
