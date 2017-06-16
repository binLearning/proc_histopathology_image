/*
 * Select training sample
 */

#include <iostream>
#include <fstream>
#include <string>
#include <vector>

#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>

#include <boost/format.hpp>
#include <boost/lexical_cast.hpp>

#include "boost_app_fs.h"

using namespace std;
using namespace cv;


void SelectTrainSample(string dir_src)
{
  string dir_original  = PathJoin(dir_src, "crop/original");
  string dir_mask_fine = PathJoin(dir_src, "mask/fine");
  
  string dir_sample_normal = PathJoin(dir_src, "sample/normal");
  string dir_sample_nidus  = PathJoin(dir_src, "sample/nidus");
  
  CreateDir(dir_sample_normal);
  CreateDir(dir_sample_nidus);
  
  string file_path_info = PathJoin(dir_src, "files.txt");
  ifstream ifs_info(file_path_info.c_str(), ios::in);

  string file_path_distribution = PathJoin(dir_src, "sample/sample_distribution.txt");
  ofstream ofs_distribution(file_path_distribution.c_str(), ios::out);

  boost::format out_fmt_sss("%-10s   %-10s   %-10s");
  boost::format out_fmt_sdd("%-10s   %-10d   %-10d");
  ofs_distribution << out_fmt_sss % "file" % "#nidus" % "#normal" << endl << endl;
  
  const int PIXEL_VALUE_THRESHOLD   = 240;
  const int SAMPLE_SIZE             = 224;
  const int SLIDING_STEP            = 32;
  
  const int NUMBER_THRESHOLD_VALID  = 10000; // 224*224*0.2 = 10035.2
  const int NUMBER_THRESHOLD_NIDUS  = 30000; // 224*224*0.6 = 30105.6
  const int NUMBER_THRESHOLD_NORMAL = 5000;  // 224*224*0.1 = 5017.6
  
  const int RANDOM_SELECT_MAX_NUM   = 10000;
  
  int total_num_invalid = 0;
  int total_num_normal  = 0;
  int total_num_nidus   = 0;
  
  string file_name;
  string file_path_save;
  
  while (ifs_info.peek() != EOF)
  {
    getline(ifs_info, file_name);
    //if (file_name != string("13052-2")) continue;
    
    int num_invalid = 0;
    int num_normal  = 0;
    int num_nidus   = 0;
    
    string sub_dir_normal = PathJoin(dir_sample_normal, file_name);
    string sub_dir_nidus  = PathJoin(dir_sample_nidus, file_name);
  
    CreateDir(sub_dir_normal);
    CreateDir(sub_dir_nidus);
    
    string file_path_ori  = PathJoin(dir_original,  file_name+".jpg");
    string file_path_mask = PathJoin(dir_mask_fine, file_name+".jpg");
    
    Mat img_original = imread(file_path_ori, CV_LOAD_IMAGE_COLOR);
    Mat img_mask     = imread(file_path_mask, CV_LOAD_IMAGE_GRAYSCALE);
    
    Mat img_gray_ori;
    cvtColor(img_original, img_gray_ori, CV_BGR2GRAY);

    Mat img_valid = img_gray_ori < PIXEL_VALUE_THRESHOLD;

    int height = img_original.rows;
    int width  = img_original.cols;
    int height_th = height - SAMPLE_SIZE;
    int width_th  = width  - SAMPLE_SIZE;
    
    Rect rect_select;
    rect_select.width  = SAMPLE_SIZE;
    rect_select.height = SAMPLE_SIZE;
    
    // sliding window
    for (int row = 0; row < height_th; row += SLIDING_STEP)
    {
      for (int col = 0; col < width_th; col += SLIDING_STEP)
      {
        rect_select.x = col;
        rect_select.y = row;
        
        Mat img_select_valid = img_valid(rect_select);
        int num_pixel_valid = countNonZero(img_select_valid);
        if (num_pixel_valid < NUMBER_THRESHOLD_VALID)
        {
          ++num_invalid;
          continue;
        }
        
        Mat img_select_mask = img_mask(rect_select);
        Mat img_select_ori  = img_original(rect_select);
        
        int num_pixel_mask = countNonZero(img_select_mask);
        if (num_pixel_mask > NUMBER_THRESHOLD_NIDUS)
        {
          ++num_nidus;
          
          file_path_save = PathJoin(sub_dir_nidus,
                                    boost::lexical_cast<string>(num_nidus)+".jpg");
          imwrite(file_path_save, img_select_ori);
        }
        else if (num_pixel_mask < NUMBER_THRESHOLD_NORMAL)
        {
          ++num_normal;
          
          file_path_save = PathJoin(sub_dir_normal,
                                    boost::lexical_cast<string>(num_normal)+".jpg");
          imwrite(file_path_save, img_select_ori);
        }
      }
    }
     
    // random select
    for (int num = 0; num < RANDOM_SELECT_MAX_NUM; ++num)
    {
      rect_select.x = rand() % width_th;
      rect_select.y = rand() % height_th;
      
      Mat img_select_valid = img_valid(rect_select);
      int num_pixel_valid = countNonZero(img_select_valid);
      if (num_pixel_valid < NUMBER_THRESHOLD_VALID)
      {
        ++num_invalid;
        continue;
      }
      
      Mat img_select_mask = img_mask(rect_select);
      Mat img_select_ori = img_original(rect_select);
      
      int num_pixel_mask = countNonZero(img_select_mask);
      if (num_pixel_mask > NUMBER_THRESHOLD_NIDUS)
      {
        ++num_nidus;
        
        file_path_save = PathJoin(sub_dir_nidus,
                                  boost::lexical_cast<string>(num_nidus)+".jpg");
        imwrite(file_path_save, img_select_ori);
      }
      else if (num_pixel_mask < NUMBER_THRESHOLD_NORMAL)
      {
        ++num_normal;
        
        file_path_save = PathJoin(sub_dir_normal,
                                  boost::lexical_cast<string>(num_normal)+".jpg");
        imwrite(file_path_save, img_select_ori);
      }
    }

    cout << out_fmt_sdd % file_name % num_nidus % num_normal << endl;

    ofs_distribution << out_fmt_sdd % file_name % num_nidus % num_normal << endl;

    total_num_nidus   += num_nidus;
    total_num_normal  += num_normal;
    total_num_invalid += num_invalid;
  }

  cout << out_fmt_sdd % "total" % total_num_nidus % total_num_normal << endl;

  ofs_distribution << endl;
  ofs_distribution << out_fmt_sdd % "total" % total_num_nidus % total_num_normal << endl;

  ifs_info.close();
  ofs_distribution.close();
}
