# pvz_eap_hack
一、python版本：

python版本3.7.9（版本不一致可能导致读写文件的差异）

其他依赖可以根据文件头部引用自己安装，pygame需要手动安装对应版本


二、描述：

未连接数据库，暂时用本地文件存储。

danmu.log存储弹幕信息；

integral.txt存储积分和用户信息。


三、使用方法：

单独弹幕互动模式：python test.py（修改文件头部参数roomid为你要监听的直播间号） 

单独ESP的作弊模式：python main_esp.py

带ESP的互动模式：python main_bili_esp.py（修改文件头部参数roomid为你要监听的直播间号） 


四、目前维护版本：

test.py可能有些bug没有修复，需要自己调试下。

main_bili_esp.py是目前在维护的文件，目前还有部分小bug有待修复。
