import os

import matplotlib.pyplot as plt
import numpy as np


xlim_left  = -1000
xlim_right = 101000
info_dir   = 'info/1.0'
draw_label = '1.0'

fig = plt.figure()
fig.set_size_inches(16, 16)

#list_color = ['deepskyblue', 'orange', 'purple', 'hotpink', 'seagreen']

'''============================================================================
                             train/test loss
============================================================================'''
ax1 = fig.add_subplot(211)
ax1.set_title('loss', fontsize=16)
ax1.grid(True)

ylim_bottom = -0.1
ylim_top    = 8.1
ax1.set_xlim(xlim_left, xlim_right)
ax1.set_ylim(ylim_bottom,ylim_top)

data_test_loss  = np.loadtxt(os.path.join(info_dir, 'test_loss.txt'))
data_train_loss = np.loadtxt(os.path.join(info_dir, 'train_loss.txt'))

label_test_loss  = 'test_loss_' + draw_label
label_train_loss = 'train_loss_' + draw_label

ax1.plot(data_test_loss[:,0], data_test_loss[:,1], linewidth=1,
         color='deepskyblue', linestyle='-', label=label_test_loss)
#ax1.scatter(data_test_loss[:,0], data_test_loss[:,1], 20, marker='o', c='deepskyblue')
ax1.plot(data_train_loss[:,0], data_train_loss[:,1], linewidth=1.5,
         color='orange', linestyle='-', label=label_train_loss)
#ax1.scatter(data_train_loss[:,0], data_train_loss[:,1], 20, marker='o', c='orange')

ax1.legend(loc='upper right', fontsize=14)
'''============================================================================
                             test accuracy
============================================================================'''
ax1 = fig.add_subplot(212)
ax1.set_title('accuracy', fontsize=16)
ax1.grid(True)

ylim_bottom = -0.01
ylim_top    = 1.01
ax1.set_xlim(xlim_left, xlim_right)
ax1.set_ylim(ylim_bottom,ylim_top)

data_test_acc  = np.loadtxt(os.path.join(info_dir, 'test_acc.txt'))
  
label_test_acc  = 'test_acc_' + draw_label

ax1.plot(data_test_acc[:,0], data_test_acc[:,1], linewidth=1,
         color='deepskyblue', linestyle='-', label=label_test_acc)
ax1.scatter(data_test_acc[:,0], data_test_acc[:,1], 20, marker='o', c='deepskyblue')

nparr_test_acc = np.array(data_test_acc[:,1])
max_value_index = nparr_test_acc.argmax()
point_x = data_test_acc[:,0][max_value_index]
point_y = data_test_acc[:,1][max_value_index]
ax1.scatter(point_x, point_y, 50, marker='o', c='hotpink')
ax1.annotate('MAX (%d, %.3f)' % (point_x, point_y), xy=(point_x,point_y), 
             xycoords='data', xytext=(3,3),
             textcoords='offset points', fontsize=14,
             color='hotpink')
         
ax1.legend(loc='lower right', fontsize=14)
