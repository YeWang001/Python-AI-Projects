from matplotlib import pyplot as plt
import matplotlib

font = {'family' : 'MicroSoft YaHei',
        'weight' : 'bold',
        'size'   : '12'}
matplotlib.rc('font', **font)

x = range(11,31)
y = [1,0,1,1,2,4,3,2,3,4,4,5,6,5,4,3,3,1,1,1]

#设置图形大小
plt.figure(figsize=(20,8), dpi=80)

plt.plot(x,y)

#设置x轴刻度
_xticks_labels=['{}岁'.format(i) for i in x]
plt.xticks(x, _xticks_labels)
plt.yticks(range(0,9))

#绘制网格
plt.grid(alpha=0.1)

plt.show()
