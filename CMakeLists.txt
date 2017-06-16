cmake_minimum_required(VERSION 2.8)

project(proc_histopathology_image)

include_directories(
  /usr/local/include
  /root/proc_histopathology_image/3rdparty/boost_1_63_0
  /root/proc_histopathology_image/include
)

link_directories(
  /usr/local/lib
)

set(src_files
  src/boost_app_fs.cpp
  src/create_file_list.cpp
  src/crop_valid_area.cpp
  src/create_nidus_mask.cpp
  src/select_train_sample.cpp
  src/main.cpp
)

add_executable(proc_histopathology_image ${src_files})

target_link_libraries(proc_histopathology_image
  libopencv_core.so
  libopencv_highgui.so
  libopencv_imgproc.so
)
