from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import sys

import numpy as np

#from PIL import Image
#Image.MAX_IMAGE_PIXELS = 1000000000
#Image.warnings.simplefilter('error', Image.DecompressionBombWarning)

from scipy.io import loadmat, savemat
from scipy.misc import imread, imsave
from shutil import rmtree
from six.moves import xrange
from skimage.color import label2rgb

from colormap import labelcolormap_level6


def _save_data(image_name_dst, label_name_dst, cmap_name_dst, image_data_dst, label_data_dst):
  cmap = labelcolormap_level6()

  imsave(image_name_dst, image_data_dst)

  mat_data = {}
  mat_data['mask'] = label_data_dst
  savemat(label_name_dst, mat_data, do_compression=True)

  label_mask_cmap = label2rgb(label_data_dst, colors=cmap[1:], bg_label=0)
  label_mask_cmap[label_data_dst == 0] = [0,0,0]
  imsave(cmap_name_dst, label_mask_cmap.astype(np.uint8))


# [1] non-processed
# [2] anticlockwise rotation 90 degree
# [3] anticlockwise rotation 180 degree
# [4] anticlockwise rotation 270 degree
# [5] horizontal flip
# [6] anticlockwise rotation 90 degree + horizontal flip
# [7] anticlockwise rotation 180 degree + horizontal flip
# [8] anticlockwise rotation 270 degree + horizontal flip
def rotate_and_flip(dir_rt, category_name, proc_types):
  dir_src_image = os.path.join(dir_rt, 'crop_fcn_category/image', category_name)
  dir_src_label = os.path.join(dir_rt, 'crop_fcn_category/label', category_name)
  dir_src_cmap  = os.path.join(dir_rt, 'crop_fcn_category/cmap',  category_name)

  file_list = []
  for rt,rt_sub,files in os.walk(dir_src_image):
    file_list.extend(os.path.splitext(os.path.basename(f))[0] for f in files)

  for f in file_list[:]:
    print(f)

    sub_dir = f.split('_')[0]

    image_name_ori = os.path.join(dir_src_image, sub_dir, f+'.jpg')
    label_name_ori = os.path.join(dir_src_label, sub_dir, f+'.mat')

    image_data_ori = imread(image_name_ori)
    label_data_ori = loadmat(label_name_ori)['mask'][...].astype(np.uint8)
   
    # [2] anticlockwise rotation 90 degree
    if 2 in proc_types:
      image_name_dst = os.path.join(dir_src_image, sub_dir, f+'_2.jpg')
      label_name_dst = os.path.join(dir_src_label, sub_dir, f+'_2.mat')
      cmap_name_dst  = os.path.join(dir_src_cmap,  sub_dir, f+'_2.jpg')

      image_data_dst = np.rot90(image_data_ori)
      label_data_dst = np.rot90(label_data_ori)

      _save_data(image_name_dst, label_name_dst, cmap_name_dst, 
                 image_data_dst, label_data_dst)
    # [3] anticlockwise rotation 180 degree
    if 3 in proc_types:
      image_name_dst = os.path.join(dir_src_image, sub_dir, f+'_3.jpg')
      label_name_dst = os.path.join(dir_src_label, sub_dir, f+'_3.mat')
      cmap_name_dst  = os.path.join(dir_src_cmap,  sub_dir, f+'_3.jpg')

      image_data_dst = np.rot90(image_data_ori, 2)
      label_data_dst = np.rot90(label_data_ori, 2)

      _save_data(image_name_dst, label_name_dst, cmap_name_dst, 
                 image_data_dst, label_data_dst)
    # [4] anticlockwise rotation 270 degree
    if 4 in proc_types:
      image_name_dst = os.path.join(dir_src_image, sub_dir, f+'_4.jpg')
      label_name_dst = os.path.join(dir_src_label, sub_dir, f+'_4.mat')
      cmap_name_dst  = os.path.join(dir_src_cmap,  sub_dir, f+'_4.jpg')

      image_data_dst = np.rot90(image_data_ori, 3)
      label_data_dst = np.rot90(label_data_ori, 3)

      _save_data(image_name_dst, label_name_dst, cmap_name_dst,
                 image_data_dst, label_data_dst)
    # [5] horizontal flip
    if 5 in proc_types:
      image_name_dst = os.path.join(dir_src_image, sub_dir, f+'_5.jpg')
      label_name_dst = os.path.join(dir_src_label, sub_dir, f+'_5.mat')
      cmap_name_dst  = os.path.join(dir_src_cmap,  sub_dir, f+'_5.jpg')

      image_data_dst = np.fliplr(image_data_ori)
      label_data_dst = np.fliplr(label_data_ori)

      _save_data(image_name_dst, label_name_dst, cmap_name_dst,
                 image_data_dst, label_data_dst)
    # [6] anticlockwise rotation 90 degree + horizontal flip
    if 6 in proc_types:
      image_name_dst = os.path.join(dir_src_image, sub_dir, f+'_6.jpg')
      label_name_dst = os.path.join(dir_src_label, sub_dir, f+'_6.mat')
      cmap_name_dst  = os.path.join(dir_src_cmap,  sub_dir, f+'_6.jpg')

      image_data_dst = np.fliplr(np.rot90(image_data_ori))
      label_data_dst = np.fliplr(np.rot90(label_data_ori))

      _save_data(image_name_dst, label_name_dst, cmap_name_dst, 
                 image_data_dst, label_data_dst)
    # [7] anticlockwise rotation 180 degree + horizontal flip
    if 7 in proc_types:
      image_name_dst = os.path.join(dir_src_image, sub_dir, f+'_7.jpg')
      label_name_dst = os.path.join(dir_src_label, sub_dir, f+'_7.mat')
      cmap_name_dst  = os.path.join(dir_src_cmap,  sub_dir, f+'_7.jpg')

      image_data_dst = np.fliplr(np.rot90(image_data_ori, 2))
      label_data_dst = np.fliplr(np.rot90(label_data_ori, 2))

      _save_data(image_name_dst, label_name_dst, cmap_name_dst,
                 image_data_dst, label_data_dst)
    # [8] anticlockwise rotation 270 degree + horizontal flip
    if 8 in proc_types:
      image_name_dst = os.path.join(dir_src_image, sub_dir, f+'_8.jpg')
      label_name_dst = os.path.join(dir_src_label, sub_dir, f+'_8.mat')
      cmap_name_dst  = os.path.join(dir_src_cmap,  sub_dir, f+'_8.jpg')

      image_data_dst = np.fliplr(np.rot90(image_data_ori, 3))
      label_data_dst = np.fliplr(np.rot90(label_data_ori, 3))

      _save_data(image_name_dst, label_name_dst, cmap_name_dst,
                 image_data_dst, label_data_dst)


def main():
  dir_rt = sys.argv[1]

  rotate_and_flip(dir_rt, 'nidus1', [2,3,4,5,6,7,8])
  rotate_and_flip(dir_rt, 'nidus2', [2,3,4,5,7])
  rotate_and_flip(dir_rt, 'nidus3', [3,5])
  rotate_and_flip(dir_rt, 'nidus5', [2,3,4,5])


if __name__ == '__main__':
  main()
