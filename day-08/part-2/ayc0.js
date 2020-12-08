const { performance } = require("perf_hooks");

let acc;

const parseLine = (lineNb, line, lineToChange) => {
  const op = line.substring(0, 3);
  const value = parseInt(line.substring(4), 10);
  const shouldChange = lineNb === lineToChange;
  if (op === "acc") {
    acc += value;
    return lineNb + 1;
  }
  if ((op === "nop" && !shouldChange) || (op === "jmp" && shouldChange)) {
    return lineNb + 1;
  }

  if ((op === "jmp" && !shouldChange) || (op === "nop" && shouldChange)) {
    return lineNb + value;
  }

  return lineNb + 1;
};

/**
 * @param {string} s puzzle input in string format
 * @returns {string} solution flag
 */
const run = (s) => {
  const lines = s.trimEnd().split("\n");
  const possibleLinesToChange = new Set();

  let i = 0;
  for (const line of lines) {
    if (line.startsWith("acc")) {
      i++;
      continue;
    }
    possibleLinesToChange.add(i++);
  }

  const visitedLines = new Set();

  mainLoop: for (const lineToChange of possibleLinesToChange) {
    visitedLines.clear();
    acc = 0;
    let lineNb = 0;
    while (true) {
      if (lineNb >= lines.length) {
        break mainLoop;
      }
      if (visitedLines.has(lineNb)) {
        break;
      }
      visitedLines.add(lineNb);
      lineNb = parseLine(lineNb, lines[lineNb], lineToChange);
    }
    acc = 0;
  }

  return acc;
};

const start = performance.now();
const answer = run(process.argv[2]);

console.log(`_duration:${performance.now() - start}`);
console.log(answer);
