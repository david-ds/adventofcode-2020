const { performance } = require("perf_hooks");

let acc = 0;

const parseLine = (lineNb, line) => {
  const op = line.substring(0, 3);
  const value = parseInt(line.substring(4), 10);
  switch (op) {
    default:
    case "nop":
      return lineNb + 1;
    case "acc":
      acc += value;
      return lineNb + 1;
    case "jmp":
      return lineNb + value;
  }
};

/**
 * @param {string} s puzzle input in string format
 * @returns {string} solution flag
 */
const run = (s) => {
  const lines = s.trimEnd().split("\n");
  const visitedLines = new Set();
  let lineNb = 0;
  while (!visitedLines.has(lineNb)) {
    visitedLines.add(lineNb);
    lineNb = parseLine(lineNb, lines[lineNb]);
  }
  return acc;
};

const start = performance.now();
const answer = run(process.argv[2]);

console.log(`_duration:${performance.now() - start}`);
console.log(answer);
