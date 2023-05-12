import { useState } from 'react';

function Square({ value, onSquareClick }) {
  return (
    <button className="square" onClick={onSquareClick}>
      {value}
    </button>
  );
}

export default function Board() {
  //declares a state variable named squares that defaults to an array of 9 nulls corresponding to the 9 squares:
  //Array(9).fill(null) creates an array with nine elements and sets each of them to null. The useState() call around it declares a squares state variable that’s initially set to that array. Each entry in the array corresponds to the value of a square. When you fill the board in later, the squares array will look something like this:
  //['O', null, 'X', 'X', 'X', 'O', 'O', null, null]
  const [xIsNext, setXIsNext] = useState(true);
  const [squares, setSquares] = useState(Array(9).fill(null));
  const [squaresX, setSquaresX] = useState(Array(9).fill(null));
  const [squaresO, setSquaresO] = useState(Array(9).fill(null));

  const [countX = 0, setCountX] = useState();
  const [countO = 0, setCountO] = useState();


  function handleClick(i) {
    if (calculateWinner(squares)) {
      return;
    }
    const nextSquares = squares.slice();


    if (nextSquares[i] === 'X' && countX === 3 && xIsNext) {
      if (nextSquares[4] !== 'X' || (nextSquares[4] === 'X' && i === 4)) {
        nextSquares[i] = null;
        setCountX(countX - 1);
        setSquaresX(calculateValidMove(i))
      }

    }
    else if (nextSquares[i] === 'O' && countO === 3 && !xIsNext) {
      if (nextSquares[4] !== 'O' || (nextSquares[4] === 'O' && i === 4)) {
        nextSquares[i] = null;
        setCountO(countO - 1);
        setSquaresO(calculateValidMove(i))
      }
    }
    else if (xIsNext && !nextSquares[i] && countX < 3 && (!squaresX[i] || squaresX[i] === 'Y')) {
      nextSquares[i] = 'X';
      setCountX(countX + 1);
      if (squaresX[i] !== 'Y') {
        setXIsNext(!xIsNext);
      }

    } else if (!xIsNext && !nextSquares[i] && countO < 3 && (!squaresO[i] || squaresO[i] === 'Y')) {
      nextSquares[i] = 'O';
      setCountO(countO + 1);
      if (squaresO[i] !== 'Y') {
        setXIsNext(!xIsNext);
      }
    }
    setSquares(nextSquares);

  }


  const winner = calculateWinner(squares);
  let status;
  if (winner) {
    status = 'Winner: ' + winner;
  } else if (countX === 3 && xIsNext) {
    if (squares[4] === 'X') {
      status = "X must relocate the center piece"
    } else {
      status = "X must relocate an existing piece to an adjacent empty square";
    }
  } else if (countO === 3 && !xIsNext) {
    if (squares[4] === 'O') {
      status = "O must relocate the center piece"
    } else {
      status = "O must relocate an existing piece to an adjacent empty square";
    }
  } else {
    status = 'Next player: ' + (xIsNext ? 'X' : 'O');
  }

  return (
    <>
      <div className="status">{status}</div>
      <div className="board-row">
        <Square value={squares[0]} onSquareClick={() => handleClick(0)} />
        <Square value={squares[1]} onSquareClick={() => handleClick(1)} />
        <Square value={squares[2]} onSquareClick={() => handleClick(2)} />
      </div>
      <div className="board-row">
        <Square value={squares[3]} onSquareClick={() => handleClick(3)} />
        <Square value={squares[4]} onSquareClick={() => handleClick(4)} />
        <Square value={squares[5]} onSquareClick={() => handleClick(5)} />
      </div>
      <div className="board-row">
        <Square value={squares[6]} onSquareClick={() => handleClick(6)} />
        <Square value={squares[7]} onSquareClick={() => handleClick(7)} />
        <Square value={squares[8]} onSquareClick={() => handleClick(8)} />
      </div>
    </>
  );
}

function calculateWinner(squares) {
  const lines = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6],
  ];
  for (let i = 0; i < lines.length; i++) {
    const [a, b, c] = lines[i];
    if (squares[a] && squares[a] === squares[b] && squares[a] === squares[c]) {
      return squares[a];
    }
  }
  return null;
}

function calculateValidMove(square) {
  const moves = [
    ['Y', null, 'N', null, null, 'N', 'N', 'N', 'N'],
    [null, 'Y', null, null, null, null, 'N', 'N', 'N'],
    ['N', null, 'Y', 'N', null, null, 'N', 'N', 'N'],
    [null, null, 'N', 'Y', null, 'N', null, null, 'N'],
    [null, null, null, null, 'Y', null, null, null, null],
    ['N', null, null, 'N', null, 'Y', 'N', null, null],
    ['N', 'N', 'N', null, null, 'N', 'Y', null, 'N'],
    ['N', 'N', 'N', null, null, null, null, 'Y', null],
    ['N', 'N', 'N', 'N', null, null, 'N', null, 'Y']
  ];
  return moves[square];
}






