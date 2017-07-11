import os

import matplotlib.pyplot as plt
import numpy as np

xlim_left  = -1000
xlim_right = 1905000

fig = plt.figure()
fig.set_size_inches(18, 16)

list_color = ['deepskyblue', 'orangered', 'green', 'purple']

info_dir = 'fcn_resnet_50_1.0'


'''============================================================================
                               train/test loss
============================================================================'''
ax1 = fig.add_subplot(211)
ax1.set_title('loss', fontsize=15)
ax1.set_xlim(xlim_left, xlim_right)
ax1.set_ylim(0, 850000)
ax1.grid(True)

data_info = np.loadtxt(os.path.join(info_dir, 'train_loss.txt'))
ax1.plot(data_info[:,0], data_info[:,1],
         color=list_color[0], linestyle='-', label='train loss')

data_info = np.loadtxt(os.path.join(info_dir, 'test_loss.txt'))
ax1.plot(data_info[:,0], data_info[:,1], linewidth=1.5, 
         color=list_color[1], linestyle='-', label='test loss')
min_value_index = data_info[:,1].argmin()
point_x = data_info[min_value_index, 0]
point_y = data_info[min_value_index, 1]
ax1.scatter(point_x, point_y, 60, marker='o', c=list_color[1])
ax1.annotate('MIN(%d, %.3f)' % (point_x, point_y), xy=(point_x,point_y), 
             xycoords='data', xytext=(-5, -15),
             textcoords='offset points', fontsize=15,
             color=list_color[1])

ax1.legend(loc='upper right', fontsize=15)

'''============================================================================
                              various indicator
============================================================================'''
ax1 = fig.add_subplot(212)
ax1.set_title('various indicator', fontsize=15)
ax1.set_xlim(xlim_left, xlim_right)
ax1.set_ylim(0, 1)
ax1.grid(True)

data_info = np.loadtxt(os.path.join(info_dir, 'overall_acc.txt'))
ax1.plot(data_info[:,0], data_info[:,1], color=list_color[0], 
         linewidth=1.5, linestyle='-', label='overall accuracy')
max_value_index = data_info[:,1].argmax()
point_x = data_info[max_value_index, 0]
point_y = data_info[max_value_index, 1]
ax1.scatter(point_x, point_y, 60, marker='o', c=list_color[0])
ax1.annotate('MAX(%d, %.3f)' % (point_x, point_y), xy=(point_x,point_y), 
             xycoords='data', xytext=(-5, +10),
             textcoords='offset points', fontsize=15,
             color=list_color[0])

data_info = np.loadtxt(os.path.join(info_dir, 'mean_acc.txt'))
ax1.plot(data_info[:,0], data_info[:,1], color=list_color[1], 
         linewidth=1.5, linestyle='-', label='mean accuracy')
max_value_index = data_info[:,1].argmax()
point_x = data_info[max_value_index, 0]
point_y = data_info[max_value_index, 1]
ax1.scatter(point_x, point_y, 60, marker='o', c=list_color[1])
ax1.annotate('MAX(%d, %.3f)' % (point_x, point_y), xy=(point_x,point_y), 
             xycoords='data', xytext=(-5, +22),
             textcoords='offset points', fontsize=15,
             color=list_color[1])

data_info = np.loadtxt(os.path.join(info_dir, 'mean_iu.txt'))
ax1.plot(data_info[:,0], data_info[:,1], color=list_color[2], 
         linewidth=1.5, linestyle='-', label='mean IU')
max_value_index = data_info[:,1].argmax()
point_x = data_info[max_value_index, 0]
point_y = data_info[max_value_index, 1]
ax1.scatter(point_x, point_y, 60, marker='o', c=list_color[2])
ax1.annotate('MAX(%d, %.3f)' % (point_x, point_y), xy=(point_x,point_y), 
             xycoords='data', xytext=(-5, +10),
             textcoords='offset points', fontsize=15,
             color=list_color[2])

data_info = np.loadtxt(os.path.join(info_dir, 'fwavacc.txt'))
ax1.plot(data_info[:,0], data_info[:,1], color=list_color[3], 
         linewidth=1.5, linestyle='-', label='fwavacc')
max_value_index = data_info[:,1].argmax()
point_x = data_info[max_value_index, 0]
point_y = data_info[max_value_index, 1]
ax1.scatter(point_x, point_y, 60, marker='o', c=list_color[3])
ax1.annotate('MAX(%d, %.3f)' % (point_x, point_y), xy=(point_x,point_y), 
             xycoords='data', xytext=(-5, +25),
             textcoords='offset points', fontsize=15,
             color=list_color[3])

ax1.legend(loc='lower right', fontsize=15)
