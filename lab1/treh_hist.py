import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime as dt
import csv

def treh_hist(_x, _y, _z, flname):
    try:
        dpi = 80
        fig = plt.figure(dpi = dpi, figsize = (512 / dpi, 384 / dpi) )
        mpl.rcParams.update({'font.size': 10})

        plt.title('Процент совпадения размера стихотворения с эталонами')

        #рисуем три бара
        plt.bar(0, _x,
                width = 1, color = 'red', label = 'анапест',
                zorder = 2)
        plt.bar(1, _y,
                width = 1, color = 'blue', label = 'амфибрахий',
                zorder = 2)
        plt.bar(2, _z,
                width = 1, color = 'green', label = 'дактиль',
                zorder = 2)

        #убираем подписи по оси х
        data_names = ['']
        xs = range(len(data_names))
        plt.xticks(xs, data_names)

        plt.legend(loc='upper right') #где писать легенду
        #plt.show()
        plt.savefig(flname)
    except MatplotlibDeprecationWarning:
        print('')
    return True

