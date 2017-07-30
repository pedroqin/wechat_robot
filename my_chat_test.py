#!/usr/bin/python
# -*- coding:utf-8 -*-
import requests
import time
from itchat.content import *
import itchat
import ConfigParser
import commands
import sys
import os
#####info#####
import info
import music
import temperature
from sign_in import *
import datetime

from NetEaseMusicApi import interact_select_song
reload (sys)
sys.setdefaultencoding('utf8')
'''
*************personal Chat:************
命令---功能
*help                               --get this message
*setadmin                      --XXXX
speakXXXX                    --speak XXXX by sounder
糗百+页数(1/2/3...)      --爬取糗百纯文本内容
天气+地点                      --查询天气
温度                                 --查询宿舍温度
[音乐]功能----命令
播放                                 --音乐播放+[歌曲序号]
停止                                 --音乐停止/音乐暂停
更新列表                         --音乐更新
读取列表                         --音乐列表+[列表页数]
[get fil/img/vid/msg]
/Pedro/python/file/    <----file saved in this path when you send /img/vid/fil/voi to it
*get+fil/img/vid/msg+:/!+filepath    <---- if you get the file in /Pedro/python/file/XXX pls use '!',or, use ':' with whole path
*************group Chat:************
for amin：关闭群聊 打开群聊
签到
昨日统计
今日统计/统计

'''
KEY = '6d1f45613b434325b1b823f19fca5a91'
my_ID=''
#print info.admin_name
def get_response(msg):
    apiUrl = 'http://www.tuling123.com/openapi/api'
    data = {
        'key'    : KEY,
        'info'   : msg,
        'userid' : 'Pedro-wechat-robot',
    }
    try:
        r = requests.post(apiUrl, data=data).json()
        return r.get('text')
    except:
        return

#with open('stop.mp3','w') as f: pass
#def close_music():
#    os.startfile('stop.mp3')


@itchat.msg_register(itchat.content.TEXT)
def tuling_reply(msg):


#####let robot who is me
#    if msg['FromUserName'] == my_ID:
#        return 'I know you'
#####send command
#    get_IP = ['*ip','*IP']
#    for i in get_IP:
#            if msg['Text'] == i:
#                (status_cmd,output_cmd) = commands.getstatusoutput('ls')
#                return u'return : '+str(status_cmd)+u'\nresult : \n' + str(output_cmd)
    
#    cf = ConfigParser.ConfigParser()
#    cf.read('admin.conf')

#######  get robot switch and admin ID ######### now disable by Pedro
#    robot_switch = cf.get('switch','RobotSwitch')
#    my_ID = cf.get('admin','ID')
#    if msg['Text'].startswith('**'):
#        cf = ConfigParser.ConfigParser()
#        cf.read('admin.conf')
#        stop_cmd = ['baibai','bai','bye','byebye','shutdown','stop','close']
#        start_cmd = ['hi','hello','open','girl','start']
#        if robot_switch == 'True':
#        if True:
#            for i in stop_cmd:
#                if i == msg['Text'][2:]:
#                    cf.set('switch','RobotSwitch','False')
#                    cf.write(open("admin.conf","w"))
#                    return 'robot shutdown successfully'
#
#        else:
#            for i in start_cmd:
#                if i == msg['Text'][2:]:
#                    cf.set('switch','RobotSwitch','True')
#                    cf.write(open("admin.conf","w"))
#                    return 'robot reboot successfully'


####send message to admin
    admin_id=itchat.search_friends(name=info.admin_name)[0]['UserName']
    if msg['FromUserName'] != admin_id :
        itchat.send(u'I received %s\u2005 %s' % (msg['User']['NickName'],msg['Content']),admin_id)



#my_ID will change when you login after logoff
    if msg['Text'].startswith('*'):
######  help  ##############
        if msg['Text'][1:] == 'help':
            return '''******************
*help                               --get this message
*setadmin                      --XXXX
speakXXXX                    --speak XXXX by sounder
糗百+页数(1/2/3...)      --爬取糗百纯文本内容
天气+地点                      --查询天气
温度                                 --查询宿舍温度
[音乐]
播放                                 --音乐播放+[歌曲序号]
停止                                 --音乐停止/音乐暂停
更新列表                         --音乐更新
读取列表                         --音乐列表+[列表页数]
[get fil/img/vid/msg]
/Pedro/python/file/    <----file saved in this path when you send /img/vid/fil/voi to it
*get+fil/img/vid/msg+:/!+filepath    <---- if you get the file in /Pedro/python/file/XXX pls use '!',or, use ':' with whole path
******************
'''


