#!/usr/bin/python
#-*-encoding:utf-8-*-
import os,sys
import linecache
import ConfigParser
import time
import commands
music_dir = '/Pedro/python/movies/music'
list_file = '/Pedro/python/functions/music_list'

##### update music list ######
def update_music(music_dir=music_dir,list_file=list_file):
    
    pfile=open(list_file,'w')
#    musics = []
    line_num = 0
    lists=os.listdir(music_dir)
    for line in lists:
         if line[-4:] == '.mp3':
             line_num +=1
             pfile.write('%s. %s\n' % (str(line_num),line))
    pfile.close()
    
    return 'There are %d songs / %d Pages in all' % (line_num,line_num/10+1)
#### list music to user ######
def list_music(page='1'):
    pfile=open(list_file)
    lines=len(pfile.readlines())
    pfile.close()    
    songs=''
    
    if page.isdigit() and (int(page)*10<(lines+10))and ((page) > 0):
        for line_num in range((int(page)-1)*10,int(page)*10):
            if line_num <= lines:
                songs+=linecache.getline(list_file,line_num)       
        return songs
    else:
       return "Wrong page number,pls check"
    
#### play music ######
def play_music(number='1'):
    pfile=open(list_file)
    lines=len(pfile.readlines())
    pfile.close()    

    if number.isdigit() and (int(number)<=lines):
        length=len(str(number))+2
        song=linecache.getline(list_file,int(number))[length:]
        os.system('mplayer  \"%s%s\" &' % (music_dir,song[:-1]))#####string song has a '\n'
        return 'Start to play %s' % song[:-1]
    else:
        return "It is not int or out of range"


#### kill the music mpg123  ######
def stop_music():

#    os.system('killall mpg123')
    (status_cmd,output_cmd) = commands.getstatusoutput('killall mplayer')
    if status_cmd != 0:
        return 'Fail to turn off the music'
    return 'Turn off the music Successfully'



#print (list_music('2'))
#print (play_music('2'))
#print(update_music(music_dir,list_file))
#time.sleep(10)
#print(stop_music())
