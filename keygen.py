#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import random
import datetime

from typing import Union
from config import TABLE, KEY_LIST

TIME_VAL = []
COUNT_VAL = []


def get_random_expire_time(days_num: int, is_max=False) -> (int, int):
    """
    根据预期的注册码有效期计算注册码参数
    :param days_num: 注册码有效期，从 2019/12/7 起的天数，支持 0-968659
    :param is_max: 是否直接设置注册码有效期为算法支持的最大值，days_num=0 时有效
    :return: 生成的计算参数，包括两个值
    """
    if len(TIME_VAL) == 0:
        for i in range(0x473C * 0x11, 0x00FFFFFF, 0x11):
            if i % 0x11 == 0:
                TIME_VAL.append(i)

    if days_num == 0:
        if is_max:
            val_0 = TIME_VAL[-1]
        else:
            days_num = 5 * 365 + int(random.random() * 30)
            val_0 = TIME_VAL[days_num]
    else:
        days_num = len(TIME_VAL) if days_num > len(TIME_VAL) else days_num
        val_0 = TIME_VAL[days_num]
    val_1 = (((val_0 ^ 0xffe53167) + 180597) ^ 0x22c078 ^ 0x5b8c27) & 0xffffff
    return val_0, val_1


def get_random_user_count(user_num=0, is_max=False) -> (int, int):
    """
    根据预期的注册码有效用户数计算注册码参数
    :param user_num: 预期的可激活用户数，支持 1-0x3E8
    :param is_max: 是否直接设置注册码有效用户数为算法支持的最大值，user_num=0 时有效
    :return: 生成的计算参数，包括两个值
    """
    if len(COUNT_VAL) == 0:
        for i in range(0xB, 0x3E8 * 0xB, 0xB):
            if i % 0xB == 0:
                COUNT_VAL.append(i)

    if user_num == 0:
        if is_max:
            val_0 = 0x3E8 * 0xB
        else:
            val_0 = random.choices(population=COUNT_VAL, k=1)[0]
    else:
        user_num = 0x3E8 if user_num > 0x3E8 else user_num
        val_0 = user_num * 0xB
    val_1 = ((val_0 ^ 0x3421) - 19760) ^ 0x7892
    return val_0, val_1


def get_calc_value(username: str, days_idx: int, user_idx: int) -> int:
    """
    根据传入的参数计算出用于生成激活码的参数值
    :param username: 用户名
    :param days_idx: 根据激活码有效期计算出的第一个参数
    :param user_idx: 根据激活码用户数计算出的第一个参数
    :return: 生成激活码的关键参数值
    """
    ret = 0
    cnt_idx = (15 * user_idx) & 0xff
    time_idx = (17 * days_idx) & 0xff
    cal_idx = 0
    for ch in username:
        val = ord(ch.upper())
        ret = TABLE[cnt_idx] + TABLE[time_idx] + TABLE[cal_idx] + TABLE[val + 47] * (
                (ret + TABLE[val]) ^ TABLE[val + 13])
        cnt_idx = (cnt_idx + 13) & 0xff
        time_idx = (time_idx + 9) & 0xff
        cal_idx = (cal_idx + 19) & 0xff
    return ret


