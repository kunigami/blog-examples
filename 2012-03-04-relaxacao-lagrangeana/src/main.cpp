#include "facility_location.hpp"
#include "gradient_method.hpp"
#include "time_utils.hpp"

#include <iostream>
#include <fstream>
#include <cstdio>

using namespace std;

int main(int argc, char **argv){
    

    if(argc < 2){
        printf("Uso: %s <arquivo>\n", argv[0]); 
        return 1;
    }
    const char *filename = argv[1];

    FacilityLocation* prob = FacilityLocation::getInstance();
    
    prob->readInput(filename);

    GradientMethod gradient(prob);

    int nr = prob->getNRelaxedConstraints();
    vector<double> u(nr, 1.0/nr);

    // Começa a medir o tempo
    Time startTime = TimeUtils::getTime();

    gradient.solve(2.0, 0.2, 30, u);

    double elapsedSec = TimeUtils::elapsedSeconds(startTime);

    double primalBound = gradient.getPrimalBound();
    double dualBound = gradient.getDualBound();

    int nClients = prob->getNClients();
    int nFactories = prob->getNFactories();

    // Imprime algumas estatísticas
    printf("%d\n", nFactories);
    printf("%d\n", nClients);
    printf("%.2lf\n", primalBound);
    printf("%.2lf\n", dualBound);
    printf("%.2lf\n", elapsedSec);

    return 0;
}
