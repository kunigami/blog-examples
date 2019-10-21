#include <gecode/int.hh>
#include <gecode/search.hh>
#include <gecode/minimodel.hh>

#include <iostream>

using namespace Gecode;

class NQueens : public Space {

protected:
    IntVarArray sol;
    int _n;
public:
    NQueens(int n) : sol(*this, n, 1, n) {

        _n = n;
        for (int i = 0; i<n; i++)
            for (int j = i+1; j<n; j++) {
                rel(*this, sol[i] != sol[j]);
                rel(*this, sol[i]+i != sol[j]+j);
                rel(*this, sol[i]-i != sol[j]-j);
            } 
        
        branch(*this, sol, INT_VAR_SIZE_MIN, INT_VAL_MAX);      
    }
  
    NQueens(bool share, NQueens &s) : Space(share, s){
        _n = s._n;
        sol.update(*this, share, s.sol);
    }
    virtual Space* copy(bool share){
        return new NQueens(share, *this);
    }
    void print(void) const {
        std::cout << sol << std::endl;
    }
};

int main (){

    NQueens* m = new NQueens(6);
    DFS<NQueens> e(m);
    delete m;

    // busca e imprime todas as solucoes
    while(NQueens* s = e.next()){
        s->print();
        delete s;
    }

    return 0;
}
