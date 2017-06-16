/*
 * Create nidus mask
 */

#include <iostream>
#include <fstream>
#include <string>
#include <vector>

#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>

#include "boost_app_fs.h"

typedef unsigned char uchar;

using namespace std;
using namespace cv;


void CreateNidusMask(string dir_src)
{
  string dir_original  = PathJoin(dir_src, "crop/original");
  string dir_annotated = PathJoin(dir_src, "crop/annotated");
  
  string dir_mask_coarse = PathJoin(dir_src, "mask/coarse");
  string dir_mask_fine   = PathJoin(dir_src, "mask/fine");
  
  // visualization
  string dir_redraw = PathJoin(dir_src, "redraw");
  
  CreateDir(dir_mask_coarse);
  CreateDir(dir_mask_fine);
  CreateDir(dir_redraw);
  
  string file_path_info = PathJoin(dir_src, "files.txt");
  ifstream ifs_info(file_path_info.c_str(), ios::in);
  string file_name;
  
  Mat img_original;
  Mat img_annotated;
  Mat img_subtract;
  Mat img_dilate;
  Mat img_threshold;
  Mat img_floodfill;
  Mat img_floodfill_inv;
  Mat img_mask;
  Mat img_erode;
  Mat img_mask_fine;
  
  while (ifs_info.peek() != EOF)
  {
    getline(ifs_info, file_name);
    
    cout << file_name << endl;
    
    string file_path_ori = PathJoin(dir_original,  file_name+".jpg");
    string file_path_ann = PathJoin(dir_annotated, file_name+".jpg");
    
    string file_path_save;
    
    Mat img_original  = imread(file_path_ori, CV_LOAD_IMAGE_COLOR);
    Mat img_annotated = imread(file_path_ann, CV_LOAD_IMAGE_COLOR);
    
    Mat img_gray_ori, img_gray_ann;
    cvtColor(img_original,  img_gray_ori, CV_BGR2GRAY);
    cvtColor(img_annotated, img_gray_ann, CV_BGR2GRAY);
    
    // subtracte images to get annotation lines
    // (original image - annotated image)
    subtract(img_gray_ori, img_gray_ann, img_subtract);
    
    threshold(img_subtract, img_threshold, 30, 255, THRESH_BINARY);
    
    dilate(img_threshold, img_dilate, Mat(), Point(-1,-1), 5);

    img_dilate.copyTo(img_floodfill);
    floodFill(img_floodfill, Point(0,0), 255);
    if (file_name == string("15946-4"))
    {
      Mat img_floodfill_hole;
      img_dilate.copyTo(img_floodfill_hole);
      //floodFill(img_floodfill_hole, Point(6000,900), 255); // original
      floodFill(img_floodfill_hole, Point(4500,900), 255); // crop
      img_floodfill = img_floodfill ^ img_floodfill_hole;
    }
    
    bitwise_not(img_floodfill, img_floodfill_inv);
    
    img_mask = img_dilate | img_floodfill_inv;
    
    erode(img_mask, img_erode, Mat(), Point(-1,-1), 5);
    file_path_save = PathJoin(dir_mask_coarse, file_name+".jpg");
    imwrite(file_path_save, img_erode);
    
    img_erode.copyTo(img_mask_fine);
    
    Mat img_redraw;
    img_annotated.copyTo(img_redraw);
    
    int height = img_redraw.rows;
    int width  = img_redraw.cols;
    
    int pixel_threshold = 230;
    int pixel_subtract  = 50;
    
    for(int row=0; row<height; ++row)
    {
      for(int col=0; col<width; ++col)
      {
        if (img_erode.at<uchar>(row, col) == 255)
        {
          if (img_original.at<Vec3b>(row, col)[0] > pixel_threshold &&
              img_original.at<Vec3b>(row, col)[1] > pixel_threshold &&
              img_original.at<Vec3b>(row, col)[2] > pixel_threshold)
          {
            img_mask_fine.at<uchar>(row, col) = 0;
            continue;
          }
          
          img_redraw.at<Vec3b>(row, col)[0] -= pixel_subtract;
          if (img_redraw.at<Vec3b>(row, col)[0] < 0)
            img_redraw.at<Vec3b>(row, col)[0] = 0;
          img_redraw.at<Vec3b>(row, col)[1] -= pixel_subtract;
          if (img_redraw.at<Vec3b>(row, col)[1] < 0)
            img_redraw.at<Vec3b>(row, col)[1] = 0;
        }
        else
        {
          if (img_original.at<Vec3b>(row, col)[0] > pixel_threshold &&
              img_original.at<Vec3b>(row, col)[1] > pixel_threshold &&
              img_original.at<Vec3b>(row, col)[2] > pixel_threshold)
            continue;
          
          img_redraw.at<Vec3b>(row, col)[0] -= pixel_subtract;
          if (img_redraw.at<Vec3b>(row, col)[0] < 0)
            img_redraw.at<Vec3b>(row, col)[0] = 0;
          img_redraw.at<Vec3b>(row, col)[2] -= pixel_subtract;
          if (img_redraw.at<Vec3b>(row, col)[2] < 0)
            img_redraw.at<Vec3b>(row, col)[2] = 0;
        }
      }
    }
    file_path_save = PathJoin(dir_mask_fine, file_name+".jpg");
    imwrite(file_path_save, img_mask_fine);
    file_path_save = PathJoin(dir_redraw, file_name+".jpg");
    imwrite(file_path_save, img_redraw);
  }
}
