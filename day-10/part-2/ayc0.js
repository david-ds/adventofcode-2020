const { performance } = require("perf_hooks");

/**
 * @param {string} s puzzle input in string format
 * @returns {string} solution flag
 */
const run = (s) => {
  // Your code goes here
  let max = 0;
  const counts = {};
  const array = s
    .trim()
    .split("\n")
    .map(Number)
    .sort((a, b) => {
      if (a > max) {
        max = a;
      }
      counts[a] = 0;
      return a - b;
    });

  array.unshift(0);
  array.push(max + 3);
  counts[0] = 0;
  counts[max + 3] = 1;

  for (let index = array.length - 2; index >= 0; index--) {
    const cur = array[index];
    let count = 0;
    for (let shift = 3; shift >= 1; shift--) {
      if (index + shift >= array.length || array[index + shift] > cur + 3) {
        continue;
      }

      count += counts[array[index + shift]];
    }

    counts[array[index]] = count;
  }

  return counts[0];
};

// const input1 = `
// 16
// 10
// 15
// 5
// 1
// 11
// 7
// 19
// 6
// 12
// 4
// `;
// const input2 = `28
// 33
// 18
// 42
// 31
// 14
// 46
// 20
// 48
// 47
// 24
// 23
// 49
// 45
// 19
// 38
// 39
// 11
// 1
// 32
// 25
// 35
// 8
// 17
// 7
// 9
// 4
// 2
// 34
// 10
// 3
// `;
// assert(run(input1) === 8, "Doesn't match 8 but " + run(input1));
// assert(run(input2) === 19208, "Doesn't match 19208 but " + run(input2));

const input = process.argv[2];

// run 2 times to optimize JIT
run(input);
run(input);

const start = performance.now();
const answer = run(input);

console.log(`_duration:${performance.now() - start}`);
console.log(answer);
