#include <gecode/int.hh>
#include <gecode/search.hh>
#include <gecode/minimodel.hh>
#include <iostream>

using namespace Gecode;

class SendMoreMoney : public Space {

protected:
    IntVarArray sol;
public:
    SendMoreMoney(void) : sol(*this, 8, 0, 9){
        // Referencias para melhor legibilidade
        IntVar 
            s(sol[0]), e(sol[1]), n(sol[2]), d(sol[3]),
            m(sol[4]), o(sol[5]), r(sol[6]), y(sol[7]);

        // Números nao podem comecar com 0
        rel(*this, s != 0);
        rel(*this, m != 0);

        // Todas as variaveis devem ter valores distintos
        distinct(*this, sol);

        // Vetor de inteiros
        IntArgs c(4+4+5);
        // Vector de variaveis inteiras
        IntVarArgs x(4+4+5);

        // SEND
        c[0]=1000; c[1]=100; c[2]=10; c[3]=1;
        x[0]=s; x[1]=e; x[2]=n; x[3]=d;
        // MORE
        c[4]=1000; c[5]=100; c[6]=10; c[7]=1;
        x[4]=m; x[5]=o; x[6]=r; x[7]=e;
        // MONEY
        c[8]=-10000; c[9]=-1000; c[10]=-100; c[11]=-10; c[12]=-1;
        x[8]=m; x[9]=o; x[10]=n; x[11]=e; x[12]=y;

        linear(*this, c, x, IRT_EQ, 0);

        branch(*this, sol, INT_VAR_SIZE_MIN, INT_VAL_MIN);
    }
  
    SendMoreMoney(bool share, SendMoreMoney &s) : Space(share, s){
        sol.update(*this, share, s.sol);
    }
    virtual Space* copy(bool share){
        return new SendMoreMoney(share, *this);
    }
    void print(void) const {
        std::cout << sol << std::endl;
    }
};

int main (){

    SendMoreMoney* m = new SendMoreMoney();
    DFS<SendMoreMoney> e(m);
    delete m;

    // busca e imprime todas as solucoes
    while(SendMoreMoney* s = e.next()){
        s->print();
        delete s;
    }
    
    return 0;
}
