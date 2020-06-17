#! /usr/bin/env python
# coding: utf-8
__author__ = '鹛桑够'


ip_1a = 256
ip_2a = ip_1a * ip_1a
ip_3a = ip_1a * ip_2a
ip_4a = ip_1a * ip_3a


def ip_value_str( ip_str=None, ip_value=None):
    if ip_str is not None:
        ip_s = ip_str.split(".")
        if len(ip_s) != 4:
            return 0
        try:
            ip = int(ip_s[0]) * ip_3a + int(ip_s[1]) * ip_2a + int(ip_s[2]) * ip_1a + int(ip_s[3])
        except ValueError:
            return 0
        return ip
    if ip_value is not None:
        ip_1 = ip_value / ip_3a
        ip_value %= ip_3a
        ip_2 = ip_value / ip_2a
        ip_value %= ip_2a
        ip_3 = ip_value / ip_1a
        ip_4 = ip_value % ip_1a
        ip_str = "%s.%s.%s.%s" % (ip_1, ip_2, ip_3, ip_4)
        return ip_str


def verify_in_subnet(ip_str, sub_net):
    sub_info = sub_net.split("/")
    if len(sub_info) != 2:
        if ip_str != sub_net:
            return False
        else:
            return True
    ip_value = ip_value_str(ip_str=ip_str)
    net_ip_str, num = sub_info
    net_ip_value = ip_value_str(ip_str=net_ip_str)
    num = int(num)
    if ip_value ^ net_ip_value < 2 ** (32 - num):
        return True
    return False
