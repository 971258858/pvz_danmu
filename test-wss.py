import websocket
from threading import Thread
import time
import sys


def on_message(ws, message):
    print("接收了：",message)


def on_error(ws, error):
    print(error)


def on_close(ws):
    print("### closed ###")


def on_open(ws):
    def run(*args):
        room_id = 3502000
        json = {
            "uid": 0,
            "roomid": room_id,
            "protover": 1,
            "platform": "web",
            "clientver": "1.4.0"
        }

        ws.send("Hello")
        time.sleep(1)
        ws.close()
        print("Thread terminating...")

    Thread(target=run).start()


if __name__ == "__main__":
    websocket.enableTrace(True)
    host = "ws://82.157.123.54:9010/ajaxchattest"
    ws = websocket.WebSocketApp(host,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()