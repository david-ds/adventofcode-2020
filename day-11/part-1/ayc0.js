// @ts-check

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
 * @param {Dimensions} dimensions
 * @returns {number}
 */
const getNeighbors = (index, grid, dimensions) => {
  let neighbors = 0;
  /**
   *
   * @param {Value} v
   */
  const addNeighbor = (v) => {
    if (v === 1) {
      neighbors++;
    }
  };
  const placementInLine = index % dimensions.columns;
  const isFirstCol = placementInLine === 0;
  const isLastCol = placementInLine === dimensions.columns - 1;
  const placementInColumn = Math.floor(index / dimensions.columns);
  const isFirstLine = placementInColumn === 0;
  const isLastLine = placementInColumn === dimensions.lines - 1;
  if (!isFirstCol) {
    addNeighbor(grid[index - 1]);
    if (!isFirstLine) {
      addNeighbor(grid[index - 1 - dimensions.columns]);
    }
    if (!isLastLine) {
      addNeighbor(grid[index - 1 + dimensions.columns]);
    }
  }
  if (!isLastCol) {
    addNeighbor(grid[index + 1]);
    if (!isFirstLine) {
      addNeighbor(grid[index + 1 - dimensions.columns]);
    }
    if (!isLastLine) {
      addNeighbor(grid[index + 1 + dimensions.columns]);
    }
  }
  if (!isFirstLine) {
    addNeighbor(grid[index - dimensions.columns]);
  }
  if (!isLastLine) {
    addNeighbor(grid[index + dimensions.columns]);
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
      // newGrid[index] = undefined;
      continue;
    }
    const neighbors = getNeighbors(index, grid, dimensions);
    if (state === 0 && neighbors === 0) {
      newGrid[index] = 1;
    } else if (state === 1 && neighbors >= 4) {
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

const start = performance.now();
const answer = run(process.argv[2]);

console.log(`_duration:${performance.now() - start}`);
console.log(answer);
