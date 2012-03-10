#include "facility_location.hpp"

#include <iostream>
#include <fstream>
#include <boost/algorithm/string.hpp>
#include <boost/bind.hpp>

using namespace std;
using namespace boost;

FacilityLocation* FacilityLocation::instance = NULL;

// Este é um modelo lagrangeano de minimização
FacilityLocation::FacilityLocation() : LagrangeanModel(true) {    
}

FacilityLocation* FacilityLocation::getInstance(){
    if(instance == NULL)
        instance = new FacilityLocation();
    return instance;
}

int FacilityLocation::x(int i, int j){
    return m + i*m + j; // variaveis x são indexadas após y
}

int FacilityLocation::y(int j){
    return j;
}

void FacilityLocation::readInput(const char *filename){
    
    string trash;
    ifstream fin(filename);
    
    // Leitura dos dados
    fin >> m >> n;

    fixed_cost.resize(m);

    string line;
    // Descarta linha em branco

    getline(fin, line);
    for(int j = 0; j < m; j++){
        // Faz uma leitura robusta para contemplar os diferentes tipos
        // de formatos        
        getline(fin, line);

        vector<string> data;
        split(data, line, is_any_of(" "));
        
        // Remove tokens vazios
        data.erase(remove_if(data.begin(), data.end(), bind(&string::empty, _1)), data.end());

        fixed_cost[j] = atof(data[1].c_str());
    }

    cost.resize(n);
    int demand; // Ignora demanda
    for(int i = 0; i < n; i++){
        fin >> demand;
        cost[i].resize(m);
        for(int j = 0; j < m; j++){
            fin >> cost[i][j];
        }
    }

}

int FacilityLocation::getNClients(){
    return n;
}

int FacilityLocation::getNFactories(){
    return m;
}

void FacilityLocation::solveLagrangeanDual(const vector<double> &u, vector<double> &sol){
    
    // Custos lagrangeanos
    vector< vector<double> > lcost(n);

    for(int i = 0; i < lcost.size(); i++){
        lcost[i] = vector<double>(m);
        for(int j = 0; j < lcost[i].size(); j++)
            lcost[i][j] = cost[i][j] - u[i];
    }

    // Resolve o problema por inspeção
    sol.assign(getNVars(), 0);
    for(int j = 0; j < m; j++){
        double open_cost = fixed_cost[j]; // Custo de abrir a fabrica e atender aos clientes
        for(int i = 0; i < n; i++)
            if(lcost[i][j] < 0) open_cost += lcost[i][j];

        if(open_cost < 0){
            sol[y(j)] = 1;
            for(int i = 0; i < n; i++)
                if(lcost[i][j] < 0) sol[x(i, j)] = 1;
        }
    }
}

void FacilityLocation::buildFeasibleSolution(const vector<double> &lsol, vector<double> &sol){
    sol.assign(getNVars(), 0);
    for(int j = 0; j < m; j++)
        sol[y(j)] = lsol[y(j)];

    // A solution can be expressed by the open facilities 
    for(int i = 0; i < n; i++){
        int bestJ = -1;
        double bestVal = 1e123;
        for(int j = 0; j < m; j++)
            if(sol[y(j)] > 0 && cost[i][j] < bestVal){
                bestVal = cost[i][j];
                bestJ = j;
            }
        sol[x(i, bestJ)] = 1;
    }
}

double FacilityLocation::getPrimalCost(const vector<double> &sol){
    double c = 0;
    for(int j = 0; j < m; j++){
        c += sol[y(j)] * fixed_cost[j];
        for(int i = 0; i < n; i++){
            c += sol[x(i, j)] * cost[i][j];
        }
    }
    return c;    
}

double FacilityLocation::getLagrangeanCost(const vector<double> &u, const vector<double> &sol){
    double c = 0;
    for(int j = 0; j < m; j++){
        c += sol[y(j)] * fixed_cost[j];
        for(int i = 0; i < n; i++){
            c += sol[x(i, j)] * (cost[i][j] - u[i]);
        }
    }
    for(size_t i = 0; i < u.size(); i++){
        c += u[i];
    }
    return c;
}

void FacilityLocation::getFixedCost(vector<double> &fixed_cost){
    fixed_cost = this->fixed_cost;
}

int FacilityLocation::getNVars(){
    return m + m*n;
}

int FacilityLocation::getNRelaxedConstraints(){
    return n;
}

void FacilityLocation::getMultipliersWeight(const vector<double> &sol, vector<double> &w){
    w.resize(n);
    for(size_t i = 0; i < n; i++){
        w[i] = 1;
        for(size_t j = 0; j < m; j++)
            w[i] -= sol[x(i,j)];
    }
}
