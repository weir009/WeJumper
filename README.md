# WeJumper
A python script, use "pygame + adb" to control WeChat  mini-program "Jump".

微信小程序“跳一跳”的外挂，需要Android手机，在PC上控制，理论上PyGame支持的平台都可以。

“跳一跳”这个小程序玩起来实在上瘾，为了戒瘾，花了一个多小时写了个程序半自动地玩，从此想要多少分就可以多少分了，也就不再惦记玩了。


# 前置条件
* Android手机
* 有adb工具可以连接到手机（网上搜吧，不再详述）
* python
* pygame

# 用法
0.  文本编辑器打开jump.py，修改其中的ADB_PATH，指向adb的绝对路径（Windows下是adb.exe）；然后根据自己手机，修改屏幕大小SCREEN_WIDTH、SCREEN_HEIGHT。然后USB连接手机，并开启调试模式。
1. 开启"跳一跳"小程序
2. 运行jump.py，如果成功，可以看到当前手机界面
3. 用鼠标左键标出两个点（从哪里，要跳到哪里），然后右键点击
4. 等待几秒钟，看到新界面，重复3

其他：键盘上下键可以调节跳跃长度所乘的因子，可根据实际情况调节。


![UI](ui.png?raw=true "界面")

