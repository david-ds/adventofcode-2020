const { performance } = require("perf_hooks");

/**
 * @param {string} s puzzle input in string format
 * @returns {string} solution flag
 */
const run = (s) => {
  // Your code goes here
  const array = s
    .trim()
    .split("\n")
    .map(Number)
    .sort((a, b) => a - b);
  const results = { 1: 0, 2: 0, 3: 1 };
  let prev = 0;
  array.forEach((cur) => {
    results[cur - prev]++;
    prev = cur;
  });
  return results["3"] * results["1"];
};

const start = performance.now();
const answer = run(process.argv[2]);

console.log(`_duration:${performance.now() - start}`);
console.log(answer);
