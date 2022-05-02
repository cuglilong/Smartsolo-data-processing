import csv
import os
from obspy.geodetics import gps2dist_azimuth,kilometers2degrees
from obspy.taup import TauPyModel
import os
from tokenize import PlainToken
from obspy.core import read
import numpy as np
from obspy import UTCDateTime, read, Trace, Stream
import sys
import glob
import subprocess
from obspy.core import UTCDateTime
#csv 仪器所记载时间内catalog文件所处路径
#path 提取P波后所存储位置
def catalogread(csv,path):
    csv_file = csv.reader(open(csv))
    print(csv_file)
    seismo =[]
    for seism in csv_file:
        seismo.append(seism)
    for i in range(0,len(seismo)):
        pathmk = []
        pathmk.append(path)
        pathmk.append('/')
        pathmk.append(str(i+1))
        pathmk = ''.join(pathmk)
        print(pathmk)
        if os.path.exists(pathmk):
            pass
        else:
            os.mkdir(pathmk)
    return seismo
#path1 统一时间文件格式后smartsolo文件所处路径
#save_path 存储路径
def Pwaveget(stla,stlo,seismo,path1,save_path,):
    last = ['_E.miniseed','_N.miniseed','_Z.miniseed']
    last1 = ['_E.sac','_N.sac','_Z.sac']
    starttime = []
    evla = []
    evlo = []
    depth = []
    for i in range(0,len(seismo)):
        starttime.append(seismo[i][0])
        evla.append(float(seismo[i][1]))
        evlo.append(float(seismo[i][2]))
        depth.append(float(seismo[i][3]))
    pt = []#P wave travel time
    for i in range(0,len(seismo)):
        dist,az,baz = gps2dist_azimuth(evla[i],evlo[i],stla,stlo)
        dist /= 1000.0
        gcarc = kilometers2degrees(dist)
        model = TauPyModel(model="iasp91")
        pt.append(model.get_travel_times(depth[i],gcarc)[0].time)
    sttime = []
    begin = []
    end = []
    for i in range(0,len(starttime)):
        time = UTCDateTime(starttime[i])
        timebegin = time+pt[i]-60
        timeend = time+pt[i]+240
        sttime.append(time)
        begin.append(timebegin)
        end.append(timeend)
        time_title = []
        time_title_list = []
    for i in range(0,len(starttime)):
        stt = []
        sttt = starttime[i].split(':')[0].split('-')
        stt.append(sttt[0])
        stt.append(sttt[1])
        stt.append(sttt[2])
        stt.append('00')
        time_title_list.append(stt)
        time_title.append(''.join(stt))
    startmin = []
    for i in range(0,len(starttime)):
        min = starttime[i].split(':')[1]
        startmin.append(int(min))
    
    for i in range(0,len(starttime)):
        date = starttime[i].split('T')[0]
        pathsm = []
        pathsm.append(path1)
        pathsm.append('/')
        pathsm.append(date)
        pathsm = ''.join(pathsm)
        if startmin[i] < 30:
            for j in range(0,len(last)):
                pathsm1 = []
                pathsm1.append(pathsm)
                pathsm1.append('/')
                pathsm1.append(time_title[i])
                pathsm1.append(last[j])           
                st = read(''.join(pathsm1))
                tr = st[0]
                b = begin[i]
                e = end[i]
                tr1 = tr.trim(b,e)
                st = Stream(tr1)
                fl = []
                fl.append(save_path)
                fl.append('/')
                fl.append(str(i+1))
                fl.append('/')
                fl.append('smartsolo_')
                fl.append(str(i+1))
                fl.append(last1[j])
                st.write(''.join(fl),format='SAC')
        else:
            for j in range(0,len(last)):
                pathsm1 = []
                pathsm1.append(pathsm)
                pathsm1.append('/')
                pathsm1.append(time_title[i])
                pathsm1.append(last[j])
                pathsm2 = []
                pathsm2.append(pathsm)
                pathsm2.append('/')
                t = int(time_title_list[i][2].split('T')[1])+1
                time2_title = []
                time2_title.append(time_title_list[i][0])
                time2_title.append(time_title_list[i][1])
                time2_title.append(time_title_list[i][2].split('T')[0])
                time2_title.append('T')
                if t<10:
                    time2_title.append('0')
                time2_title.append(str(t))
                time2_title.append('00')
                pathsm2.append(''.join(time2_title))
                pathsm2.append(last[j])
                st = read(''.join(pathsm1))
                st += read(''.join(pathsm2))
                st.merge(method=1,fill_value=0)
                tr = st[0]
                b = begin[i]
                e = end[i]
                tr1 = tr.trim(b,e)
                st = Stream(tr1)
                fl = []
                fl.append(save_path)
                fl.append('/')
                fl.append(str(i+1))
                fl.append('/')
                fl.append('smartsolo_')
                fl.append(str(i+1))
                fl.append(last1[j])
                st.write(''.join(fl),format='SAC')

