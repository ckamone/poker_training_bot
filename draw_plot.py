#read excel draw plot

#import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import datetime

def getDistance(list):
    #name = input('введите имя файла для чтения данных: ')
    # all_dfs = pd.read_excel(rr+'.xls', sheet_name=None)
    # df2 = pd.read_excel(rr+'.xls', 1) #sheet_name='Results2')
    # all_dfs()
    #mdf = pd.concat(pd.read_excel(name + '.xls', sheet_name=None), ignore_index=True)

    #x = mdf.values[4:, 0]
    #y1 = mdf.values[4:, 2]
    #y2 = mdf.values[4:, 3]
    x=[];y1=[]
    for i in range(len(list)):
        x.append(list[i][0])
        y1.append(list[i][1])

    plt.figure(figsize=(15, 15))
    plt.plot(x, y1, '-', label='your bank')
    #plt.plot(x, y2, '--', label='RX')

    plt.title('bankroll')
    plt.legend()
    plt.grid()
    plt.xlabel('games')
    plt.ylabel('money $')

    #plt.yticks([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25])
    #plt.ticklabel_format(style='sci', axis='x', scilimits=(0, 0))

    #plt.show()
    data=str(datetime.datetime.now())
    data=data[0:-7]
    data=data.replace(' ','_')
    name='plot_'+data+'.png'
    #name.replace(' ','_')
    plt.savefig(name)

    return name