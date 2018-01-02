# coding: utf-8
import os
import subprocess
import time
import random
 
import pygame
from pygame.locals import *

##################################
## 说明：用adb发送消息，玩游戏“跳一跳”。需要adb工具（Android）
## 用法：进入“跳一跳”，运行程序，鼠标左键点击两个位置，设置好后，右键点击。
##          键盘上下键调节跳远长度因子

##################################
## 可调节参数，根据实际情况调整
# ADB位置
ADB_PATH = r'/usr/local/android-sdk-linux/platform-tools/adb'

# 屏幕大小
SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 1920

# 跳跃长度因子
JUMP_FACTOR = 2.7

##################################
# constants
FRAMES_PER_SEC = 30
SCREEN_SCALE = 2			# 截图缩小参数
SCREENRECT = Rect(0, 0, SCREEN_WIDTH / SCREEN_SCALE, SCREEN_HEIGHT / SCREEN_SCALE)
PT_COLOR = Color(0,255,0, 0),
RED= Color(255,0, 0),

class Jumper:
	def __init__(self):
		# 两个点初始化
		self.start = None
		self.end = None
		
		# factor显示
		self.jump_factor = JUMP_FACTOR
		self.update_factor()
		
		# adb shell初始化
		self.adb = subprocess.Popen([ADB_PATH,  "shell"],  stdin=subprocess.PIPE)
		time.sleep(1)
		
		# 截屏
		self.adb.stdin.write('/system/bin/screencap -p /sdcard/screenshot.png \n')
		time.sleep(1)
		subprocess.check_call([ADB_PATH, 'pull',  '/sdcard/screenshot.png', 'screenshot.png'])
		
		# 加载初始背景
		img = pygame.image.load('screenshot.png')
		self.back = pygame.transform.scale(img, SCREENRECT[2:])
		
	def update_factor(self):
		self.font =  pygame.font.Font(None, 30)
		self.text_surface = self.font.render('Factor: %.1f' % self.jump_factor, True, RED)

	def update(self, ev):
		# 更新
		for event in ev:
			if event.type == pygame.MOUSEBUTTONDOWN:	# 鼠标处理
				if event.button == 1:
					# 鼠标左键点击，设置两个点
					if not self.start:	# first click
						self.start = pygame.mouse.get_pos()
					elif not self.end:
						self.end = pygame.mouse.get_pos()
					else:
						self.start = pygame.mouse.get_pos()
						self.end = None
						
				if event.button == 3  and self.start and self.end:
					# 鼠标右键点跳
					self.touch(  (abs(self.start[0] - self.end[0]) ** 2 + abs(self.start[1] - self.end[1]) ** 2)**0.5 )
					
					img = pygame.image.load('screenshot.png')
					self.back = pygame.transform.scale(img, SCREENRECT[2:])
					
					self.start = None
					self.end = None
			elif event.type == pygame.KEYDOWN:	# 增减跳跃因子
				if event.key == pygame.K_UP:
					self.jump_factor += 0.1
					self.update_factor()
				elif event.key == pygame.K_DOWN:
					self.jump_factor -= 0.1
					self.update_factor()

	def draw(self, screen):
		# 绘制屏幕
		screen.blit(self.back, (0, 0))
		if self.start:
			pygame.draw.circle(screen, PT_COLOR, self.start, 10)
		if self.end:
			pygame.draw.circle(screen, PT_COLOR, self.end, 10)
			
		screen.blit(self.text_surface, (0, 0, 100, 100))
			
	def touch(self, length):
		# 发送触摸消息，并截屏
		
		# 点击位置+抖动
		x = SCREEN_WIDTH / 2 + random.randint(-100, 100)
		y = SCREEN_HEIGHT * 4 / 5 + random.randint(-100, 100)
		
		# 触摸消息
		cmd = "input swipe %d %d %d %d %d\n" %(x, y, x, y,  length * self.jump_factor)
		self.adb.stdin.write(cmd)
		
		# 截屏并复制出来
		time.sleep(3)
		self.adb.stdin.write('/system/bin/screencap -p /sdcard/screenshot.png \n')
		time.sleep(1)
		subprocess.check_call([ADB_PATH, 'pull',  '/sdcard/screenshot.png', 'screenshot.png'])
		
	def quit(self):
		if self.adb:
			self.adb.stdin.write('exit\n')

def main(winstyle = 0):
	pygame.init()

	screen = pygame.display.set_mode(SCREENRECT.size, 0)
	clock = pygame.time.Clock()

	jumper = Jumper()

	# 循环
	while True:
		clock.tick(FRAMES_PER_SEC)

		pygame.event.pump()
		keystate = pygame.key.get_pressed()
		if keystate[K_ESCAPE] or pygame.event.peek(QUIT):
			break
		
		ev = pygame.event.get()
		jumper.update(ev)
		jumper.draw(screen)
		
		pygame.display.update()

	jumper.quit()
	pygame.time.wait(10)

if __name__ == '__main__':
	main()
