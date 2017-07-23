#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys,urllib2, json
reload(sys) # Python2.5 初始化后会删除 sys.setdefaultencoding 这个方法，我们需要重新载入
sys.setdefaultencoding('utf-8') #这个是解决合成中文文本的时候，Unicode和utf-8编码问题的，可以尝试注释掉会不会报错
#调用和风天气的API
url = 'https://free-api.heweather.com/v5/weather?city=' + sys.argv[1] + '&key=3e0c6c55f1a545a7a25d912e7fd394ab'
req = urllib2.Request(url)
resp = urllib2.urlopen(req).read()
#将JSON转化为Python的数据结构
json_data = json.loads(resp)
data = json_data['HeWeather5'][0]
#获取PM2.5的值
pm25 = data['aqi']['city']['pm25']
#获取空气质量
air_quality = data['aqi']['city']['qlty']
#获取城市
city = data['basic']['city']
#获取现在的天气、温度、体感温度、风向、风力等级
now_weather = data['now']['cond']['txt']
now_tmp = data['now']['tmp']
now_fl = data['now']['fl']
now_wind_dir = data['now']['wind']['dir']
now_wind_sc = data['now']['wind']['sc']
#今天的天气
today = data['daily_forecast'][0]
weather_day = today['cond']['txt_d']
weather_night = today['cond']['txt_n']
tmp_high = today['tmp']['max']
tmp_low = today['tmp']['min']
wind_dir = today['wind']['dir']
wind_sc = today['wind']['sc']
#天气建议
#舒适度
comf = data['suggestion']['comf']['brf']
comf_txt = data['suggestion']['comf']['txt']
#流感指数
flu = data['suggestion']['flu']['brf']
flu_txt = data['suggestion']['flu']['txt']
#穿衣指数
drsg = data['suggestion']['drsg']['brf']
drsg_txt = data['suggestion']['drsg']['txt']
weather_forcast_txt = " %s\n\t今天空气质量%s,PM2.5值%s,白天天气%s,夜间天气%s,\n\t最高气温%s摄氏度,最低气温%s摄氏度,\n\t风力%s,风向%s,\n\t天气舒适度：%s,%s,\n\t流感指数：%s,%s \n\t穿衣指数：%s,%s \n\t现在外面的天气：%s,当前温度:%s,当前风力:%s"%(city,air_quality,pm25,weather_day,weather_night,tmp_high,tmp_low,wind_sc,wind_dir,comf,comf_txt,flu,flu_txt,drsg,drsg_txt,now_weather,now_tmp,now_wind_sc)
print weather_forcast_txt
