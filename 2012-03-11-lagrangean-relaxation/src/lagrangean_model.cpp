#include "lagrangean_model.hpp"

LagrangeanModel::LagrangeanModel(bool minimization){
    LagrangeanModel::minimization = minimization;
}

bool LagrangeanModel::isMinimization(){
    return minimization;
}
