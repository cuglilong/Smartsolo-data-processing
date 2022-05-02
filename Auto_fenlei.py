from obspy import read
import os
from tokenize import PlainToken
from numpy import kaiser
from shutil import copy
def listdir(path,list_name):
    for file in os.listdir(path):
        file_path = os.path.join(path,file)
        if os.path.isdir(file_path):
            listdir(file_path,list_name)
        else:
            list_name.append(file_path)

def smprocess(path,save_path,No):
    for i in range(0,len(No)):
        read_path = []
        read_path.append(path)
        read_path.append('/')
        read_path.append(No[i])
        read_path = ''.join(read_path)
        sm = []
        listdir(read_path,sm)
        for j in range(0,len(sm)):
            smn = []
            smname = sm[j].split('.')
            smn.append(save_path)
            smn.append('/')
            smn.append(smname[2])
            smn.append('-')
            smn.append(smname[3])
            smn.append('-')
            smn.append(smname[4])
            smn = ''.join(smn)
            if os.path.exists(smn):
                pass
            else:
                os.mkdir(smn)
        for j in range(0,len(sm)):
            smname = sm[j].split('.')
            smn = []
            smn.append(save_path)
            smn.append('/')
            smn.append(smname[2])
            smn.append('-')
            smn.append(smname[3])
            smn.append('-')
            smn.append(smname[4])
            smn = ''.join(smn)
            rename = []
            rename.append(smn)
            rename.append('/')
            rename.append(smname[2])
            rename.append(smname[3])
            rename.append(smname[4])
            rename.append('T')
            rename.append(smname[5])
            rename.append(smname[6])
            rename.append('_')
            rename.append(smname[9])
            rename.append('.miniseed')
            st = read(sm[j])
            st.write(''.join(rename),format='MSEED')
#########################################################
#path smartsolo原始数据所处文件夹
#save_path 处理后储存文件夹
#No 仪器编号
