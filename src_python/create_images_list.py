import os
import random
import sys


def main():
  dir_src = sys.argv[1]
  
  info_file_test  = 'images_test.txt'
  info_file_train = 'images_train.txt'

  dir_src_nidus  = os.path.join(dir_src, 'nidus')
  dir_src_normal = os.path.join(dir_src, 'normal')

  list_subdirs_nidus  = [dirs for dirs in os.listdir(dir_src_nidus)]
  list_subdirs_normal = [dirs for dirs in os.listdir(dir_src_normal)]
  
  #select nidus samples -------------------------------------------------------
  NUM_NIDUS_COARSE = 50
  NUM_NIDUS_FINE   = 1500
  
  nidus_test_coarse = []
  nidus_train = []
  
  for subdir in list_subdirs_nidus:
    for rt,_,files in os.walk(os.path.join(dir_src_nidus, subdir)):
      random.shuffle(files)
      nidus_test_coarse.extend(os.path.join(rt,f) for f in files[:NUM_NIDUS_COARSE])
      if len(files) > NUM_NIDUS_COARSE:
        nidus_train.extend(os.path.join(rt,f) for f in files[NUM_NIDUS_COARSE:])
  
  random.shuffle(nidus_test_coarse)
  nidus_test_fine = nidus_test_coarse[:NUM_NIDUS_FINE]
  nidus_train.extend(nidus_test_coarse[NUM_NIDUS_FINE:])
  
  #select normal samples ------------------------------------------------------
  NUM_NORMAL_COARSE = 500
  NUM_NORMAL_FINE   = 8500
  
  normal_test_coarse = []
  normal_train = []
  
  for subdir in list_subdirs_normal:
    for rt,_,files in os.walk(os.path.join(dir_src_normal, subdir)):
      random.shuffle(files)
      normal_test_coarse.extend(os.path.join(rt,f) for f in files[:NUM_NORMAL_COARSE])
      if len(files) > NUM_NORMAL_COARSE:
        normal_train.extend(os.path.join(rt,f) for f in files[NUM_NORMAL_COARSE:])
  
  random.shuffle(normal_test_coarse)
  normal_test_fine = normal_test_coarse[:NUM_NORMAL_FINE]
  normal_train.extend(normal_test_coarse[NUM_NORMAL_FINE:])
  
  # combine -------------------------------------------------------------------
  files_test  = nidus_test_fine + normal_test_fine
  files_train = nidus_train + normal_train
  
  random.shuffle(files_test)
  random.shuffle(files_train)
  
  with open(info_file_test, 'w') as f_test:
    for f in files_test:
      label = 0
      if 'nidus' in f:
        label = 1
      f_test.write('{} {}\n'.format(f, label)) # NOTE
  
  with open(info_file_train, 'w') as f_train:
    for f in files_train:
      label = 0
      if 'nidus' in f:
        label = 1
      f_train.write('{} {}\n'.format(f, label)) # NOTE


if __name__ == '__main__':
  main()


# NOTE
# There is only one space, otherwise Caffe will be given errors:
# Could not open or find file xxx.jpg
# Check failed: cv_img.data Could not load xxx.jpg
