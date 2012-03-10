#ifndef FACILITY_LOCATION
#define FACILITY_LOCATION

#include "lagrangean_model.hpp"
#include <vector>

using namespace std;

class FacilityLocation : public LagrangeanModel {

 private:

    int m; // Numero de instalacoes
    int n; // Numero de clientes
    
    vector<double> fixed_cost;     // Custo fixo de abrir uma fabrica 
    vector< vector<double> > cost; // Custo de associar um cliente i a uma fabrica j

    // Singleton
    static FacilityLocation *instance;

    // Metodos auxiliares para indexar o vetor de solucoes
    int x(int i, int j);
    int y(int j);

    FacilityLocation();

 public:

    // Método factory
    static FacilityLocation *getInstance();

    // Lê a estrutura de um stream
    void readInput(const char *filename);

    //// Getters e setters

    // Retorna o número de clientes
    int getNClients();
    // Retorna o número de fábricas
    int getNFactories();


    void getFixedCost(vector<double> &fixed_cost);

    // Número de variáveis do problema
    int getNVars();

    //
    // Implementação dos métodos virtuais de LagrangeanModel. Ver lagrangean_model.hpp
    // para uma referencia
    //
    void solveLagrangeanDual(const vector<double> &u, vector<double> &sol);

    int getNRelaxedConstraints();

    double getLagrangeanCost(const vector<double> &u, const vector<double> &sol);
    
    void buildFeasibleSolution(const vector<double> &lsol, vector<double> &sol);

    double getPrimalCost(const vector<double> &sol);

    void getMultipliersWeight(const vector<double> &sol, vector<double> &w);
};

#endif
