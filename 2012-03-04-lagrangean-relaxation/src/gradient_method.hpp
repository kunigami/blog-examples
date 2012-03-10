#ifndef GRADIENT_METHOD
#define GRADIENT_METHOD

#include "lagrangean_model.hpp"

class GradientMethod {

private:

    // Modelo representando o problema a ser resolvido
    LagrangeanModel *model;
    // Melhor limitante dual
    double dualBound;
    // Melhor limitante primal
    double primalBound;
    // Melhor solução primal
    vector<double> bestPrimal;

    // Decide se a é um melhor valor dual do que b. Ou seja, se o
    // problema for de minimização, se a > b, se for de maximização, a
    // < b
    bool betterDual(double a, double b);

    // Decide se a é um melhor valor dual do que b. Ou seja, se o
    // problema for de minimização, se a < b, se for de maximização, a
    // > b
    bool betterPrimal(double a, double b);

    // Atualiza os multiplicadores lagrangeanos
    void updateLagrangeanMultipliers(double pi, const vector<double> &lagSol, vector<double> &u);

    // Limitante superior
    double upperBound();
    
    // Limitante inferior
    double lowerBound();

public:

    GradientMethod(LagrangeanModel *model);

    void solve(double pi, double tPi, int maxNStuck, const vector<double> &u0);

    // Retorna o valor do melhor limitante primal
    double getPrimalBound();
    // Retorna o valor do melhor limitante dual
    double getDualBound();

};

#endif
