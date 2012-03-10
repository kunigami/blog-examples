PROJECT(FACILITY_LOCATION)

CMAKE_MINIMUM_REQUIRED(VERSION 2.4.5)

SET(CMAKE_BUILD_TYPE Debug)

INCLUDE(FindBOOST)

IF(Boost_FOUND)
  INCLUDE_DIRECTORIES(${Boost_INCLUDE_DIR}) 
  ADD_EXECUTABLE(facility_location main.cpp facility_location.cpp gradient_method.cpp lagrangean_model.cpp time_utils.cpp)
ELSE()
  MESSAGE("Esse programa usa a biblioteca BOOST")
ENDIF()

