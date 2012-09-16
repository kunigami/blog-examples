#ifndef PLI_SOLVER_HPP
#define PLI_SOLVER_HPP

#include "CbcModel.hpp"
#include "OsiClpSolverInterface.hpp"

#include <vector>
using namespace std;

/* Solves a PLI reading from a .lp file */
struct PLISolver {
    
    vector<double> solution;

    OsiClpSolverInterface solver;

    int maxSeconds;
 
    // Load the model from filename
    PLISolver(const char *filename);   

    // Time limit for solving
    void setMaxSeconds(int);

    // Solve the model. Returns true if the solution is optimal
    bool solve();
};

#endif
