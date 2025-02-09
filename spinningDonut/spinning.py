'''
Author: BITnene465 2073335023@qq.com
Date: 2025-01-31 10:06:56
LastEditors: BITnene465 2073335023@qq.com
LastEditTime: 2025-01-31 13:55:27
FilePath: \spinningDonut\spinning.py
Description: 使用Python实现在终端内用字符渲染一个旋转的甜甜圈

Copyright (c) 2025 by BITnene465, All Rights Reserved. 
'''

import time
import sys
import os
import math
import numpy as np

# 在终端内渲染一个旋转进度条
def spinning_cursor(limit=10):
    start = time.time()
    while time.time() - start < limit:
        for i in ['|', '/', '-', '\\']:
            sys.stdout.write(i)
            sys.stdout.flush()
            time.sleep(0.2)
            sys.stdout.write('\b')
            

# 用一个数据类来存储各种参数: 甜甜圈的角度、半径、字符等
class Donut:
    def __init__(self, isClockwise=-1, total_steps_per_cirle=40, angle=0.0, inner_radius=0.3, outer_radius=0.8, empty_char=' ', char_list=['*', '+', '$','#'], width=100, height=50, fps=30):
        self.isClockwise = isClockwise   # 旋转方向， 1 为顺时针， -1 为逆时针
        self.total_steps_per_circle = total_steps_per_cirle     # 转一周的步数
        self.angle = angle   # 当前的旋转角度
        
        
        self.inner_radius = inner_radius # 内半径, 归一化到区间 [-1, 1]
        self.outer_radius = outer_radius # 外半径, 归一化值
        self.thickness = (outer_radius - inner_radius) / 2   # 甜甜圈的厚度（也是一个半径值）， 归一化值
        self.empty_char = empty_char # 空白字符
        self.char_list = char_list   # 用来填充甜甜圈的字符, 从最暗到最亮
        self.width = width           # 屏幕宽度
        self.height = height         # 屏幕高度           
        self.fps = fps                  # 帧率
    
    def rotate_one_step(self):
        self.angle += 2 * math.pi * self.isClockwise / self.total_steps_per_circle
        # 保证 angle 的范围在 [0, 2 * pi]
        while self.angle >= 2 * math.pi:
            self.angle -= 2 * math.pi
        while self.angle < 0:
            self.angle += 2 * math.pi
    
    def check(self, x, y, z):
        center_radius = (self.outer_radius + self.inner_radius) / 2
        # 将 x, y, z 转换到甜甜圈的坐标系中, 相当于点在 xoz 平面上绕原点旋转 -self.angle
        x, z = x * math.cos(self.angle) - z * math.sin(self.angle), x * math.sin(self.angle) + z * math.cos(self.angle)
        
        # 计算点到甜甜圈中心线的距离
        if x!=0 or y!=0:
            sin_alpha = y / math.sqrt(x ** 2 + y ** 2)
            cos_alpha = x / math.sqrt(x ** 2 + y ** 2)
            distance = math.sqrt((x - center_radius * cos_alpha) ** 2 + (y - center_radius * sin_alpha) ** 2 + z ** 2)
        else:
            distance =  float('inf')  # 无穷大
        
        if distance < self.thickness:
            # 计算亮度： 计算该点的法向量与光线的夹角
            normal_vector = np.array([x - center_radius * cos_alpha, y - center_radius * sin_alpha, z])
            light_vector = np.array([-math.sin(self.angle), 0, math.cos(self.angle)])
            normal_vector = normal_vector / np.linalg.norm(normal_vector)
            light_vector = light_vector / np.linalg.norm(light_vector)
            cos_theta = np.dot(normal_vector, light_vector)
            return ((cos_theta + 1) / 2) * (len(self.char_list) - 1)
        else:
            return 0.0
        
    
# 渲染一帧
def render_frame(donut, lightArray):
    # 取样并确定每个像素的值
    steps = 100
    step_size = 2.0 / steps
    for y in range(donut.height):
        for x in range(donut.width):
            # 归一化到 [-1, 1]
            x_normalized = (x - donut.width / 2) / (donut.width / 2)
            y_normalized = (y - donut.height / 2) / (donut.height / 2)
            z_normalized = - 1.0
            lightArray[x, y] = 0.0
            for _ in range(steps):
                res = donut.check(x_normalized, y_normalized, z_normalized)
                lightArray[x, y] = max(lightArray[x, y], res)
                z_normalized += step_size    
            
    # 生成Ascii的帧输出
    output = []
    for y in range(donut.height):
        for x in range(donut.width):
            if lightArray[x, y] < 0.01:
                output.append(donut.empty_char)
            else:
                output.append(donut.char_list[round(lightArray[x, y])])
        output.append('\n')
    # 清除终端所有输出
    os.system('cls' if os.name == 'nt' else 'clear')
    print(''.join(output))
    
    
# 用一个函数来渲染甜甜圈
def render_donut(donut):
    lightArray = np.zeros((donut.width, donut.height), dtype=float)
    while True:
        render_frame(donut, lightArray)
        donut.rotate_one_step()
        time.sleep(1.0 / donut.fps)
    


            
if __name__ == '__main__':
    print("Spinning Donut loading...")
    spinning_cursor(1)
    donut = Donut()
    render_donut(donut)