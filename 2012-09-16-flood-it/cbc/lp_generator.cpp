#include "lp_generator.hpp"

#include <fstream>
#include <iostream>

// funcao para imprimir uma equacao
inline ostream& operator<< (ostream &o, vector<Variable> &eq){
    for(size_t i = 0; i < eq.size(); i++)
        o << (i ? (eq[i].isNeg() ? " - " : " + " ) : "   ") << eq[i];
    return o;
}


Constraint::Constraint(){
    eq.clear();
    eqType = LE;
    rhs = 0;
}

inline ostream& operator<< (ostream &o, Constraint constraint){
    string op;
    switch(constraint.eqType){
    case Constraint::LE:
        op = " <= ";
        break;
    case Constraint::EQ:
        op = " = ";
        break;
    case Constraint::GE:
        op = " >= ";
    }
    return o << constraint.eq << op << constraint.rhs;
}

Bound::Bound(int _varId, double eq){
    varId = _varId;
    ub = lb = eq;
}
inline ostream& operator<< (ostream &o, Bound &b){
    if(b.ub - b.lb < 1e-3){
        o << "x" << b.varId << " = " << b.ub;
    }
    else {
        o << b.lb << " <= x" << b.varId << " <= " << b.ub;
    }
    return o;
}

void LPGenerator::builder(){

    setProblemType();
    numVars = getNumVars();
    buildObjFunc();
    buildConstraints();
    setVarTypes();
    setBounds();
}

void LPGenerator::generate(const char *filename){

    builder();

    ofstream fout(filename);

    // imprime trecho da funcao objetivo
    fout << (problemType == MIN ? "Minimize" : "Maximize") << "\n";    
    fout << objFunc << "\n";  
   
    // imprime trecho das restricoes
    fout << "Subject To\n";
    for(size_t i = 0; i < constraints.size(); i++){
        fout << constraints[i] << "\n";
    }

    // TODO: implementar o trecho bounds
    fout << "Bounds\n";
    for(size_t i = 0; i < bounds.size(); i++){
        fout << bounds[i] << "\n";
    }

    // imprime trecho do tipo das variaveis
    int binCount = 0, intCount = 0;
    for(size_t i = 0; i < varTypes.size(); i++){
        switch(varTypes[i]){
        case Variable::INTEGER:
            intCount++; 
            break;
        case Variable::BINARY:
            binCount++;
            break;
        }
    }
    if(intCount > 0){
        fout << "General\n   ";
        bool first = true;
        for(size_t i = 0; i < numVars; i++)
            if(varTypes[i] == Variable::INTEGER){
                if (first) first = false;
                else fout << " ";
                fout << "x" << i; 
            }

        fout << "\n";
    }
    if(binCount > 0){
        fout << "Binary\n   ";
        bool first = true;
        for(size_t i = 0; i < numVars; i++)
            if(varTypes[i] == Variable::BINARY){
                if(first) first = false;
                else fout << " ";
                fout << "x" << i; 
            }
        fout << "\n";
    }
    fout << "End\n";
    fout.close();
}
void LPGenerator::setProblemType(){
    problemType = MIN;
}

void LPGenerator::setVarTypes(){    
    varTypes.assign(numVars, Variable::REAL);
}

void LPGenerator::setBounds(){
}

