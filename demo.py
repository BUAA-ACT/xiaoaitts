#-*- coding:utf8 -*-
# Copyright (c) 2019 barriery
# Python release: 3.7.0
import xiaoaitts

username = 'username'
password = 'password'
message = 'message'

t = xiaoaitts.XiaoaiTTS(username, password)

# 如果账户下有多个音箱设备，查看speak函数指定具体的音箱
t.speak(message)
