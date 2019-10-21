#include <iostream>

#include <stdlib.h>

using namespace std;

#include "board.hpp"
#include "flood_ilp.hpp"
#include "cbc/ilp_solver.hpp"

vector< vector< int > > mat;

void readInput(){

    int h, w;
    cin >> h >> w;
    mat.resize(h);

    for(size_t i = 0; i < h; i++){
        mat[i].resize(w);
        for(size_t j = 0; j < w; j++){
            cin >> mat[i][j];
        }
    }
}

int main(int argc, char **argv){

    readInput();
    Board board(mat);

    board.info();

    for(int k = board.ncolors; k < board.nlabels; k++){
        FloodILPGenerator pliGen(board, k);
        pliGen.generate("tmp.lp");

        ILPSolver solver("tmp.lp");
        bool opt = solver.solve();

        if(opt){
            vector<double> solution = solver.solution;
        
            vector<int> colorOrder = pliGen.extractMovements(solution);
        
            cout << "Optimal movements:\n";
            for(size_t i = 0; i < colorOrder.size(); i++){
                cout << colorOrder[i] << " ";
            }
            cout << endl;

            board.print();
            board.floodIt(colorOrder);
            board.print();
            
            break;
        }
    }

    return 0;
}
