#include <gecode/driver.hh>
#include <gecode/int.hh>
#include <gecode/minimodel.hh>
#include <gecode/search.hh>

#include <string>
#include <cmath>
#include <cctype>
#include <vector>

using namespace Gecode;

const int n = 3;
const int N = n*n;

class Sudoku : public Space {

protected:
  IntVarArray sol;
  
public:

  Sudoku(std::vector<std::string> &mat) : sol(*this, N*N, 1, N) {
    
    Matrix<IntVarArray> m(sol, N, N);

    // Linhas e colunas devem ter valores diferentes
    for (int i=0; i<N; i++) {
      distinct(*this, m.row(i));
      distinct(*this, m.col(i));
    }

    // Restricoes dos sub-quadrados
    for (int i=0; i<N; i+=n) {
      for (int j=0; j<N; j+=n) {
        distinct(*this, m.slice(i, i+n, j, j+n));
      }
    }

    // Celulas ja preenchidas
    for (int i=0; i<N; i++)
      for (int j=0; j<N; j++)
        if (mat[i][j] != '.')
          rel(*this, m(i,j), IRT_EQ, mat[i][j] - '0');
    
    branch(*this, sol, INT_VAR_SIZE_MIN, INT_VAL_SPLIT_MIN);
  }

  Sudoku(bool share, Sudoku& s) : Space(share, s) {
    sol.update(*this, share, s.sol);
  }

  virtual Space* copy(bool share) {
    return new Sudoku(share, *this);
  }

  void print() const {
    for (int i = 0; i<N*N; i++) {
      if (sol[i].assigned()) 
        std::cout << sol[i] << " ";
      else
        std::cout << ". ";
      
      if((i+1) % N == 0)
        std::cout << std::endl;
    }
    std::cout << std::endl;
  }
};

int main(int argc, char* argv[]) {

  std::vector<std::string> mat(N);
  for(int i = 0; i < N; i++)
    std::cin >> mat[i];

  Sudoku* m = new Sudoku(mat);
  DFS<Sudoku> e(m);

  while(Sudoku* s = e.next()){
        s->print();
        delete s;
  }

  return 0;
}
