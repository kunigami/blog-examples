cmake_minimum_required(VERSION 2.6)

#set(CMAKE_BUILD_TYPE Debug)
set(CMAKE_BUILD_TYPE Release)

# Try finding CBC library
set(CBC_HOME $ENV{CBC_HOME})

message(${CBC_HOME}/lib)

find_library(CBC NAMES Cbc PATHS ${CBC_HOME}/lib)
find_library(CGL NAMES Cgl PATHS ${CBC_HOME}/lib)
find_library(CLP NAMES Clp PATHS ${CBC_HOME}/lib)
find_library(OSI NAMES Osi PATHS ${CBC_HOME}/lib)
find_library(COIN_UTILS NAMES CoinUtils PATHS ${CBC_HOME}/lib)
find_library(OSICLP NAMES OsiClp PATHS ${CBC_HOME}/lib) 

if(NOT CBC)
    message("Cbc library not found :(")
else()
   message("Cbc library found :)")
   # Turn cbc on
   set(CMAKE_CXX_FLAGS "-DENABLE_CBC")
   set(CBC_INCLUDES ${CBC_HOME}/include/coin)
   set(CBC_LIBRARIES ${CBC} ${CGL} ${CLP} ${OSI} ${COIN_UTILS} ${OSICLP})

   set(PLI_SRCS cbc/lp_generator.cpp cbc/pli_solver.cpp)
   include_directories(cbc)
   include_directories(${CBC_INCLUDES})

   add_executable(solver main.cpp flood_pli.cpp board.cpp cbc/lp_generator.cpp cbc/pli_solver.cpp)

   # link solver to COIN-OR
   target_link_libraries(solver ${CBC_LIBRARIES})

endif()
