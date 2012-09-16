#include "board.hpp"
#include <set>
using namespace std;

int Board::ndir = 4;
int Board::dy[ ] = {-1, 0, 1, 0};
int Board::dx[ ] = {0, 1, 0, -1};

Board::Board(vector< vector<int> > &m) : _m(m) {

    h = m.size();
    w = m[0].size();
    ncolors = countColors();

    labelCells();
    buildLabelGraph();
}

int Board::countColors(){
    set<int> colorSet;
    for(int y = 0; y < h; y++){
        for(int x = 0; x < w; x++){
            colorSet.insert(_m[y][x]);
        }
    }
    return colorSet.size();
}

void Board::labelCells(){

    // Initialize labels
    labels.resize(h);
    for(int i = 0; i < h; i++){
        labels[i] = vector<int>(w, -1);
    }
    nlabels = 0;
    
    // Start labeling
    labelColors.clear();
    for(int y = 0; y < h; y++){
        for(int x = 0; x < w; x++){
            if(labels[y][x] == -1){
                labelColors.push_back(_m[y][x]);
                labelCellsAux(y, x, _m[y][x], nlabels++);
            }
        }
    }
}

void Board::labelCellsAux(int y, int x, int color, int label){

    if(!valid(y, x) || labels[y][x] != -1 || _m[y][x] != color) return;
    labels[y][x] = label;

    for(int i = 0; i < ndir; i++){
        labelCellsAux(y + dy[i], x + dx[i], color, label);
    }
}

void Board::buildLabelGraph(){

    vector< set<int> > adjSet(nlabels);
    
    for(int y = 0; y < h; y++){
        for(int x = 0; x < w; x++){
            int l1 = labels[y][x];
            for(int i = 0; i < ndir; i++){
                if(valid(y + dy[i], x + dx[i])){
                    int l = labels[y + dy[i]][x + dx[i]];
                    if(l != l1) adjSet[l1].insert(l);
                }
            }
        }
    }
    // Convert adj set to adj list
    adjList.resize(nlabels);
    for(int i = 0; i < nlabels; i++){
        adjList[i].clear();
        copy(adjSet[i].begin(), adjSet[i].end(), back_inserter(adjList[i]));
    }
}

bool Board::valid(int y, int x){
    return y >= 0 && y < h && x >= 0 && x < w;
}

void Board::floodIt(vector<int> &colors){

    visited.resize(h);
    for(size_t y = 0; y < h; y++)
        visited[y].resize(w);

    for(size_t i = 0; i < colors.size(); i++){

        for(size_t y = 0; y < h; y++)
            for(size_t x = 0; x < w; x++)
                visited[y][x] = false;

        floodItAux(colors[i], 0, 0);

        print();
    }
}

void Board::floodItAux(int color, int y, int x){

    if(!valid(y, x) || _m[y][x] != _m[0][0] || visited[y][x]) return;

    visited[y][x] = true;

    for(int i = 0; i < ndir; i++)
        floodItAux(color, y + dy[i], x + dx[i]);

    _m[y][x] = color;
}

void Board::print(){
    for(int i = 0; i < h; i++){
        for(int j = 0; j < w; j++)
            cout << " " << _m[i][j];
        cout << endl;
    }
    cout << endl;
}

void Board::info(){
    cout << "Height:               " << h << endl;
    cout << "Width:                " << w << endl;
    cout << "Number of colors:     " << ncolors << endl;
    cout << "Number of components: " << nlabels << endl;
}
