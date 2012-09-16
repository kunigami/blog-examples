#ifndef ILP_SOLVER_HPP
#define ILP_SOLVER_HPP

#include "CbcModel.hpp"
#include "OsiClpSolverInterface.hpp"

#include <vector>
using namespace std;

/* Solves a ILP reading from a .lp file */
struct ILPSolver {
    
    vector<double> solution;

    OsiClpSolverInterface solver;

    int maxSeconds;
 
    // Load the model from filename
    ILPSolver(const char *filename);   

    // Time limit for solving
    void setMaxSeconds(int);

    // Solve the model. Returns true if the solution is optimal
    bool solve();
};

#endif
