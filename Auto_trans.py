import os
import sys
import glob
import subprocess

os.putenv("SAC_DISPLAY_COPYRIGHT","0")
path = ''#所需要去除仪器响应的原始数据路径
os.chdir(path)
s = ""
for sacfile in glob.glob("*.sac"):
    Pz = ''#仪器响应文件所处路径
    s += "r {}\n".format(sacfile)
    s += "rmean;rtr;taper\n"
    s += "trans from polezero subtype {} to none freq 0.01 0.02 20 22\n".format(Pz)
    s += "mul 1.0e9\n"
    s += "w over\n"
s += "q\n"
subprocess.Popen(['sac'],stdin=subprocess.PIPE).communicate(s.encode())
print('finished!')