def get_password_from_username(username: str, user_cnt=0, max_user=False, days_cnt=0, max_days=False) -> str:
    """
    根据用户名、注册码有效期、可激活用户数等信息，按照 [0xac] 类算法生成激活码（密码）
    :param username: 激活时使用的用户名
    :param user_cnt: 激活码的可激活用户数
    :param max_user: 使用算法支持的最大可激活用户数
    :param days_cnt: 激活码有效期，从 2019/12/7 起的天数
    :param max_days: 使用算法支持的最大有效期
    :return: 激活码（密码）
    """
    print("===== 生成零售密钥，可正常激活 =====")
    buff: list[Union[int, str]] = [0] * 10
    days_val0, days_val1 = get_random_expire_time(days_num=days_cnt, is_max=max_days)
    user_val0, user_val1 = get_random_user_count(user_num=user_cnt, is_max=max_user)

    val = get_calc_value(username, days_val0 // 0x11, user_val0 // 0xB)
    for idx in range(4):
        buff[4 + idx] = (val >> (idx * 8)) & 0xff
    buff[3] = 0xac
    buff[2] = (user_val1 & 0xff) ^ buff[5]
    buff[1] = ((user_val1 >> 8) & 0xff) ^ buff[7]
    buff[0] = (days_val1 & 0xff) ^ buff[6]
    buff[8] = ((days_val1 >> 8) & 0xff) ^ buff[4]
    buff[9] = ((days_val1 >> 16) & 0xff) ^ buff[5]

    for idx in range(10):
        if buff[idx] < 0:
            buff[idx] &= 0xff
        buff[idx] = hex(buff[idx])[2:].zfill(2)
    password = "%s%s-%s%s-%s%s-%s%s-%s%s" % (buff[0], buff[1], buff[2], buff[3], buff[4], buff[5], buff[6], buff[7], buff[8], buff[9])
    print("用户名", username)
    print("激活码", password)
    print("可激活用户数", user_val0 // 0xB)

    base_date = datetime.datetime(year=2019, month=12, day=7)
    expire_date = base_date + datetime.timedelta(days=TIME_VAL.index(days_val0))
    print("到期时间为", expire_date.strftime("%Y-%m-%d"))
    print("剩余天数为", (expire_date - datetime.datetime.now()).days, "天")
    return password


def get_evaluation_password_from_username(username: str, user_cnt=0, max_user=False) -> str:
    """
    根据用户名、注册码有效期、可激活用户数等信息，按照 [0x9c] 类算法生成激活码（密码）
    :param username: 激活时使用的用户名
    :param user_cnt: 激活码的可激活用户数
    :param max_user: 使用算法支持的最大可激活用户数
    :return: 激活码（密码）
    """
    print("===== 生成测试密钥，可激活但不再受官方支持 =====")
    buff: list[Union[int, str]] = [0] * 8
    buff[3] = 0x9c
    user_val0, user_val1 = get_random_user_count(user_num=user_cnt, is_max=max_user)
    val = get_calc_value(username, 0, user_val0 // 0xB)

    buff[4] = val & 0xff
    buff[5] = (val >> 8) & 0xff
    buff[6] = (val >> 16) & 0xff
    buff[7] = (val >> 24) & 0xff
    buff[2] = buff[5] ^ (user_val1 & 0xff)
    buff[1] = buff[7] ^ ((user_val1 >> 8) & 0xff)
    while True:
        buff[0] = int(random.random() * 256)
        v10 = (((buff[6] ^ buff[0]) ^ 0x18 + 61) & 0xff) ^ 0xa7
        if v10 >= 10:
            break

    for idx in range(8):
        if buff[idx] < 0:
            buff[idx] &= 0xff
        buff[idx] = hex(buff[idx])[2:].zfill(2)
    password = "%s%s-%s%s-%s%s-%s%s" % (buff[0], buff[1], buff[2], buff[3], buff[4], buff[5], buff[6], buff[7])
    print("用户名", username)
    print("激活码", password)
    print("可激活用户数", user_val0 // 0xB)
    return password


if __name__ == "__main__":
    license_type = "0xac"
    # license_type = "0x9c"
    # license_type = "0xfc"
    uname = "TestUser"
    prefer_user = 2
    key = KEY_LIST.get_by_name(license_type)
    if key is None:
        raise ValueError(f"License type [{license_type}] not supported.")
    if not key.activated:
        raise ValueError(f"License type [{license_type}] not available for activating.")

    if key.retail:
        prefer_days = 10 * 365
        # 按指定有效期、指定用户数生成激活码
        get_password_from_username(username=uname, user_cnt=prefer_user, days_cnt=prefer_days)
        # 按最长有效期、最大用户数生成激活码
        # get_password_from_username(username=uname, max_days=True, max_user=True)
    else:
        get_evaluation_password_from_username(username=uname, user_cnt=prefer_user)
