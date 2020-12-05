const { entries } = require("lodash");
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

let start = Date.now();
let answer = run(process.argv[2]);

console.log("_duration:" + (Date.now() - start).toString());
console.log(answer);
