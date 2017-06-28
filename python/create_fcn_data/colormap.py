import numpy as np


# Get the specified bit value
def _bitget(byteval, idx):
  return ((byteval & (1 << idx)) != 0)

# Create label-color map, label --- [R G B]
def labelcolormap():
  color_map = np.array([ [  0,   0,   0],   # 0 - background
                         [170, 205, 170],   # 1 - normal
                         [245, 165, 205] ]) # 2 - nidus
  return color_map
