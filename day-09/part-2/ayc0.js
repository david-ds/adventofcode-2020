const { performance } = require("perf_hooks");

const isValid = (range, nb) => {
  for (let i = 0; i < 24; i++) {
    for (let j = i + 1; j < 25; j++) {
      if (range[i] + range[j] === nb) {
        return true;
      }
    }
  }
  return false;
};

/**
 * @param {string} s puzzle input in string format
 * @returns {string} solution flag
 */
const run = (s) => {
  const lines = s.trim().split("\n");
  const previous25 = [];
  const rest = [];
  const checked = [];
  lines.forEach((line, i) => {
    if (i < 25) {
      previous25.push(parseInt(line, 10));
    } else {
      rest.push(parseInt(line, 10));
    }
  });
  let valueToCheck;
  while (rest.length) {
    valueToCheck = rest.shift();
    if (!isValid(previous25, valueToCheck)) {
      break;
    }
    checked.push(previous25.shift());
    previous25.push(valueToCheck);
  }
  for (let i = 0; i < 25; i++) {
    checked.push(previous25.shift());
  }
  let sum = 0;
  let base = checked.length - 1;
  let i = base;
  while (base) {
    sum = 0;
    i = base;
    while (sum < valueToCheck) {
      sum += checked[i--];
    }
    if (sum === valueToCheck) {
      const contiguous = checked.slice(i + 1, base + 1);
      return Math.min(...contiguous) + Math.max(...contiguous);
    }
    base--;
  }
};

const start = performance.now();
const answer = run(process.argv[2]);

console.log(`_duration:${performance.now() - start}`);
console.log(answer);
