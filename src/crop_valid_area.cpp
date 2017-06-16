/*
 * Crop valid area
 */

#include <algorithm>
#include <fstream>
#include <iostream>
#include <string>
#include <vector>

#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>

#include "boost_app_fs.h"
#include "crop_valid_area.h"

using namespace std;
using namespace cv;


Rect ContainAll(vector<Rect> vec_rect, int width, int height);


void CropValidArea(string dir_src)
{
  string dir_original  = PathJoin(dir_src, "original");
  string dir_annotated = PathJoin(dir_src, "annotated");
  
  string dir_crop_ori  = PathJoin(dir_src, "crop/original");
  string dir_crop_ann  = PathJoin(dir_src, "crop/annotated");
  
  CreateDir(dir_crop_ori);
  CreateDir(dir_crop_ann);
  
  string file_path_info = PathJoin(dir_src, "files.txt");
  ifstream ifs_info(file_path_info.c_str(), ios::in);
  string file_name;
  
  while (ifs_info.peek() != EOF)
  {
    getline(ifs_info, file_name);
    //if (file_name != string("14298")) continue;
    
    cout << file_name << endl;
    
    string file_path_ori = PathJoin(dir_original,  file_name+".jpg");
    string file_path_ann = PathJoin(dir_annotated, file_name+"_annotated.jpg");
    
    Mat img_original  = imread(file_path_ori, CV_LOAD_IMAGE_COLOR);
    Mat img_annotated = imread(file_path_ann, CV_LOAD_IMAGE_COLOR);
    
    Mat img_gray_ori;
    cvtColor(img_original,  img_gray_ori, CV_BGR2GRAY);
    
    Mat img_canny;
    Canny(img_gray_ori, img_canny, 0, 255, 3);
    
    // solution #2
    //Mat img_dilate;
    //dilate(img_canny, img_dilate, Mat(), Point(-1,-1), 3);
    
    //Mat img_erode;
    //erode(img_dilate, img_erode, Mat(), Point(-1,-1), 5);
    
    vector<vector<Point> > contours;
    findContours(img_canny, contours, CV_RETR_EXTERNAL, CV_CHAIN_APPROX_NONE);

    vector<Point> vec_all_points;
    vector<vector<Point> >::iterator iter = contours.begin();
    for( ; iter != contours.end(); ++iter)
    {
      vec_all_points.insert(vec_all_points.end(), iter->begin(), iter->end());
    }
    
    Rect rect_crop = boundingRect(vec_all_points);
    
    /*
    // solution #1
    Mat img_dilate;
    dilate(img_canny, img_dilate, Mat(), Point(-1,-1), 20);
    
    vector<vector<Point> > contours;
    findContours(img_dilate, contours, CV_RETR_EXTERNAL, CV_CHAIN_APPROX_NONE);
    
    // get first two maximum contour
    vector<int> vec_contour_area;
    for(int idx=0; idx<contours.size(); ++idx)
    {
      int area_val = contourArea(contours[idx]);
      vec_contour_area.push_back(area_val);
    }
    
    int max_area_val[2] = {0};
    int max_area_idx[2] = {-1};
    vector<int>::iterator vec_iter;
    
    vec_iter = max_element(vec_contour_area.begin(), vec_contour_area.end());
    max_area_val[0] = *vec_iter;
    max_area_idx[0] = distance(vec_contour_area.begin(), vec_iter);
    
    vec_contour_area.erase(vec_iter);
    vec_iter = max_element(vec_contour_area.begin(), vec_contour_area.end());
    max_area_val[1] = *vec_iter;
    max_area_idx[1] = distance(vec_contour_area.begin(), vec_iter);
    if (max_area_idx[1] >= max_area_idx[0])
    {
      ++max_area_idx[1];
    }
    
    Mat img_maxarea = Mat::zeros(img_original.size(), CV_8UC3);
    Scalar color = Scalar(255,255,255);
    if (max_area_idx[0] > -1)
    {
      drawContours(img_maxarea, contours, max_area_idx[0], color, -1, 4);
    }
    if (max_area_idx[1] > -1)
    {
      drawContours(img_maxarea, contours, max_area_idx[1], color, -1, 4);
    }
    
    //RotatedRect rrect_area;
    Rect rect_area_0, rect_area_1;
    Rect rect_crop;
    
    //rrect_area = minAreaRect(contours[max_area_idx[0]]);
    //rect_area_0 = rrect_area.boundingRect();
    //rrect_area = minAreaRect(contours[max_area_idx[1]]);
    //rect_area_1 = rrect_area.boundingRect();
    
    rect_area_0 = boundingRect(contours[max_area_idx[0]]);
    rect_area_1 = boundingRect(contours[max_area_idx[1]]);
    
    int height = img_original.rows;
    int width  = img_original.cols;
    vector<Rect> vec_rect;
    vec_rect.push_back(rect_area_0);
    vec_rect.push_back(rect_area_1);
    rect_crop = ContainAll(vec_rect, width, height);
    */
    
    Mat img_crop_ori = img_original(rect_crop);
    Mat img_crop_ann = img_annotated(rect_crop);
    
    string file_path_save = PathJoin(dir_crop_ori, file_name+".jpg");
    imwrite(file_path_save, img_crop_ori);
    file_path_save = PathJoin(dir_crop_ann, file_name+".jpg");
    imwrite(file_path_save, img_crop_ann);
  }
}

Rect ContainAll(vector<Rect> vec_rect, int width, int height)
{
  /*
  // solution #1_1
  vector<int> vec_x, vec_y;
  
  vector<Rect>::iterator iter = vec_rect.begin();
  for ( ; iter != vec_rect.end(); ++iter)
  {
    //vec_ul_x.push_back(vec_rect.x);
    //vec_ul_y.push_back(vec_rect.y);
    //vec_lr_x.push_back(vec_rect.x + vec_rect.width);
    //vec_lr_y.push_back(vec_rect.y + vec_rect.height);
    vec_x.push_back(iter->x);
    vec_y.push_back(iter->y);
    vec_x.push_back(iter->x + iter->width);
    vec_y.push_back(iter->y + iter->height);
  }
  
  int min_x = *(min_element(vec_x.begin(), vec_x.end()));
  int min_y = *(min_element(vec_y.begin(), vec_y.end()));
  int max_x = *(max_element(vec_x.begin(), vec_x.end()));
  int max_y = *(max_element(vec_y.begin(), vec_y.end()));
  
  Rect rect_ret;
  rect_ret.x      = max(0, min_x);
  rect_ret.y      = max(0, min_y);
  rect_ret.width  = min(width  - rect_ret.x, max_x - min_x);
  rect_ret.height = min(height - rect_ret.y, max_y - min_y);
  
  cout << rect_ret.x << ",";
  cout << rect_ret.y << ",";
  cout << rect_ret.width << ",";
  cout << rect_ret.height << endl;
  */
  
  // solution #1_2
  vector<Point> vec_points;
  vector<Rect>::iterator iter = vec_rect.begin();
  for ( ; iter != vec_rect.end(); ++iter)
  {
    vec_points.push_back(Point(iter->x, iter->y));
    vec_points.push_back(Point(iter->x + iter->width, iter->y + iter->height));
  }
  
  Rect rect_ret = boundingRect(vec_points);
  
  return rect_ret;
}
