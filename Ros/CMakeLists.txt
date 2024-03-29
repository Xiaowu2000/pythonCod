cmake_minimum_required(VERSION 2.8.3)
project(mrga)

add_compile_options(-std=c++11)

## Find catkin macros and libraries
find_package(catkin REQUIRED COMPONENTS
  roscpp
  rospy
  std_msgs
  nav_msgs
  geometry_msgs
  diagnostic_msgs
  sensor_msgs
  tf
  mrga_msgs
)

find_package(Boost REQUIRED COMPONENTS
  filesystem
)
add_definitions(-Wno-deprecated-declarations) # Disable deprecated declarations warning (about std::auto_ptr)

###################################
## catkin specific configuration ##
###################################

## Declare things to be passed to dependent projects
catkin_package(
  LIBRARIES ${PROJECT_NAME}
  CATKIN_DEPENDS roscpp rospy std_msgs nav_msgs geometry_msgs diagnostic_msgs tf sensor_msgs
  DEPENDS
)
###########
## Build ##
###########

## include_directories(include)
include_directories(
  ${catkin_INCLUDE_DIRS}
  include
)

## goal allocation sources
set(RPDYNAMIC_SOURCES
	src/MRGAStrategy.cpp)


## Declare cpp executables
add_executable(MRGAAlgorithm ${RPDYNAMIC_SOURCES})
add_dependencies(MRGAAlgorithm ${catkin_EXPORTED_TARGETS})

## Specify libraries against which to link a library or executable target
target_link_libraries(MRGAAlgorithm ${catkin_LIBRARIES} ${Boost_LIBRARIES})

##########
## Test ##
##########

# please do not use add_rosttest_gtest (seems to be interfering with qtcreator and cmake)

#############
## Install ##
#############

install(TARGETS MRGAAlgorithm
  ARCHIVE DESTINATION ${CATKIN_PACKAGE_LIB_DESTINATION}
  LIBRARY DESTINATION ${CATKIN_PACKAGE_LIB_DESTINATION}
  RUNTIME DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)