######  set admin ID #######
        cf = ConfigParser.ConfigParser()
        cf.read(info.admin_file)
        my_ID = cf.get('admin','ID')
        if msg['Text'][1:] == 'setadmin':
            cf.set('admin','ID',msg['FromUserName'])
            cf.write(open(info.admin_file,"w"))
            return 'set You as Admin successfully !'


######  if is admin , run command  #######
        if msg['FromUserName'] == my_ID:

########music function   not ready#######
#            if msg['Text'][1:] == 'close':
#                close_music()
#                return 'music OFF'
#            elif msg['Test'][1:6] == 'play:':
#                itchat.send(interact_select_song(msg['Text'][6:]),my_ID)
#            else:
            if msg['Text'][1:4] == 'get':
##########   *get[img,fil,msg,vid]:[][filename]:[path]
                get_file(msg['Text'][4:7],msg['Text'][7],msg['Text'][8:])
                return 'post file to you successfully,pls check!'
            else:
                (status_cmd,output_cmd) = commands.getstatusoutput(msg['Text'][1:])
	
                return u'return : '+str(status_cmd)+u'\nresult : \n' + str(output_cmd)
        else:
            return 'Wrong admin ID, pls check'
#    elif robot_switch == 'True':


######  speak words you send me  #######
    if msg['Text'].startswith('speak'):
        cf = ConfigParser.ConfigParser()
        cf.read(info.admin_file)
        token = cf.get('token','key')
        url = 'http://tsn.baidu.com/text2audio?tex="%s"&lan=zh&per=0&pit=1&spd=7&cuid=9805555&ctp=1&tok=%s' % (msg['Text'][5:].strip().replace(' ',',').replace('\n','。'),token)
        os.system('mpg123  "%s" & ' % url)
        return 'speak words successfully'

#########  音乐  #######
    if msg['Text'].startswith(u'音乐'):
        if msg['Text'][2:].startswith(u'暂停') or msg['Text'][2:].startswith(u'停止'):
            return music.stop_music()
        elif msg['Text'][2:].startswith(u'更新'):
            return music.update_music()
        elif msg['Text'][2:].startswith(u'列表'):
            if len(msg['Text']) == 4:
                return music.list_music('1')
            else :
                return music.list_music(msg['Text'][4:])
        
        elif msg['Text'][2:].startswith(u'播放'):
            if len(msg['Text']) == 4:
                return music.play_music('1')
            else :
                return music.play_music(msg['Text'][4:])
       
#########  temperature  #######
    if msg['Text'].startswith(u'温度'):
        if len(msg['Text']) == 2:
            return str(temperature.temp())
	
#########  糗百  #######
    if msg['Text'].startswith(u'糗百'):
        if len(msg['Text']) == 2:
            page='1'
        elif msg['Text'][2:].isdigit():
            page=msg['Text'][2:]
        else :
            page='1'
        (status_cmd,output_cmd) = commands.getstatusoutput('python /Pedro/python/functions/qiubai.py '+page)
	
        return u'return : '+str(status_cmd)+u'\nresult : \n' + str(output_cmd.decode('utf-8'))

########  天气   #######
    if msg['Text'].startswith(u'天气'):
        if len(msg['Text']) == 2:
            local='东丽'
        else :
            local=msg['Text'][2:]
        (status_cmd,output_cmd) = commands.getstatusoutput('python /Pedro/python/functions/weather.py '+local)
        if status_cmd != 0:
            return u'天气查询失败，请输入正确地址'	
        return u'return : '+str(status_cmd)+u'\nresult : \n' + str(output_cmd.decode('utf-8'))
######### reply in normal #######
    defaultReply = 'I received: ' + msg['Text']
######### reply by tuling #######
    reply = get_response(msg['Text'])
    return reply or defaultReply
    return

######get_file function######
def get_file(file_type,path_type,file_path,fileDir='/Pedro/python/file/',toUserName=None,mediaID=None):
####   ':' : write path by yourself   '!' : file in path /Pedro/python/file/
    admin_id=itchat.search_friends(name='Pedro')[0]['UserName']
    if path_type == ':':
        file_tmp='@%s@%s' % (file_type,file_path)
    else:
        file_tmp='@%s@%s%s' % (file_type,fileDir,file_path)
    itchat.send(file_tmp,admin_id)
