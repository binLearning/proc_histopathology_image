/*
 * MAIN
 */

#include <iostream>
#include <string>
#include <vector>

#include "create_file_list.h"
#include "crop_valid_area.h"
#include "create_nidus_mask.h"
#include "select_train_sample.h"

using namespace std;


int main()
{
  string dir_src("../images");

  CreateFileList(dir_src);
  CropValidArea(dir_src);
  CreateNidusMask(dir_src);
  SelectTrainSample(dir_src);
  
  return 0;
}
