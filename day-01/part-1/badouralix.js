const { performance } = require('perf_hooks');
const _ = require("lodash")

/**
 * @param {string} s puzzle input in string format
 * @returns {string} solution flag
 */
const run = s => {
  const entries = _.map(_.split(s, "\n"), _.toInteger)

  for (const [i, e] of Object.entries(entries)) {
    for (const f of _.slice(entries, _.toInteger(i) + 1)) {
      if (e + f == 2020) {
        return e * f
      }
    }
  }
};

const start = performance.now();
const answer = run(process.argv[2]);

console.log(`_duration:${performance.now() - start}`);
console.log(answer);
