#include "gradient_method.hpp"

#include <iostream>
#include <limits>
#include <numeric>

#include <cstdio>
#include <cmath>

using namespace std;

GradientMethod::GradientMethod(LagrangeanModel *model){
    GradientMethod::model = model;

    if(model->isMinimization()){
        dualBound = numeric_limits<double>::min();
        primalBound = numeric_limits<double>::max();
    }
    else {
        dualBound = numeric_limits<double>::max();
        primalBound = numeric_limits<double>::min();
    }
}

void GradientMethod::solve(double pi, double tPi, int maxNStuck, const vector<double> &u0){
    
    int nr = model->getNRelaxedConstraints();
    // Número de iterações sem melhoria do dual
    int nStuck = 0;
    vector<double> u = u0;
    // Solução lagrangeana
    vector<double> lagSol;
    // Solução primal
    vector<double> primalSol;

    while(1){

        // Obtém o ótimo da relaxação lagrangeana
        model->solveLagrangeanDual(u, lagSol);
        double lagCost = model->getLagrangeanCost(u, lagSol);
    
        if(betterDual(lagCost, dualBound)){
            dualBound = lagCost;
            nStuck = 0;
        }
        else nStuck++;
        
        // Obtém uma soluçõo primal
        model->buildFeasibleSolution(lagSol, primalSol);
        // Atualiza melhor primal conhecido
        double primalCost = model->getPrimalCost(primalSol);
        if(betterPrimal(primalCost, primalBound)){
            primalBound = primalCost;
            bestPrimal = primalSol;
        }
        // Encontrada solução ótima
        if(fabs(primalBound - dualBound) < 1e-5)
            break;
        // Atingido número máximo de iterações sem melhora
        if(nStuck == maxNStuck){
            nStuck = 0;
            pi /= 2.0;
            if(pi < tPi) break;
        }
        updateLagrangeanMultipliers(pi, lagSol, u);
    }



}


bool GradientMethod::betterPrimal(double a, double b){
    return model->isMinimization() ? a < b : a > b;
}
bool GradientMethod::betterDual(double a, double b){
    return model->isMinimization() ? a > b : a < b;
}
double GradientMethod::upperBound(){
    return model->isMinimization() ? primalBound : dualBound;
}
double GradientMethod::lowerBound(){
    return model->isMinimization() ? dualBound : primalBound;
}

void GradientMethod::updateLagrangeanMultipliers(double pi, const vector<double> &lagSol, vector<double> &u){

    vector<double> grad;
    model->getMultipliersWeight(lagSol, grad);
    
    double gradLength = 0;
    for(size_t i = 0; i < grad.size(); i++)
        gradLength += grad[i]*grad[i];

    double gap = 1.05 * upperBound() - lowerBound();
    double t = pi*gap/gradLength;
    
    for(size_t i = 0; i < u.size(); i++){
        u[i] = max(0.0, u[i] + t*grad[i]);
    }
}

double GradientMethod::getPrimalBound(){
    return primalBound;
}
double GradientMethod::getDualBound(){
    return dualBound;
}
