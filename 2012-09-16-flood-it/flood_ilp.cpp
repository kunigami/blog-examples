#include "flood_pli.hpp"
#include "board.hpp"
#include <cmath>
#include <algorithm>

FloodPLIGenerator::FloodPLIGenerator(Board &b, int k) : _b(b) {

    // Theorem 5
    int n = max(b.h, b.w);

    maxT = (k == -1) ? n*(3 + sqrt(2*b.ncolors)) + b.ncolors : k;

    maxC = b.ncolors;
    maxL = b.nlabels;
    xSize = maxT*maxC;
    ySize = maxT*maxL;
}

int FloodPLIGenerator::getNumVars(){
    return xSize + ySize;
}

void FloodPLIGenerator::buildObjFunc(){

    LPGenerator::objFunc.clear();
    for(size_t c = 0; c < maxC; c++)
        for(size_t t = 0; t < maxT; t++)
            LPGenerator::objFunc.push_back(Variable(x(c, t)));

}
 
void FloodPLIGenerator::buildConstraints(){

    // Each component must be covered at maximum once
    LPGenerator::constraints.clear();
    for(size_t i = 0; i < _b.nlabels; i++){
        Constraint c;
        for(size_t t = 0; t < maxT; t++){
            c.addVar(Variable(y(i, t)));
        }
        c.eqType = Constraint::GE;
        c.rhs = 1;
        LPGenerator::constraints.push_back(c);
    }
    
    // At each iteration, at most one color may be chosen
    for(size_t t = 0; t < maxT; t++){
        Constraint con;
        for(int c = 0; c < maxC; c++){
            con.addVar(Variable(x(c, t)));
        }
        con.eqType = Constraint::LE;
        con.rhs = 1;
        LPGenerator::constraints.push_back(con);
    }

    // A component may only be colored if some of its adjacent was colored before
    for(size_t i = 0; i < _b.nlabels; i++){
        for(size_t t = 1; t < maxT; t++){

            Constraint con;
            con.addVar(Variable(y(i, t)));

            for(size_t j = 0; j < _b.adjList[i].size(); j++){

                int adj = _b.adjList[i][j];
                con.addVar(Variable(y(adj, t-1), -1.0));

            }
            con.eqType = Constraint::LE;
            con.rhs = 0;
            LPGenerator::constraints.push_back(con);
        }
    }

    for(size_t i = 0; i < _b.nlabels; i++){
        for(size_t t = 1; t < maxT; t++){
            Constraint con;
            int ci = _b.labelColors[i];
            con.addVar(Variable(y(i, t)));
            con.addVar(Variable(x(ci, t), -1.0));
            con.addVar(Variable(y(i, t-1), -1.0));
            con.eqType = Constraint::LE;
            con.rhs = 0;
            LPGenerator::constraints.push_back(con);
        }
    }

    // Additional constraints
    
    // Don't choose the same color in consecutive iterations
    for(size_t t = 1; t < maxT; t++){
        for(int c = 0; c < maxC; c++){
            Constraint con;
            con.addVar(Variable(x(c, t)));
            con.addVar(Variable(x(c, t-1)));
            con.eqType = Constraint::LE;
            con.rhs = 1;            
            LPGenerator::constraints.push_back(con);
        }
    }

}

int FloodPLIGenerator::x(int c, int t){
    return c*maxT + t;
}

int FloodPLIGenerator::y(int i, int t){
    return xSize + i*maxT + t;
}

void FloodPLIGenerator::setVarTypes(){    
    LPGenerator::varTypes.assign(getNumVars(), Variable::BINARY);
}

void FloodPLIGenerator::setBounds(){
    LPGenerator::bounds.clear();
    LPGenerator::bounds.push_back(Bound(y(0, 0), 1.0));
    for(int i = 1; i < maxL; i++){
        LPGenerator::bounds.push_back(Bound(y(i, 0), 0.0));
    }
}

vector<int> FloodPLIGenerator::extractMovements(vector<double> lpSolution){
    vector<int> movements;
    for(int t = 1; t < maxT; t++){
        int chosenColor = -1;
        for(int c = 0; c < maxC; c++){
            if(lpSolution[x(c, t)] > 0.0){
                chosenColor = c;
                break;
            }
        }
        if(chosenColor == -1)
            cerr << "Color not found for iteration " << t << endl;
        movements.push_back(chosenColor);
    }
    return movements;
}
