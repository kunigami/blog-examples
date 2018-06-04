const GUESS = 0;
const SUBTREE = 1;

class BullsAndCows extends React.Component {
  constructor(props) {
    super(props)
    this.state = {
    	items: [],
      node: props.decisionTree,
    }
  }

  render() {

  	const itemsReact = this.state.items.map((item, index) => {
    	return(
      	<Item key={index}>
          Guessed: {this.renderGuess(item.guess)}, result: {item.result}
        </Item>
      );
    });


    let solvedMessage;
    if (!this.isSolved()) {
      itemsReact.push(
        <Item key={'current'}>
          Guess: {this.renderGuess(this.state.node[GUESS])}
        </Item>
      );
    } else {
      solvedMessage = (
        <Message>
          Solved! The secret is: {this.renderGuess(this.state.node[GUESS])}
        </Message>
      );

    }

    return (
      <div style={{display: 'flex', justifyContent: 'center'}}>
        <div style={{width: 800}}>
          <Title>Bulls and Cows Solver</Title>
          <Description>
            Think of a 4-digit number with no repeated digits. Then choose the
            outcome (x, y), where x is the number of digits
            the solver got right AND in the right position, and y be the number
            of digits it got right but in the wrong position.
          </Description>
          <ol>
          {itemsReact}
          </ol>
          {solvedMessage}
          {this.renderOptions()}
        </div>
      </div>
    )
  }

  handleChange = (event) => {
	  const selection = event.target.value;
    if (selection === 'none') {
	    return;
    }
    this.setState(() => {
	    const currentGuess = this.state.node[GUESS];
	    const items = this.state.items;
      items.push({guess: currentGuess, result: selection});
      const nextNode = this.state.node[SUBTREE][selection];
      return {items, node: nextNode};
    })

  }

  renderGuess(guess) {
  	return JSON.stringify(guess);
  }

  isSolved() {
	  return (
      !this.state.node[SUBTREE] ||
      Object.keys(this.state.node[SUBTREE]).length == 0
    );
  }

  renderOptions() {
  	const subtree = this.state.node[SUBTREE];
    // Leaf node, meaning we found the solution
    if (!subtree) {
    	return null;
    }

    const options = [<option value={'none'}>Select outcome</option>]
    	.concat(Object.keys(subtree).map(value =>
    		<option value={value}>{value}</option>
    	));
    return (
    	<select
        style={{marginTop: 20}}
        value={'none'}
        onChange={this.handleChange}>
        {options}
      </select>
    );
  }
}

function Title({children}) {
  const style = {
    color: '#aaaaaa',
    fontFamily: "Verdana, Geneva, sans-serif",
  };
  return <h2 style={style}>{children}</h2>;
}

function Item({children}) {
  const style = {
    fontFamily: 'Inconsolata',
  };
  return <li style={style}>{children}</li>;
}

function Description({children}) {
  const style = {
    color: '#777777',
    fontSize: 12,
    fontFamily: 'Verdana, Geneva, sans-serif',
    width: 500,
  };
  return <div style={style}>{children}</div>;
}

function Message({children}) {
  const style = {
    fontFamily: 'Inconsolata',
  };
  return <div style={style}>{children}</div>;
}

ReactDOM.render(
  <BullsAndCows decisionTree={decisionTree} />,
  document.querySelector("#app"),
);
