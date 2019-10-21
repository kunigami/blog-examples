#ifndef LP_GENERATOR_HPP
#define LP_GENERATOR_HPP

#include <cmath>

#include <vector>
#include <iostream>
#include <string>

using namespace std;

struct Variable {
    
    int id;
    double coeficient;

    Variable(int id=0, double coeficient = 1.0) : id(id), coeficient(coeficient) {}

    enum Type {
        REAL, INTEGER, BINARY
    };

    friend ostream& operator<< (ostream &o, Variable v){
        return o << fabs(v.coeficient) << " x" << v.id;
    }
    bool isNeg(){
        return coeficient < 1e-5;
    }
};

typedef vector<Variable> Equation;

struct Constraint {

    Equation eq;
    int rhs;

    enum Type {
        LE, EQ, GE
    } eqType;

    Constraint();

    void addVar(Variable var) { eq.push_back(var); } 

    friend ostream& operator<< (ostream &o, Constraint constraint);

};

struct Bound {
    int varId;
    double lb;
    double ub;

    Bound(int _varId, double eq);
};

struct LPGenerator {

    // Number of variables
    int numVars;

    // Objective function
    Equation objFunc;
    // Maximization or minimization?
    enum ProblemType {
        MIN, MAX
    } problemType;

    // Set of Constraints
    vector< Constraint > constraints;

    // Variable types
    vector < Variable::Type > varTypes;

    // Variable bounds
    vector < Bound > bounds;

    // Generate the LP model and save to filename
    virtual void generate(const char *filename);

    virtual void builder();

    // Methods that should be implemented by deriving classes
    virtual int getNumVars() = 0;
    virtual void buildObjFunc() = 0;
    virtual void buildConstraints() = 0;

    // Optional: Defaults to minimization
    virtual void setProblemType();

    // Optional: Defaults to real variables
    virtual void setVarTypes(); 

    // Optional: Set bounds of variables
    virtual void setBounds();
};

#endif
