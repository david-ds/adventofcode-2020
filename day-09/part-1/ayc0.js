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
  lines.forEach((line, i) => {
    if (i < 25) {
      previous25.push(parseInt(line, 10));
    } else {
      rest.push(parseInt(line, 10));
    }
  });
  while (rest.length) {
    const valueToCheck = rest.shift();
    if (!isValid(previous25, valueToCheck)) {
      return valueToCheck;
    }
    previous25.shift();
    previous25.push(valueToCheck);
  }
  return -1;
};

const start = performance.now();
const answer = run(process.argv[2]);

console.log(`_duration:${performance.now() - start}`);
console.log(answer);
