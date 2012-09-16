#include <gecode/driver.hh>
#include <gecode/int.hh>
#include <gecode/minimodel.hh>
#include <vector>

using namespace Gecode;

typedef std::vector< std::vector<int> > AdjMat;

class Nonogram : public Space {
protected:
 
  AdjMat &_rows;
  AdjMat &_cols;
  BoolVarArray sol;

  // Expressao regular a partir de uma linha
  DFA regexp(std::vector<int> &v) {
    REG r0(0), r1(1);
    REG border = *r0;
    REG between = +r0;
    REG r = border;
    for(size_t i = 0; i < v.size(); i++){
      if(i > 0) r += between;
      r += r1(v[i], v[i]);
    }
    return r + border;
  }

public:

  Nonogram(AdjMat &rows, AdjMat &cols)
    : _rows(rows), _cols(cols), sol(*this, rows.size()*cols.size(), 0, 1) {
    
    Matrix<BoolVarArray> m(sol, _cols.size(), _rows.size());
    
    // Restricoes das colunas
    for (size_t w=0; w < cols.size(); w++)
      extensional(*this, m.col(w), regexp(cols[w]));
    // Post constraints for rows
    for (size_t h=0; h < rows.size(); h++)
      extensional(*this, m.row(h), regexp(rows[h]));
    
    // Numero de dicas de colunas
    int ncols = 0;
    // Number de dicas de linhas
    int nrows = 0;
    
    for (int w = 0; w < cols.size(); w++)
      ncols += cols[w].size();
    for (int h = 0; h < rows.size(); h++)
      nrows += rows[h].size();
    
    for (int w = 0; w < cols.size(); w++)
      branch(*this, m.col(w), INT_VAR_NONE, INT_VAL_MIN);
  }

  Nonogram(bool share, Nonogram& s)
    : Space(share,s), _rows(s._rows), _cols(s._cols) {
    sol.update(*this, share, s.sol);
  }

  virtual Space* copy(bool share) {
    return new Nonogram(share, *this);
  }

  void print() const {
    Matrix<BoolVarArray> m(sol, _cols.size(), _rows.size());
    for (int h = 0; h < _rows.size(); ++h) {
      for (int w = 0; w < _cols.size(); ++w)
        std::cout << ((m(w,h).val() == 1) ? '#' : '.');
      std::cout << std::endl;
    }
    std::cout << std::endl;
  }
};

void readInput(AdjMat &hints){
  for(int i = 0; i < hints.size(); i++){
    int nhints;
    std::cin >> nhints;
    hints[i] = std::vector<int>(nhints);
    for(int j =0; j < nhints; j++){
      std::cin >> hints[i][j];
    }
  }
}

int main(int argc, char* argv[]) {

  int nrows, ncols;
  std::cin >> nrows >> ncols; 
  std::vector< std::vector<int> > rows(nrows), cols(ncols);
  readInput(rows);
  readInput(cols);
  
  Nonogram* m = new Nonogram(rows, cols);
  DFS<Nonogram> e(m);
  delete m;
  
  while(Nonogram* s = e.next()){
    s->print();
    delete s;
  }
  
  return 0;
}
