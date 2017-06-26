import os
import sys
from six.moves import xrange


def main(argv=None):
  log_file = sys.argv[1]
  save_dir = sys.argv[2]

  fp_log = open(log_file, 'r')

  save_path = os.path.join('.', save_dir)
  if not os.path.exists(save_path):
    os.mkdir(save_path)

  save_file_test_acc   = os.path.join(save_path, 'test_acc.txt')
  save_file_test_loss  = os.path.join(save_path, 'test_loss.txt')
  save_file_train_loss = os.path.join(save_path, 'train_loss.txt')

  fp_test_acc   = open(save_file_test_acc, 'w')
  fp_test_loss  = open(save_file_test_loss, 'w')
  fp_train_loss = open(save_file_train_loss, 'w')

  flag_test_acc   = 'Test net output #0: accuracy = '
  flag_test_loss  = 'Test net output #1: loss = '
  flag_train_loss = 'Train net output #0: loss = '
  end_flag = ' (*'

  iter_num_test   = 0
  iter_step_test  = 2500
  iter_num_train  = 0
  iter_step_train = 500

  for line_log in fp_log.readlines():
    # test accuracy
    if line_log.find(flag_test_acc) > 0:
      pos_start = line_log.find(flag_test_acc) + len(flag_test_acc)
      fp_test_acc.write('{}   {}'.format(iter_num_test, line_log[pos_start:]))
    # test loss
    if line_log.find(flag_test_loss) > 0:
      pos_start = line_log.find(flag_test_loss) + len(flag_test_loss)
      pos_end = line_log.find(end_flag)
      fp_test_loss.write('{}   {}\n'.format(iter_num_test, line_log[pos_start:pos_end]))
      iter_num_test += iter_step_test
    # train loss
    if line_log.find(flag_train_loss) > 0:
      pos_start = line_log.find(flag_train_loss) + len(flag_train_loss)
      pos_end = line_log.find(end_flag)
      fp_train_loss.write('{}   {}\n'.format(iter_num_train, line_log[pos_start:pos_end]))
      iter_num_train += iter_step_train

  fp_test_acc.close()
  fp_test_loss.close()
  fp_train_loss.close()
  fp_log.close()


if __name__ == '__main__':
  main()
