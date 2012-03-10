#ifndef LAGRANGEAN_MODEL
#define LAGRANGEAN_MODEL

#include <vector>

using namespace std;

/*
 * Interface required by the gradient method
 * 
 */
class LagrangeanModel {

protected:

    bool minimization;

    // Obriga as classes bases a especificar se o problema é de minimização ou não
    LagrangeanModel(bool minimization);

public:

    // Resolve a relaxacao lagrangeana
    virtual void solveLagrangeanDual(const vector<double> &u, vector<double> &sol) = 0;

    // Numero de desigualdades relaxadas (tamanho de u)
    virtual int getNRelaxedConstraints() = 0;
    
    // Valor violado das desigualdades relaxadas para uma dada solução sol
    // Por exemplo, se a desigualdade relaxada era "ax < b_i", retorna para problemas 
    // de maximização b_i - ax ou ax - b_i
    virtual void getMultipliersWeight(const vector<double> &sol, vector<double> &w) = 0;

    // Retorna o custo lagrangeano de uma solucao
    virtual double getLagrangeanCost(const vector<double> &u, const vector<double> &sol) = 0;

    // Obtém uma solução primal viável a partir de uma solução lagrangeana
    virtual void buildFeasibleSolution(const vector<double> &lsol, vector<double> &sol) = 0;

    // Retorna o custo de uma solucao para o problema primal
    virtual double getPrimalCost(const vector<double> &sol) = 0;

    // Se a função objetivo é de minimização (true) ou de maximização (fals)
    virtual bool isMinimization();
    
};

#endif
