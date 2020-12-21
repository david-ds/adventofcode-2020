/**
 * @param {string} s puzzle input in string format
 * @returns {string} solution flag
 */
const run = (s) => {
  // Your code goes here
};

let start = performance.now();
let answer = run(Deno.args[0]);

console.log(`_duration:${performance.now() - start}`);
console.log(answer);
