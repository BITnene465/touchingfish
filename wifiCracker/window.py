# 使用 tkinter 库构建简单界面，用于 wifi 破解

import os 
from tkinter import *
from tkinter import filedialog, messagebox
from cracker import scan_wifi, crack_password

def select_file(entry_password_list):
    file_path = filedialog.askopenfilename()
    entry_password_list.delete(0, END)
    entry_password_list.insert(0, file_path)

def update_wifi_list(wifi_listbox):
    wifi_listbox.delete(0, END)
    wifi_list = scan_wifi()
    for ssid, signal in wifi_list:
        if signal <= -100:
            signal_strength = 1
        elif signal <= -80:
            signal_strength = 2
        elif signal <= -60:
            signal_strength = 3
        elif signal <= -40:
            signal_strength = 4
        else:
            signal_strength = 5
        wifi_listbox.insert(END, f"{ssid} (信号强度: {signal_strength})")

def on_wifi_select(event, wifi_listbox, entry_ssid):
    selected_wifi = wifi_listbox.get(wifi_listbox.curselection())
    ssid = selected_wifi.split(" (")[0]    # 只取 ssid 部分，此处分割符号和前面对应
    entry_ssid.delete(0, END)
    entry_ssid.insert(0, ssid)

def connect_wifi(entry_ssid, entry_password_list):
    ssid = entry_ssid.get()
    password_list = entry_password_list.get()
    if not ssid:
        messagebox.showwarning("警告", "请选择一个 WiFi")
        return
    if not password_list:
        messagebox.showwarning("警告", "请选择密码字典文件")
        return
    crack_password(ssid, password_list)

def main_app():
    root = Tk()
    root.title("WiFi 破解工具")

    frame = Frame(root)
    frame.pack(pady=10, fill=BOTH, expand=True)

    label_ssid = Label(frame, text="选择 WiFi:")
    label_ssid.grid(row=0, column=0, padx=5, pady=5, sticky=W)

    entry_ssid = Entry(frame, width=50)
    entry_ssid.grid(row=0, column=1, padx=5, pady=5, sticky=EW)

    button_connect = Button(frame, text="连接 WiFi", command=lambda: connect_wifi(entry_ssid, entry_password_list))
    button_connect.grid(row=0, column=2, padx=5, pady=5, sticky=E)

    label_password_list = Label(frame, text="选择密码字典文件:")
    label_password_list.grid(row=1, column=0, padx=5, pady=5, sticky=W)

    entry_password_list = Entry(frame, width=50)
    entry_password_list.grid(row=1, column=1, padx=5, pady=5, sticky=EW)

    button_select_file = Button(frame, text="选择文件", command=lambda: select_file(entry_password_list))
    button_select_file.grid(row=1, column=2, padx=5, pady=5, sticky=E)

    frame.grid_columnconfigure(1, weight=1)

    button_scan = Button(root, text="扫描 WiFi", command=lambda: update_wifi_list(wifi_listbox), width=20)
    button_scan.pack(pady=10, fill=Y)

    wifi_listbox = Listbox(root, width=50, height=15)
    wifi_listbox.pack(pady=10, fill=BOTH, expand=True)
    wifi_listbox.bind('<<ListboxSelect>>', lambda event: on_wifi_select(event, wifi_listbox, entry_ssid))

    root.mainloop()

if __name__ == "__main__":
    main_app()