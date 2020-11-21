cmake_minimum_required(VERSION 3.13.4)
project(Cistern)
 
#Bring the headers, such as Student.h into the project
#include_directories(include)
 
include_directories(
	libraries/wiringpi/wiringPi/
	src/
)


#Can manually add the sources using the set command as follows:
#set(SOURCES src/mainapp.cpp src/Student.cpp)
 
#However, the file(GLOB...) allows for wildcard additions:
file(GLOB_RECURSE SOURCES "src/*.cpp")
file(GLOB_RECURSE WIRINGPI_SRC "libraries/wiringpi/wiringPi/*.c") 

find_package(Threads)
#add_definitions(-lwiringPi)
 
add_executable(collection ${SOURCES} )

add_library(WIRINGPI STATIC ${WIRINGPI_SRC})

#find_library(WIRINGPI_LIBS NAMES wiringPi)
target_link_libraries(collection WIRINGPI)

add_dependencies(collection WIRINGPI)

target_link_libraries(collection ${CMAKE_THREAD_LIBS_INIT})
