#include "ilp_solver.hpp"
#include <iostream>

ILPSolver::ILPSolver(const char *filename){
    
    int errors = solver.readLp(filename);      
    assert(errors == 0);    

    maxSeconds = -1;
} 

void ILPSolver::setMaxSeconds(int seconds){
    maxSeconds = seconds;
}

bool ILPSolver::solve(){
    
    // Pass data and solver to CbcModel 
    CbcModel model(solver);

    // Reduced printout
    model.setLogLevel(0);

    if(maxSeconds != -1)
        model.setMaximumSeconds(maxSeconds);

    // Do complete search
    model.solver()->branchAndBound();
    
    // Get the best solution
    int numberColumns = model.solver()->getNumCols();   
    const double *solPtr = model.solver()->getColSolution();

    solution.resize(numberColumns);
    for(int i = 0; i < numberColumns; i++){
        string name = model.solver()->getColName(i);
        int j = atoi(name.substr(1, name.length()-1).c_str());        
        solution[j] = solPtr[i];
        if(solPtr[i] > 0)
            cout << name << " " << solPtr[i] << endl;
    }
    return model.solver()->isProvenOptimal();
}
