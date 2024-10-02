var isSinglePlayer = false;
var isGameOver = false;
var turn = 1;

// Fireworks element
const fireworks = document.getElementById('fireworks');

// Set up Single Player and Multiplayer mode buttons
document.getElementById('singleplayer').addEventListener('click', function() {
  isSinglePlayer = true;
  resetGame();
  this.classList.add('selected');
  document.getElementById('multiplayer').classList.remove('selected');
});

document.getElementById('multiplayer').addEventListener('click', function() {
  isSinglePlayer = false;
  resetGame();
  this.classList.add('selected');
  document.getElementById('singleplayer').classList.remove('selected');
});

// Function to show fireworks
function displayFireworks() {
  fireworks.style.display = 'block';
}

// Function to hide fireworks
function hideFireworks() {
  fireworks.style.display = 'none';
}

// Function to reset the game state
function resetGame() {
  isGameOver = false;
  turn = 1;
  hideFireworks();

  // Clear all cells
  const cells = document.querySelectorAll('.cell');
  cells.forEach(cell => {
    cell.value = '';
    cell.style.backgroundColor = 'green';
  });
}

// Function to handle the moves
function move(cell) {
  if (isGameOver || cell.value !== '') return;

  // Make a move and check for a win
  cell.value = turn === 1 ? 'X' : 'O';
  cell.style.backgroundColor = turn === 1 ? 'red' : 'blue';

  if (checkWinner()) {
    displayFireworks();
    isGameOver = true;
    return;
  }

  // Toggle the turn
  turn = -turn;

  // In single player mode, make the AI move
  if (isSinglePlayer && turn === -1) {
    setTimeout(aiMove, 500); // Delay AI move for realism
  }
}

// Function to check if there's a winner
function checkWinner() {
  const cells = document.querySelectorAll('.cell');
  const state = Array.from(cells).map(cell => cell.value);

  const winningCombos = [
    [0, 1, 2], [3, 4, 5], [6, 7, 8], // rows
    [0, 3, 6], [1, 4, 7], [2, 5, 8], // columns
    [0, 4, 8], [2, 4, 6] // diagonals
  ];

  for (let combo of winningCombos) {
    const [a, b, c] = combo;
    if (state[a] && state[a] === state[b] && state[a] === state[c]) {
      return true;
    }
  }
  return false;
}

// Simple AI move for single player mode
function aiMove() {
  const cells = document.querySelectorAll('.cell');
  const emptyCells = Array.from(cells).filter(cell => cell.value === '');

  if (emptyCells.length > 0) {
    const randomCell = emptyCells[Math.floor(Math.random() * emptyCells.length)];
    randomCell.value = 'O';
    randomCell.style.backgroundColor = 'blue';

    if (checkWinner()) {
      displayFireworks();
      isGameOver = true;
    }

    turn = 1;
  }
}

// Reset button event listener
document.getElementById('reset').addEventListener('click', resetGame);
