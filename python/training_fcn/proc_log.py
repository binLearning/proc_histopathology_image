from __future__ import absolute_import
from __future__ import print_function

import os
import sys
from six.moves import xrange


def main(argv=None):
  log_file = sys.argv[1]
  save_dir = sys.argv[2]

  fp_log = open(log_file, 'r')

  iter_num = 0

  save_path = os.path.join('.', save_dir)
  if not os.path.exists(save_path):
    os.mkdir(save_path)

  save_train_loss = os.path.join(save_path, 'train_loss.txt')
  save_test_loss  = os.path.join(save_path, 'test_loss.txt')
  save_oa_acc     = os.path.join(save_path, 'overall_acc.txt')
  save_mean_acc   = os.path.join(save_path, 'mean_acc.txt')
  save_mean_iu    = os.path.join(save_path, 'mean_iu.txt')
  save_fwavacc    = os.path.join(save_path, 'fwavacc.txt')
  
  fp_train_loss = open(save_train_loss, 'w')
  fp_test_loss  = open(save_test_loss, 'w')
  fp_oa_acc     = open(save_oa_acc, 'w')
  fp_mean_acc   = open(save_mean_acc, 'w')
  fp_mean_iu    = open(save_mean_iu, 'w')
  fp_fwavacc    = open(save_fwavacc, 'w')

  save_form = '{:<10}{}\n'

  train_loss_flag_0 = 'Train net output'
  train_loss_flag_1 = 'loss = '
  train_loss_flag_2 = ' (*'

  test_flag      = '>>> '
  test_loss_flag = ' loss '
  oa_acc_flag    = ' overall accuracy '
  mean_acc_flag  = ' mean accuracy '
  mean_iu_flag   = ' mean IU '
  fwavacc_flag   = ' fwavacc '
  iter_flag      = 'Iteration '

  iter_train = 0
  iter_train_step = 100
  for line_log in fp_log.readlines():
    # train loss
    if line_log.find(train_loss_flag_0) > 0 and line_log.find(train_loss_flag_1) > 0:
      pos_start = line_log.find(train_loss_flag_1) + len(train_loss_flag_1)
      pos_end   = line_log.find(train_loss_flag_2)
      train_loss_info = save_form.format(iter_train, line_log[pos_start:pos_end])
      fp_train_loss.write(train_loss_info)
      iter_train += iter_train_step
    # test loss
    if line_log.find(test_flag) == 0 and line_log.find(test_loss_flag) > 0:
      pos_start = line_log.find(test_loss_flag) + len(test_loss_flag)
      test_loss = line_log[pos_start:-2]
      pos_start = line_log.find(iter_flag) + len(iter_flag)
      pos_end = line_log.find(test_loss_flag)
      iter_cur = line_log[pos_start:pos_end]
      fp_test_loss.write(save_form.format(iter_cur, test_loss))
    # overall accuracy
    if line_log.find(oa_acc_flag) > 0:
      pos_start = line_log.find(oa_acc_flag) + len(oa_acc_flag)
      oa_acc = line_log[pos_start:-2]
      pos_start = line_log.find(iter_flag) + len(iter_flag)
      pos_end = line_log.find(oa_acc_flag)
      iter_cur = line_log[pos_start:pos_end]
      fp_oa_acc.write(save_form.format(iter_cur, oa_acc))
    # mean accuracy
    if line_log.find(mean_acc_flag) > 0:
      pos_start = line_log.find(mean_acc_flag) + len(mean_acc_flag)
      mean_acc = line_log[pos_start:-2]
      pos_start = line_log.find(iter_flag) + len(iter_flag)
      pos_end = line_log.find(mean_acc_flag)
      iter_cur = line_log[pos_start:pos_end]
      fp_mean_acc.write(save_form.format(iter_cur, mean_acc))
    # mean IU
    if line_log.find(mean_iu_flag) > 0:
      pos_start = line_log.find(mean_iu_flag) + len(mean_iu_flag)
      mean_iu = line_log[pos_start:-2]
      pos_start = line_log.find(iter_flag) + len(iter_flag)
      pos_end = line_log.find(mean_iu_flag)
      iter_cur = line_log[pos_start:pos_end]
      fp_mean_iu.write(save_form.format(iter_cur, mean_iu))
    # fwavacc
    if line_log.find(fwavacc_flag) > 0:
      pos_start = line_log.find(fwavacc_flag) + len(fwavacc_flag)
      fwavacc = line_log[pos_start:-2]
      pos_start = line_log.find(iter_flag) + len(iter_flag)
      pos_end = line_log.find(fwavacc_flag)
      iter_cur = line_log[pos_start:pos_end]
      fp_fwavacc.write(save_form.format(iter_cur, fwavacc))

  fp_train_loss.close()
  fp_test_loss.close()
  fp_oa_acc.close()
  fp_mean_acc.close()
  fp_mean_iu.close()
  fp_fwavacc.close()

  fp_log.close()



if __name__ == '__main__':
  main()
