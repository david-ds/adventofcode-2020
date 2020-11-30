/**
 * @param {string} s puzzle input in string format
 * @returns {string} solution flag
 */
const run = (s: string): unknown => {
  // Your code goes here
  return s
};

let start = Date.now();
let answer = run(Deno.args[1]);

console.log("_duration:" + (Date.now() - start).toString());
console.log(answer);