########Group Chat########
@itchat.msg_register(TEXT,isGroupChat=True)
def group_reply(msg):
    dailyLogMsg(msg["User"]["NickName"])#accumulate group 's message sum
    perNum(msg["ActualNickName"],msg["User"]["NickName"])#accumulate group everyone message sum
    cf = ConfigParser.ConfigParser()
    cf.read(info.admin_file)
    closeGroup=cf.get('wechatGroup','number')
    if msg['User']["NickName"] ==closeGroup:
        if msg['ActualNickName']!=info.admin_name:
            return 
        else:
            if msg['Content']=="打开群聊":
                cf.set('wechatGroup','number',"close")
                cf.write(open(info.admin_file,"w"))
                itchat.send(u'@%s\u2005 Reboot robot Successfully !' % msg['ActualNickName'],msg['FromUserName'])
            else:
                return
    if msg['Content']=="关闭群聊":
        if msg['ActualNickName']==info.admin_name:
            wechatGroup=msg['FromUserName']
            cf.set('wechatGroup','number',msg['User']["NickName"])
            cf.write(open(info.admin_file,"w"))
            itchat.send(u'@%s\u2005 Shutdown robot Successfully !' % msg['ActualNickName'],msg['FromUserName'])
    if msg['Content']=="签到" or msg['Content']=="qiandao" or msg['Content']=="簽到":
        result=signIn(msg['ActualNickName'],msg['User']["NickName"])
        if result == "False" :
            itchat.send(u'@%s\u2005 您今天已经签过到啦，不用重复签哦~' % (msg['ActualNickName']),msg['FromUserName'])
        else:
		#if result[0].isdigit():
            itchat.send(u'签到成功！\n @%s\u2005 ,您是今天第%s个签到的，已累计签到%s天' % (msg['ActualNickName'],result[1],result[0]),msg['FromUserName'])
#        else :
 #           itchat.send(u'@%s\u2005 啊咧~签到失败，请稍后再试' % (msg['ActualNickName']),msg['FromUserName'])
    if msg['isAt']:
#        itchat.send(u'@%s\u2005I received: %s' % (msg['ActualNickName'],msg['Content']),msg['FromUserName'])
#        defaultReply = 'I received: ' + msg['Text']

#####my robot name :  @robot_P len=8
        if msg['Content'][9:]=="昨日统计":
            day=datetime.date.today()-datetime.timedelta(days=1)#yesterday 's date
            countStr="%s日 发言排行: \n名次\t   昵称\t   发言数\n" % day.strftime('%Y-%b-%d')
            i=1
            for member in listGroup(day.strftime('%b-%d-%y'),msg['User']['NickName']):
                countStr=countStr +'第'+str(i)+'名'+':'+ member["name"] + '\t' + str(member["number"]) +'\n'
                i+=1
            itchat.send(u'%s' % countStr,msg['FromUserName'])

        elif msg['Content'][9:]=="今日统计" or msg['Content'][9:]=="统计":
            day=datetime.date.today()
            countStr="%s日 发言排行: \n名次\t   昵称\t   发言数\n" % day.strftime('%Y-%b-%d')
            i=1
            for member in listGroup(day.strftime('%b-%d-%y'),msg['User']['NickName']):
                countStr=countStr +'第'+str(i)+'名'+':'+ member["name"] + '\t' + str(member["number"]) +'\n'
                i+=1
            itchat.send(u'%s' % countStr,msg['FromUserName'])
            
        else:
            reply = get_response(msg['Content'][9:])
            itchat.send(u'@%s\u2005 %s' % (msg['ActualNickName'],reply),msg['FromUserName'])

@itchat.msg_register(FRIENDS)
def add_friend(msg):
    itchat.add_friend(**msg['Text'])
 # 该操作会自动将新好友的消息录入，不需要重载通讯录
    itchat.send_msg('Nice to meet you!', msg['RecommendInfo']['UserName'])

@itchat.msg_register([PICTURE,RECORDING,ATTACHMENT,VIDEO])
def download_files(msg):
    file_name='/Pedro/python/file/%s' % msg.fileName
    msg.download(file_name)
    itchat.send('@%s@%s' % ('img' if msg['Type'] =='Picture' else 'fil',msg['FileName']),msg['FromUserName'])
    return '%s received,Path : %s' % (msg['Type'],file_name)



itchat.auto_login(hotReload=True) 
itchat.run()
