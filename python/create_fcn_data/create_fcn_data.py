from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import sys

import numpy as np

from scipy.io import savemat
from scipy.misc import imread, imsave
from shutil import rmtree
from six.moves import xrange
from skimage.color import label2rgb

from colormap import labelcolormap


def main():
  dir_rt = sys.argv[1]
  dir_ori  = os.path.join(dir_rt, 'crop/original')
  dir_mask = os.path.join(dir_rt, 'mask/fine')
  dir_dst_image = os.path.join(dir_rt, 'crop_fcn/image')
  dir_dst_label = os.path.join(dir_rt, 'crop_fcn/label')
  dir_dst_cmap  = os.path.join(dir_rt, 'crop_fcn/cmap')
  
  if os.path.exists(dir_dst_image):
    rmtree(dir_dst_image)
  os.makedirs(dir_dst_image)
  if os.path.exists(dir_dst_label):
    rmtree(dir_dst_label)
  os.makedirs(dir_dst_label)
  if os.path.exists(dir_dst_cmap):
    rmtree(dir_dst_cmap)
  os.makedirs(dir_dst_cmap)
  
  SPLIT_NUM = 10
  BG_PIXEL_VALUE = 230
  
  fp_info = open(os.path.join(dir_rt, 'fcn_info_train.txt'), 'w')
  
  cmap = labelcolormap()
  
  with open(os.path.join(dir_rt, 'files_train.txt')) as fp_files:
    for each_line in fp_files.readlines():
      file_name = each_line.strip()
      
      sub_dir_image = os.path.join(dir_dst_image, file_name)
      sub_dir_label = os.path.join(dir_dst_label, file_name)
      sub_dir_cmap  = os.path.join(dir_dst_cmap, file_name)
      
      if not os.path.exists(sub_dir_image):
        os.makedirs(sub_dir_image)
      if not os.path.exists(sub_dir_label):
        os.makedirs(sub_dir_label)
      if not os.path.exists(sub_dir_cmap):
        os.makedirs(sub_dir_cmap)
  
      file_path_ori  = os.path.join(dir_ori,  file_name+'.jpg')
      file_path_mask = os.path.join(dir_mask, file_name+'.jpg')
  
      image_ori  = imread(file_path_ori)
      image_mask = imread(file_path_mask, mode='P')
      
      height = image_ori.shape[0]
      width  = image_ori.shape[1]
      
      h_step = height // SPLIT_NUM
      w_step = width // SPLIT_NUM
      
      invalid_num_threshold = h_step * w_step * 0.95
      
      cnt = 1
      label_mask_data = np.zeros((h_step,w_step), dtype='uint8')
      for h_num in xrange(SPLIT_NUM):
        h_start = h_step * h_num
        h_end   = h_step * (h_num + 1)
        
        for w_num in xrange(SPLIT_NUM):
          w_start = w_step * w_num
          w_end   = w_step * (w_num + 1)
          
          image_crop_ori  = image_ori[h_start:h_end,w_start:w_end,:]
          image_crop_mask = image_mask[h_start:h_end,w_start:w_end]
          
          invalid_num = 0
          for row in xrange(h_step):
            for col in xrange(w_step):
              if image_crop_mask[row,col] > 100:
                label_mask_data[row,col] = 2 # niuds
              elif image_crop_ori[row,col,0] > BG_PIXEL_VALUE and \
                   image_crop_ori[row,col,1] > BG_PIXEL_VALUE and \
                   image_crop_ori[row,col,2] > BG_PIXEL_VALUE:
                label_mask_data[row,col] = 0 # background
                invalid_num += 1
              else:
                label_mask_data[row,col] = 1 # normal
          
          if invalid_num > invalid_num_threshold:
            continue
          
          mat_data = {}
          mat_data['mask'] = label_mask_data
          
          dst_file_label = '{}_{:0>3}.mat'.format(file_name, cnt)
          savemat(os.path.join(sub_dir_label,dst_file_label), mat_data,
                  do_compression=True)
          
          dst_file_image = '{}_{:0>3}.jpg'.format(file_name, cnt)
          imsave(os.path.join(sub_dir_image,dst_file_image), image_crop_ori)
          
          label_mask_cmap = label2rgb(label_mask_data, colors=cmap[1:], bg_label=0)
          label_mask_cmap[label_mask_data == 0] = [255,255,255]
          imsave(os.path.join(sub_dir_cmap,dst_file_image),
                 label_mask_cmap.astype(np.uint8))
          
          cnt += 1
      
      info = '{:<9} {:<5} {:<5} {}\n'.format(file_name, h_step, w_step, cnt-1)
      fp_info.write(info)
      
      print(info)
      
    fp_info.close()
    

if __name__ == '__main__':
  main()
