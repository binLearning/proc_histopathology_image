#ifndef _BOOST_APP_FS_H_
#define _BOOST_APP_FS_H_

#include <string>
#include <vector>

using std::string;
using std::vector;

void   CreateDir(string dir_new);
string GetCurrentFolderPath();
bool   IsExists(string path);
string PathJoin(string path_a, string path_b);
void   TraverseDir(string dir_src,
                   vector<string>& vec_file_path,
                   vector<string>& vec_file_name);

#endif
