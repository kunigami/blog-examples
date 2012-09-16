#ifndef FLOOD_ILP_HPP
#define FLOOD_ILP_HPP

#include "board.hpp"
#include "cbc/lp_generator.hpp"

class FloodPLIGenerator : public LPGenerator {
    
    Board &_b;
    // Maximum number of movements
    int maxT;
    // Maximum number of colors
    int maxC;
    // Maximum number of components
    int maxL;
    // Size of x variables
    int xSize;

    int ySize;

public:

    FloodPLIGenerator(Board &b, int k = -1);
    
    int x(int c, int t);
    int y(int i, int t);

    virtual int getNumVars();
    virtual void buildObjFunc();
    virtual void buildConstraints();

    virtual void setVarTypes();

    virtual void setBounds();

    // Returns the list of colors used
    vector<int> extractMovements(vector<double> lpSolution);
};

#endif
