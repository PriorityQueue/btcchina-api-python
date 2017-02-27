#!/usr/bin/python
# -*- coding: utf-8 -*-
from time import sleep
import time

from twilio.rest import TwilioRestClient

import btcchina

SLEEP_TIME = 1
DEPTH = 1
TIME_THREAD = 30 * 60  # N minutes 检查的时间范围 30*60为最近的30分钟内
# GAP = 1*60
PRICE_GAP = 300        # 预警价格 当TIME_THREAD时间内价格超过PRICE_GAP时 调用twilio打电话预警
WARNING_THREAD = 300

my_MAX = -1
my_MIN = 6147483200

access_key = "your_key"
secret_key = "s3cr3t_key"

bc = btcchina.BTCChina(access_key, secret_key)

# Twilio Account
account_sid = "your_test_sid"
auth_token = "your_token"
client = TwilioRestClient(account_sid, auth_token)


def debug_print(s):
    print "[>>>]", s


''' These methods have no arguments '''


# result = bc.get_account_info()
# print result
def sortedDictKey(adict):
    keys = adict.keys()
    keys.sort()
    return keys


def getMAIX(mlist):
    if len(mlist) == 0:
        return 0, 0
    vmax = mlist[0]
    vmin = mlist[0]
    for v in mlist:
        if v > vmax:
            vmax = v
        if v < vmin:
            vmin = v
    return vmin, vmax


def abstract_price(list):
    re = []
    for item in list:
        re.append(item['price'])
    return re


def update(dict, date, TIME_THREAD):
    for key in dict.keys():
        if abs(dict[key] - date) > TIME_THREAD:
            dict.pop(key)


def merge(dict, list, date):
    for item in list:
        if item not in dict.keys():
            dict[item] = date


# Make Phone Alert
def make_alert():
    call = client.calls.create(to="+8613738020604",  # Any phone number
                               from_="2312259560 ",  # Must be a valid Twilio number
                               url="http://twimlets.com/holdmusic?Bucket=com.twilio.music.ambient")
    print(call.sid)


ask_dict = {}
bid_dict = {}
while True:
    ask_list = []
    bid_list = []
    result = bc.get_market_depth2(DEPTH)

    ask = result["market_depth"]["ask"]
    bid = result["market_depth"]["bid"]
    date = result["market_depth"]['date']
    human_date = time.localtime(date)
    # human_date_str = time.strftime('%Y%m%d>%H:%M:%S', human_date)
    human_date_str = time.strftime('%H:%M:%S', human_date)
    ask_price_list = abstract_price(ask)
    bid_price_list = abstract_price(bid)
    print '>' * 6, time.strftime('%Y-%m-%d %H:%M:%S', human_date), '<' * 6
    # print ask_price_list
    # print bid_price_list
    """
        先update删除超过TIME_THREAD的旧数据
        再通过merge更新数据。

        若先merge,再update。则存在一种情况：
            当旧value和新value等值，因dict中已有旧值，故不再插入新value，但其时间戳为旧，
            因此在update时若超过TIME_THREAD，该值被删，导致数据缺失: dict == {}
            这中情况在横盘时易发生。
    """
    update(ask_dict, date, TIME_THREAD)
    update(bid_dict, date, TIME_THREAD)
    merge(ask_dict, ask_price_list, date)
    merge(bid_dict, bid_price_list, date)
    # print ask_dict
    # print bid_dict
    ask_keys = sortedDictKey(ask_dict)
    bid_keys = sortedDictKey(bid_dict)
    bid_min, bid_max = getMAIX(bid_keys)
    print 'ask::', '[%.2f, %.2f]' % getMAIX(ask_keys), '>', ask_keys
    print 'bid::', '[%.2f, %.2f]' % (bid_min, bid_max), '>', bid_keys

    if abs(bid_max - bid_min) > PRICE_GAP:
        make_alert()

    # print bid

    # update(result, ask_dict, TIME_THREAD, my_MAX)
    # debug_print(ask_dict)

    # --------------------------
    # print '-'*10
    # print 'Δ:', my_MAX - my_MIN, '@', result["market_depth"]['date']
    # print result["market_depth"]['date']

    sleep(SLEEP_TIME)
