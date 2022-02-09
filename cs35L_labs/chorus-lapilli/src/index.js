import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';

function Square(props) {
  return (
    <button className="square" onClick={props.onClick}>
      {props.value}
    </button>
  );
}

class Board extends React.Component {
  renderSquare(i) {
    return (
      <Square
        value={this.props.squares[i]}
        onClick={() => this.props.onClick(i)}
      />
    );
  }

  render() {
    return (
      <div>
        <div className="board-row">
          {this.renderSquare(0)}
          {this.renderSquare(1)}
          {this.renderSquare(2)}
        </div>
        <div className="board-row">
          {this.renderSquare(3)}
          {this.renderSquare(4)}
          {this.renderSquare(5)}
        </div>
        <div className="board-row">
          {this.renderSquare(6)}
          {this.renderSquare(7)}
          {this.renderSquare(8)}
        </div>
      </div>
    );
  }
}

class Game extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      history: [
        {
          squares: Array(9).fill(null)
        }
      ],
      stepNumber: 0,
      start_pos: null,
      xIsNext: true,
      isSecondClick: false,
      mustMoveOrWin: false,
      
    };
  }

  handleClick(i) {
    const history = this.state.history.slice(0, this.state.stepNumber + 1);
    const current = history[history.length - 1];
    const squares = current.squares.slice();
    const currentPlayer = this.state.xIsNext ? "X" : "O"
    
    
    if(this.state.stepNumber<=5){
      if (calculateWinner(squares) || squares[i]) {
        return;
      }
      squares[i] = this.state.xIsNext ? "X" : "O";
      this.setState({
        history: history.concat([
          {
            squares: squares
          }
        ]),
        stepNumber: history.length,
        xIsNext: !this.state.xIsNext
      });
    }
    
    else{

      if(!this.state.isSecondClick){
        if(squares[4] === currentPlayer){
          this.setState({
            mustMoveOrWin: true
          })
        }
        if(squares[i] === currentPlayer){
          this.setState({
            start_pos: i,
            isSecondClick: true,
          })
        }
        else{
          return
        }
      }
      else{
        //console.log(this.state.start_pos)
        if(this.isPossible(currentPlayer,squares,this.state.mustMoveOrWin,this.state.start_pos,i)){
          //console.log('Yes this')
          squares[this.state.start_pos] = null;
          squares[i] = this.state.xIsNext ? "X" : "O";
          this.setState({
            history: history.concat([
              {
                squares: squares
              }
            ]),
            stepNumber: history.length,
            xIsNext: !this.state.xIsNext,
            mustMoveOrWin: false,
          }); 
        }
        this.setState({
          isSecondClick:false,
        })

        

      }
    }
  }
    

  
  jumpTo(step) {
    this.setState({
      stepNumber: step,
      xIsNext: (step % 2) === 0
    });
  }

  isPossible(currPlayer,squares,mustMoveOrWin,start,end){
    var i_start = start/3 | 0
    var j_start = (start%3)

    var i_end = end/3 | 0
    var j_end = end%3

   var i_dif = Math.abs(i_start - i_end)
   var j_dif = Math.abs(j_start - j_end)

   if(squares[end] === null){
     console.log(mustMoveOrWin)
    if(mustMoveOrWin){
      //console.log('sss')
      var tempS = squares[start]
      var tempE = squares[end]
      squares[end] = currPlayer
      squares[start] = null
      if(calculateWinner(squares)){
        squares[end] = tempE
        squares[start] = tempS
        console.log("hello")
        console.log(i_dif,j_dif)
        console.log(squares[end])
        if((i_dif <= 1 && j_dif <= 1) && (squares[end]===null)){
          //console.log(true)
          return true
          
        }
        //return true
      }
      squares[end] = tempE
      squares[start] = tempS
      
      //console.log(currPlayer)
      //console.log(squares[start])
      if(start !== 4 && currPlayer === squares[start]){
         //console.log("reached")
         return false
      }
      
      
    }
    //console.log('passed')
    
    //console.log(squares[end])
     if((i_dif <= 1 && j_dif <= 1) && (squares[end]===null)){
       //console.log(true)
       return true  
     }
    return false
   }
  }
 


  render() {
    const history = this.state.history;
    const current = history[this.state.stepNumber];
    const winner = calculateWinner(current.squares);

    const moves = history.map((step, move) => {
      const desc = move ?
        'Go to move #' + move :
        'Go to game start';
      return (
        <li key={move}>
          <button onClick={() => this.jumpTo(move)}>{desc}</button>
        </li>
      );
    });

    let status;
    if (winner) {
      status = "Winner: " + winner;
    } else {
      status = "Next player: " + (this.state.xIsNext ? "X" : "O");
    }

    return (
      <div className="game">
        <div className="game-board">
          <Board
            squares={current.squares}
            onClick={i => this.handleClick(i)}
          />
        </div>
        <div className="game-info">
          <div>{status}</div>
          <ol>{moves}</ol>
        </div>
      </div>
    );
  }
  
}

// ========================================

ReactDOM.render(<Game />, document.getElementById("root"));

function calculateWinner(squares) {
  const lines = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
  ];
  for (let i = 0; i < lines.length; i++) {
    const [a, b, c] = lines[i];
    if (squares[a] && squares[a] === squares[b] && squares[a] === squares[c]) {
      return squares[a];
    }
  }
  return null;
}
