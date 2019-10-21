# If you have installed Gecode in a non-stardard location,
# make sure to set 
# CMAKE_INCLUDE_PATH and CMAKE_LIBRARY_PATH environment vars.

PROJECT(GEOCODE_EXAMPLES)

CMAKE_MINIMUM_REQUIRED(VERSION 2.8)

# Search for Gecode headers directory
FIND_PATH(gecode_include NAMES gecode/int.hh)
INCLUDE_DIRECTORIES(${gecode_include})

# Search for all Gecode libraries
FIND_LIBRARY(gecodedriver NAMES gecodedriver)
FIND_LIBRARY(gecodeminimodel NAMES gecodeminimodel)
FIND_LIBRARY(gecodeint NAMES gecodeint)
FIND_LIBRARY(gecodekernel NAMES gecodekernel)
FIND_LIBRARY(gecodesupport NAMES gecodesupport)
FIND_LIBRARY(gecodesearch NAMES gecodesearch)

SET(gecodelib ${gecodedriver} ${gecodeint} ${gecodekernel}
${gecodesupport} ${gecodesearch} ${gecodeminimodel})

# Build executables from our sample codes
ADD_EXECUTABLE(money money.cpp)
ADD_EXECUTABLE(nqueen nqueen.cpp)
ADD_EXECUTABLE(nonogram nonogram.cpp)
ADD_EXECUTABLE(sudoku sudoku.cpp)

# Link to Gecode libraries
TARGET_LINK_LIBRARIES(nqueen ${gecodelib})
TARGET_LINK_LIBRARIES(money ${gecodelib})
TARGET_LINK_LIBRARIES(nonogram ${gecodelib})
TARGET_LINK_LIBRARIES(sudoku ${gecodelib})



