#include <iostream>
#include <string>
#include <vector>

#define BOOST_ALL_NO_LIB
#include "libs/system/src/error_code.cpp"               // system
#include "boost/filesystem.hpp"                         // filesystem
#include "libs/filesystem/src/codecvt_error_category.cpp"
#include "libs/filesystem/src/operations.cpp"
#include "libs/filesystem/src/path.cpp"
#include "libs/filesystem/src/path_traits.cpp"
#include "libs/filesystem/src/portability.cpp"
#include "libs/filesystem/src/unique_path.cpp"
#include "libs/filesystem/src/utf8_codecvt_facet.cpp"
#include "libs/filesystem/src/windows_file_codecvt.hpp"
#include "libs/filesystem/src/windows_file_codecvt.cpp"

#include "boost/optional.hpp"
#include "boost/algorithm/string.hpp"
#include "boost/assert.hpp"
#include "boost/lexical_cast.hpp"
#include "boost/math/special_functions/round.hpp"

#include "boost_app_fs.h"

using namespace std;

namespace bfs = boost::filesystem;
typedef bfs::recursive_directory_iterator rdir_iterator;


void CreateDir(string dir_new)
{
  bfs::path bpath_dir_new(dir_new);
  if (!bfs::exists(bpath_dir_new))
  {
    bfs::create_directories(bpath_dir_new);
  }
}

string GetCurrentDirPath()
{
  return bfs::initial_path<bfs::path>().string();
}

bool IsExists(string path)
{
  bfs::path bpath(path);
  
  return bfs::exists(bpath);
}

string PathJoin(string path_a, string path_b)
{
  bfs::path bpath_a(path_a);
  bfs::path bpath_b(path_b);
  
  bpath_a /= bpath_b;
  
  return bpath_a.string();
}

void TraverseDir(string dir_src, vector<string>& vec_file_path, vector<string>& vec_file_name)
{
  string image_type(".jpg.png.jpeg.JPG.PNG");
  
  vector<string> image_list;
  
  rdir_iterator end;
  for (rdir_iterator pos(dir_src); pos!=end; ++pos)
  {
    if (!bfs::is_directory(*pos))
    {
      string file_extension = pos->path().extension().string();
      if (boost::contains(image_type, file_extension))
      {
        vec_file_path.push_back(pos->path().string());
        vec_file_name.push_back(pos->path().stem().string());
      }
    }
  }
}
