const isEqual = (a, b) => {
  for (let index = 0; index < a.length; index++) {
    if (a[index] !== b[index]) {
      return false;
    }
  }
  return true;
};

const getDimensions = (s) => {
  const lines = s.split("\n");
  return {
    lines: lines.length,
    columns: lines[0].length,
  };
};

const analyze = (s, dimensions) => {
  const grid = new Array(dimensions.columns * dimensions.lines).fill(undefined);
  let i = 0;
  for (const char of s) {
    if (char === "\n") {
      continue;
    }
    if (char === ".") {
      grid[i] = undefined;
    } else if (char === "L") {
      grid[i] = 0;
    } else {
      grid[i] = 1;
    }

    i++;
  }
  return grid;
};

const getNeighbor = (index, grid, offset, direction, dimensions) => {
  const column = index % dimensions.columns;
  const line = Math.floor(index / dimensions.columns);
  const newColumn = column + offset * direction.columns;
  const newLine = line + offset * direction.lines;
  if (
    newColumn < 0 ||
    newLine < 0 ||
    newColumn >= dimensions.columns ||
    newLine >= dimensions.lines
  ) {
    return null;
  }
  return grid[newLine * dimensions.columns + newColumn];
};

const getNeighbors = (index, grid, dimensions) => {
  let neighbors = 0;
  /**
   *
   * @param {Value | null} v
   */
  const addNeighbor = (v) => {
    if (v === 1) {
      neighbors++;
    }
  };

  const directions = [
    { lines: 0, columns: 1 },
    { lines: 0, columns: -1 },
    { lines: 1, columns: 1 },
    { lines: 1, columns: 0 },
    { lines: 1, columns: -1 },
    { lines: -1, columns: 1 },
    { lines: -1, columns: 0 },
    { lines: -1, columns: -1 },
  ];

  for (const direction of directions) {
    let neighbor = undefined;
    let offset = 1;
    while (neighbor === undefined) {
      neighbor = getNeighbor(index, grid, offset++, direction, dimensions);
    }
    addNeighbor(neighbor);
  }

  return neighbors;
};

const nextStep = (grid, dimensions) => {
  const newGrid = new Array(grid.length).fill(undefined);
  for (let index = 0; index < grid.length; index++) {
    const state = grid[index];
    if (state === undefined) {
      newGrid[index] = undefined;
      continue;
    }
    const neighbors = getNeighbors(index, grid, dimensions);
    if (state === 0 && neighbors === 0) {
      newGrid[index] = 1;
    } else if (state === 1 && neighbors >= 5) {
      newGrid[index] = 0;
    } else {
      newGrid[index] = state;
    }
  }
  return newGrid;
};

/**
 * @param {string} s puzzle input in string format
 * @returns {string} solution flag
 */
const run = (s) => {
  s = s.trim();
  const dimensions = getDimensions(s);
  let prevGrid = analyze(s, dimensions);
  /** @type {Grid} */
  let newGrid;
  while (true) {
    newGrid = nextStep(prevGrid, dimensions);
    // print(newGrid, dimensions);
    if (isEqual(newGrid, prevGrid)) {
      break;
    }
    prevGrid = newGrid;
  }
  let total = 0;
  for (const seat of newGrid) {
    if (seat === 1) {
      total++;
    }
  }
  return total.toString();
};

const input = `L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL
`;

run(input);

const start = performance.now();
const answer = run(Deno.args[0]);

console.log(`_duration:${performance.now() - start}`);
console.log(answer);
