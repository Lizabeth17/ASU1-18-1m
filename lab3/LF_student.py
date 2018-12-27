from pybrain.datasets.supervised import SupervisedDataSet 
from pybrain.tools.shortcuts import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.tools.customxml.networkwriter import NetworkWriter
from pybrain.tools.customxml.networkreader import NetworkReader
import cv2
import numpy as np
import os
from LF_showres import showres
import datetime

datas_count = 0
datas_names = []
datas_hsv = []
cps = []
cps.append('cp1.jpg')
cps.append('cp2.jpg')
#cps.append('cp3.jpg')
#cps.append('cp4.jpg')

def LoadImage(path):
    img = cv2.imread(path)
    img = cv2.resize(img, (650, 485), interpolation = cv2.INTER_CUBIC)
    hsv = np.zeros((650,485,3), np.uint8)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    return hsv.flatten()

def HSVDatas(_s):
    _s = _s[_s.find(':')+1:len(_s):1]
    s1 = _s[0:_s.find('-'):1]
    s2 = _s[_s.find('-')+1:len(_s):1]
    return [int(s1), int(s2)]

def LoadDatas():
    global datas_count
    global datas_names
    global datas_hsv
    f = open('datas.txt', 'r')
    while(True):
        s = f.readline()
        if s == '':
            break
        datas_hsv_temp = []
        s = s[0:len(s)-1:1]
        datas_names.append(s)
        datas_hsv_temp.append(HSVDatas(f.readline()))
        datas_hsv_temp.append(HSVDatas(f.readline()))
        datas_hsv_temp.append(HSVDatas(f.readline()))
        datas_hsv.append(datas_hsv_temp)
        f.readline()
        datas_count += 1

LoadDatas()
dtsi = 0
t = LoadImage(datas_names[0])
net = buildNetwork(len(t), 100, 6)
ds = SupervisedDataSet(len(t), 6)
for datas in datas_names:
    print(datas)
    print(datas_hsv[dtsi])
    datas_hsv_np = np.array(datas_hsv[dtsi])
    print(datas_hsv_np)
    ds.addSample(LoadImage(datas),datas_hsv_np.flatten())
    dtsi += 1

if os.path.isfile('LF_network.xml'):
    print('LF_network.xml exists. Loading net from it')
    net = NetworkReader.readFrom('LF_network.xml')
else:
    print('LF_network.xml doesnt exist. Creating new network')
    trainer = BackpropTrainer(net, ds)
    error = 10
    iteration = 0
    print('Training begins...')
    while error > 0.001: 
        error = trainer.train()
        iteration += 1
        print('Iteration: {0} Error {1}'.format(iteration, error))
    print('Training Done!')
#    NetworkWriter.writeToFile(net, 'LF_network.xml')
#    print('LF_network.xml saved')

now = datetime.datetime.now()
dirnameres = 'results_' + now.strftime("%d-%m-%Y_%H-%M")
os.makedirs(dirnameres)
fileres_learn = open(dirnameres+'/learning_results.txt', 'w')
fileres_cntrl = open(dirnameres+'/control_results.txt', 'w')
netres = []
def saverestofile(ch, datname):
    global dirnameres
    global netres
    Hmin = round(netres[0])
    Hmax = round(netres[1])
    Smin = round(netres[2])
    Smax = round(netres[3])
    Vmin = round(netres[4])
    Vmax = round(netres[5])
    if Hmin < 0:
        Hmin = 0
    if Smin < 0:
        Smin = 0
    if Vmin < 0:
        Vmin = 0
    if Hmax > 255:
        Hmax = 255
    if Smax > 255:
        Smax = 255
    if Vmax > 255:
        Vmax = 255
    if ch == 1:
        with open(dirnameres+'/learning_results.txt', 'a') as fileres_learn:
            print(datname, file=fileres_learn)
            print('h:' + str(Hmin) + '-' + str(Hmax), file=fileres_learn)
            print('s:' + str(Smin) + '-' + str(Smax), file=fileres_learn)
            print('v:' + str(Vmin) + '-' + str(Vmax), file=fileres_learn)
            print(' ', file=fileres_learn)
    else:
        with open(dirnameres+'/control_results.txt', 'a') as fileres_cntrl:
            print(datname, file=fileres_cntrl)
            print('h:' + str(Hmin) + '-' + str(Hmax), file=fileres_cntrl)
            print('s:' + str(Smin) + '-' + str(Smax), file=fileres_cntrl)
            print('v:' + str(Vmin) + '-' + str(Vmax), file=fileres_cntrl)
            print(' ', file=fileres_cntrl)

print('Checking:')
for datas in datas_names:
    netres = net.activate(LoadImage(datas))
    print('\nResult for ' + datas + ': ', netres)
    saverestofile(1, datas)
    cv2.imwrite(dirnameres + '/' + datas, showres(datas, netres))
for datas in cps:
    netres = net.activate(LoadImage(datas))
    print('\nResult for ' + datas + ': ', netres)
    saverestofile(2, datas)
    cv2.imwrite(dirnameres + '/' + datas, showres(datas, netres))

path1 = ''
while(path1 != 'exit'):
    path1 = input('Enter file name(with .jpg) or <exit>: ')
    if (path1 != 'exit'):
        if (os.path.isfile(path1)):
            netres = net.activate(LoadImage(path1))
            print('\nResult for ' + path1 + ': ', netres)
            saverestofile(2, path1)
            if not os.path.isfile(dirnameres + '/' + path1):
                cv2.imwrite(dirnameres + '/' + path1, showres(path1, netres))
            while(1):
                cv2.imshow('result', showres(path1, netres))

                if cv2.waitKey(20) & 0xFF == 27:
                    break
            cv2.destroyAllWindows()
        else:
            print('Error! There is no such file!')
