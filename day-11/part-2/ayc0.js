// @ts-check

const { assert } = require("console");
const { performance } = require("perf_hooks");

/**
 * @typedef {0 | 1 | undefined} Value
 */

/**
 * @typedef {Value[]} Grid
 */

/**
 * @typedef {{ columns: number, lines: number }} Dimensions
 */

/**
 *
 * @param {Grid} a
 * @param {Grid} b
 * @returns {boolean}
 */
const isEqual = (a, b) => {
  for (let index = 0; index < a.length; index++) {
    if (a[index] !== b[index]) {
      return false;
    }
  }
  return true;
};

/**
 *
 * @param {string} s
 * @returns {Dimensions}
 */
const getDimensions = (s) => {
  const lines = s.split("\n");
  return {
    lines: lines.length,
    columns: lines[0].length,
  };
};

/**
 *
 * @param {string} s
 * @param {Dimensions} dimensions
 * @returns {Grid}
 */
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

/**
 *
 * @param {number} index
 * @param {Grid} grid
 * @param {number} offset
 * @param {Dimensions} direction
 * @param {Dimensions} dimensions
 * @returns {Value | null}
 */
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

/**
 *
 * @param {number} index
 * @param {Grid} grid
 * @param {Dimensions} dimensions
 * @returns {number}
 */
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

  /** @type {Dimensions[]} */
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

/**
 *
 * @param {Grid} grid
 * @param {Dimensions} dimensions
 * @returns {Grid}
 */
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

// /**
//  *
//  * @param {Grid} grid
//  * @param {Dimensions} dimensions
//  */
// const print = (grid, dimensions) => {
//   console.log("");
//   for (let line = 0; line < dimensions.lines; line++) {
//     console.log(
//       grid
//         .slice(line * dimensions.columns, (line + 1) * dimensions.columns)
//         .map((v) => (v === 1 ? "#" : v === 0 ? "L" : "."))
//         .join("")
//     );
//   }
// };

/**
 * @param {string} s puzzle input in string format
 * @returns {number} solution flag
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
  return total;
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

const computed = run(input);
assert(computed === 26, computed);

const start = performance.now();
const answer = run(process.argv[2]);

console.log(`_duration:${performance.now() - start}`);
console.log(answer);
