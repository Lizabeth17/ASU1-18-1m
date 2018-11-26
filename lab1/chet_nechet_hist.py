import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime as dt
import csv

def chet_nechet_hist(_x, _y):
    try:
        dpi = 80
        fig = plt.figure(dpi = dpi, figsize = (512 / dpi, 384 / dpi) )
        mpl.rcParams.update({'font.size': 10})

        plt.title('Количество ударных слогов в стихотворении')

        #рисуем два бара
        plt.bar(0, _x,
                width = 1, color = 'red', label = 'четные',
                zorder = 2)
        plt.bar(1, _y,
                width = 1, color = 'blue', label = 'нечетные',
                zorder = 2)

        #убираем подписи по оси х
        data_names = ['']
        xs = range(len(data_names))
        plt.xticks(xs, data_names)

        plt.legend(loc='upper right') #где писать легенду
        plt.show()
    except MatplotlibDeprecationWarning:
        print('')
    return True
