#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# The MIT License (MIT)
# 
# Copyright (c) 2020 Murahashi Kuriki
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import sys
import io
import tweepy
import datetime
import config
# 日本語を吐き出すとエラーが出るので追加
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# OAuth認証部分
# 同じディレクトリにある config.py から鍵情報を読み込む
CK      = config.CONSUMER_KEY
CS      = config.CONSUMER_SECRET
AT      = config.ACCESS_TOKEN
ATS     = config.ACCESS_TOKEN_SECRET
auth = tweepy.OAuthHandler(CK, CS)
auth.set_access_token(AT, ATS)
api = tweepy.API(auth)

sc_name = api.get_user('mkuriki_')
print(sc_name.name)

# 各月の絵文字
moons = [
        "🌑", #1 新月
        "🌒", #2 三日月
        "🌓", #3 半月
        "🌔", #4 十三夜月
        "🌕", #5 満月
        "🌖", #6 寝待月
        "🌗", #7 弦月
        "🌘" #8 晦月
]

# 現在の年月日時を int 型で取得
dt_now = datetime.datetime.now()
timenow = dt_now.strftime('%H:%M:%S')
year = int(dt_now.strftime('%Y'))
month = int(dt_now.strftime('%m'))
day = int(dt_now.strftime('%d'))
hour = int(dt_now.strftime('%H'))

# 月ごとの定数の計算
if month == 1 or month == 3:
    month_const = 0
elif month == 2 or month == 5:
    month_const = 2
else:
    month_const = month - 2

# なんとなくお昼の 12 時以前は前日の情報にしたい
if hour < 12:
    day -= 1

# 月齢を計算し, 月齢ごとに emoji を割り振る
moon_age = (((year - 11) % 19) * 11 + month_const + day) % 30

if moon_age > 2.0 and moon_age <= 4.2:
    moon_num = 1
elif moon_age > 4.2 and moon_age <= 8.4:
    moon_num = 2
elif moon_age > 8.4 and moon_age <= 13.8:
    moon_num = 3
elif moon_age > 13.8 and moon_age <= 15.8:
    moon_num = 4
elif moon_age > 15.8 and moon_age <= 19.0:
    moon_num = 5
elif moon_age > 19.0 and moon_age <= 22.8:
    moon_num = 6
elif moon_age > 22.8 and moon_age <= 26.8:
    moon_num = 7
else:
    moon_num = 0

print("月齢 %d" % moon_age)
moon = moons[moon_num]

# 表示名を設定
nameStr = "村橋究理基%s%s" % (moon, timenow)
profileStr = "名前の%sは今夜の月を表しています。仕組みの説明→https://t.co/ACE6OhPVVz 北海道大学理学院宇宙理学 博士3+2年 惑星気象/火星大気シミュレーション。3Dプリンタ/恵迪寮寮歌集アプリ開発/高校教諭 専修免許(理科)/学芸員/恵迪寮第300期寮長/(一社)恵迪寮同窓会理事/愛知県立津島高校出身" % moon

api.update_profile(name = nameStr, description = profileStr)

