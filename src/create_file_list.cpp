/*
 * Create file list
 */

#include <algorithm>
#include <fstream>
#include <iostream>
#include <string>
#include <vector>

#include "boost_app_fs.h"
#include "create_file_list.h"

using namespace std;


void CreateFileList(string dir_src)
{
  string file_path_info = PathJoin(dir_src, "files.txt");
  ofstream ofs_info(file_path_info.c_str(), ios::out);
  
  vector<string> vec_file_path, vec_file_name;
  TraverseDir(dir_src, vec_file_path, vec_file_name);
  sort(vec_file_name.begin(), vec_file_name.end());
  
  vector<string>::iterator iter = vec_file_name.begin();
  for (; iter != vec_file_name.end(); ++iter)
  {
    ofs_info << *iter << endl;
  }
  
  ofs_info.close();
}
