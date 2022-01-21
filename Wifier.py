# -*- encoding = utf-8 -*-
# author : manlu
import subprocess
import sys
import time

import pywifi

from Bruter import Bruter

interface = None
# ssids=[]
target = ""
passwords = "./pass.txt"
timewait = 1.5
pwd = ""


def help():
    str = """
    [-] 介绍：WIFI破解器
    [-] 指令：
            help : 显示帮助信息
            test : 测试网卡
            scan : 扫描可用WIFI
            options : 显示参数
            set : 设置参数
            run : 运行
            dump : 导出结果
            system : 执行系统指令
            exit : 退出程序
    [-] 指令执行方式： 指令 (参数)
    """
    print(str)


def test():
    global interface
    wifi = pywifi.PyWiFi()
    interfaces = wifi.interfaces()
    if len(interfaces) <= 0:
        print("[-] 未检测到无线网卡")
    else:
        wifi_face = interfaces[0]
        print("[-] 检测到网卡 %s" % wifi_face.name())
        print("[-] 正在使用网卡 %s" % wifi_face.name())
        interface = wifi_face


def scan():
    global ssids
    try:
        interface.scan()
        print("[-] 正在扫描")
        for i in range(5):
            print("▋" * (i + 1), end="")
            sys.stdout.flush()
            time.sleep(1)
        print("")
        result = interface.scan_results()
        print("[-] 可用Wifi(前面的是WIFI名称，后面的是信号强度)")
        print("[-] 注：信号强度小于 -90 的几乎连不上")
        for res in result:
            ssid = res.ssid.encode('raw_unicode_escape').decode('utf-8')
            signal = res.signal
            if ssid != "":
                print("[+] %s , %d" % (ssid, signal))
            # ssids.append([ssid,signal])
    except AttributeError:
        print("[-] 无网卡，请先运行 test 指令扫描网卡")


def system(cmd):
    proc = subprocess.Popen(
        cmd,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        stdin=subprocess.PIPE
    )
    proc.stdin.close()
    proc.wait()
    text = proc.stdout.read()
    encoding = 'gbk'
    result = text.decode(encoding)
    proc.stdout.close()
    print("[+] %s" % result)


def options():
    """
    target :
    passwords :
    timewait :
    """
    global target
    global passwords
    global timewait
    s = """
[+------------------------------+]\n   
target : {}\n
passwords : {}\n
timewait : {}\n
[+------------------------------+]\n""".format(target, passwords, timewait)
    print(s)


def set(inp):
    global target
    global passwords
    global timewait
    try:
        option = inp.split(' ')[1]
        value = inp.split(' ')[2]
        if option == 'target':
            target = value
        elif option == 'passwords':
            passwords = value
        elif option == 'timewait':
            tw = float(value)
            if tw > 0:
                timewait = tw
            else:
                print("[-] 无效的timewait值，必须大于0")
        else:
            print("[-] 未知参数")
    except IndexError:
        print("[-] 无效的set指令，格式为 set option value")
        print("[-] 例如: set target targetwifi")
    except ValueError:
        print("[-] 无效的timewait值，必须是一个数字")


def dump(inp):
    try:
        outpath = inp.split(' ')[1]
        # if target!="" and password!="":
        if target + pwd != "":
            f = open(outpath, 'w', encoding='utf-8')
            f.write(target)
            f.write("\n")
            f.write(pwd)
            f.close()
        else:
            print("[-] 导出失败")
    except IndexError:
        print("[-] 无效的dump指令，格式为 set outpath")
        print("[-] 例如 : dump result.txt")


def console():
    global pwd
    while True:
        inp = input(">>>")
        command = inp.split(' ')[0]
        if command == "help":
            help()
        elif command == 'exit':
            sys.exit(0)
        elif command == "test":
            test()
        elif command == 'scan':
            scan()
        elif command == "system":
            system(inp.split(' ')[1])
        elif command == 'options':
            options()
        elif command == "set":
            set(inp)
        elif command == 'run':
            bruter = Bruter(target, passwords, timewait, interface)
            result = bruter.run()
            if result != None:
                pwd=result
        elif command == 'dump':
            dump(inp)
        else:
            print("[-] 未知的指令，请输入 help 查看指令帮助")


def banner():
    banner = r"""
 __          _______ ______ _____           
 \ \        / /_   _|  ____|_   _|          
  \ \  /\  / /  | | | |__    | |            
   \ \/  \/ /   | | |  __|   | |            
    \  /\  /   _| |_| |     _| |_           
  ___\/ _\/__ |_____|_|____|_____|__ _____  
 |  _ \|  __ \| |  | |__   __|  ____|  __ \ 
 | |_) | |__) | |  | |  | |  | |__  | |__) |
 |  _ <|  _  /| |  | |  | |  |  __| |  _  / 
 | |_) | | \ \| |__| |  | |  | |____| | \ \ 
 |____/|_|  \_\\____/   |_|  |______|_|  \_\
 
 ---Powered by manlu
 ---作者的话：WIFI破解，3分靠暴力，7分靠耐力，剩下的90分全靠运气
    """
    print(banner)


if __name__ == '__main__':
    if sys.argv[1] == 'console':
        banner()
        console()
