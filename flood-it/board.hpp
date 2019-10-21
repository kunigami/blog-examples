#ifndef BOARD_HPP
#define BOARD_HPP

#include <iostream>
#include <vector>
using namespace std;

struct Board {

    vector< vector<int> > &_m;
    int h, w;
    int ncolors;

    int nlabels;
    vector< vector<int> > labels;
    vector<int> labelColors;

    vector< vector<bool> > visited;

    vector< vector<int> > adjList;

    static int ndir;
    static int dy[ ];
    static int dx[ ];

    int countColors();
    void labelCellsAux(int y, int x, int color, int label);
    void labelCells();

    bool valid(int y, int x);

    void buildLabelGraph();

    Board(vector< vector<int> > &mat);

    void floodIt(vector<int> &colors);
    
    void floodItAux(int color, int y, int x);

    void print();

    void info();

};

#endif
