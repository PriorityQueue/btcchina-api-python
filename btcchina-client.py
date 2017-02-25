#!/usr/bin/python
# -*- coding: utf-8 -*-
from time import sleep

import btcchina

SLEEP_TIME = 1
DEPTH = 3

my_MAX = -1
my_MIN = 6147483200

access_key = "your_access_key"
secret_key = "your_se3r3t_key"

bc = btcchina.BTCChina(access_key,secret_key)


def debug_print(s):
    print "[>>>]", s

''' These methods have no arguments '''
# result = bc.get_account_info()
# print result

while(True):
    ask_list = []
    bid_list = []

    result = bc.get_market_depth2(DEPTH)
    ask = result["market_depth"]["ask"]
    bid = result["market_depth"]["bid"]

    # --------------------------
    # print '-'*10
    print ''
    for item in ask[::-1]:
        ask_list.append(item['price'])

    if my_MAX < ask_list[-1]:
        my_MAX = ask_list[-1]
    print 'ask::', ask_list
    print 'my_MAX::', my_MAX

    # print '***************'

    for item in bid:
        # print item['price'], item['amount']
        bid_list.append(item['price'])
    print 'bid::', bid_list
    if my_MIN> bid_list[0]:
        my_MIN = bid_list[0]
    print 'my_MIN::', my_MIN
    # print '-'*10
    # --------------------------
    print 'Δ:', my_MAX-my_MIN, '@', result["market_depth"]['date']
    # print result["market_depth"]['date']
    print ''

    sleep(SLEEP_TIME)
 
# NOTE: for all methods shown here, the transaction ID could be set by doing
# result = bc.get_account_info(post_data={'id':'stuff'})
# print result
 
''' buy and sell require price (CNY, 5 decimals) and amount (LTC/BTC, 8 decimals) '''
# 买卖操作
#result = bc.buy(500,1)
#print result
#result = bc.sell(500,1)
#print result
 
''' cancel requires id number of order '''
# 取消对应id的交易 id元素在order[]末尾
#result = bc.cancel(2)
#print result
 
''' request withdrawal requires currency and amount '''
# 查询提现
#result = bc.request_withdrawal('BTC',0.1)
#print result
 
''' get deposits requires currency. the optional "pending" defaults to true '''
# 查询充值
# result = bc.get_deposits('BTC',pending=False)
# print result
 
''' get orders returns status for one order if ID is specified,
    otherwise returns all orders, the optional "open_only" defaults to true '''
# 查询目前卖单  只能打印open单, close单实际上无法打印·
# result = bc.get_orders()
# print result
# result = bc.get_orders(open_only=True)
# print result
 
''' get withdrawals returns status for one transaction if ID is specified,
    if currency is specified it returns all transactions,
    the optional "pending" defaults to true '''
# result = bc.get_withdrawals(2)
# print result
# result = bc.get_withdrawals('BTC',pending=True)
# print result
 
''' Fetch transactions by type. Default is 'all'. 
    Available types 'all | fundbtc | withdrawbtc | fundmoney | withdrawmoney | 
    refundmoney | buybtc | sellbtc | tradefee'
    Limit the number of transactions, default value is 10 '''
# result = bc.get_transactions('all',10)
# print result

'''get archived order returns a specified id order which is archived,
   the market default to "BTCCNY" and the "withdetail" default to false,if "withdetail" is specified to "true", the result will include the order's detail'''
# result = bc.get_archived_order(2,'btccny',False)
# print result

'''get archived orders returns the orders which order id is less than the specified "less_than_order_id",and the returned amount is defined in "limit",
   default value is 200, if "withdetail" is specified to "true",
   the result will include to orders' detail'''
# result = bc.get_archived_orders('btccny',200,10000,False)
# print result
