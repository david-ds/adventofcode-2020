const { performance } = require("perf_hooks");

let mask = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX";
const memory = new Map();
const allOnes = BigInt(2 ** 36 - 1);

/**
 *
 * @param {string} s
 * @returns
 */
const run = (s) => {
  for (const line of s.trim().split("\n")) {
    // mask = "<>"
    if (line[1] === "a") {
      mask = line.substring(7, line.length);
      //   console.log(mask);
      continue;
    }

    // mem[<entry>] = <value>
    var indexOfEndBracket = line.indexOf("]");
    if (indexOfEndBracket == -1) continue;
    // to catch the values in "mem[<entry>] = <value>
    const entry = BigInt(line.substring(4, indexOfEndBracket));
    const value = Number(line.substring(indexOfEndBracket + 4, line.length));
    // console.log(entry, "<-", value);

    let correctedEntry = entry;
    const floatings = [];

    // 36 is the length of the mask
    let thisMask;
    for (let i = 0; i < 36; i++) {
      thisMask = mask[35 - i];
      if (thisMask === "0") {
        continue;
      } else if (thisMask === "1") {
        correctedEntry = correctedEntry | (1n << BigInt(i));
      } else {
        floatings.push(BigInt(i));
      }
    }

    // console.log(floatings);

    let correctedEntries = [correctedEntry];
    let tmpCorrectedEntries = [];
    for (const floating of floatings) {
      for (const correctedEntry of correctedEntries) {
        // marked bit at floating to 0
        tmpCorrectedEntries.push(correctedEntry & (allOnes - (1n << floating)));
        // marked bit at floating to 1
        tmpCorrectedEntries.push(correctedEntry | (1n << floating));
      }
      correctedEntries = tmpCorrectedEntries;
      tmpCorrectedEntries = [];
    }

    // console.log(correctedEntries);
    for (const correctedEntry of correctedEntries) {
      memory.set(correctedEntry, value);
    }
  }

  let total = 0;
  for (const value of memory.values()) {
    total += value;
  }
  return total;
};

let start = performance.now();
let input = process.argv[2];
// input = `
// mask = 000000000000000000000000000000X1001X
// mem[42] = 100
// mask = 00000000000000000000000000000000X0XX
// mem[26] = 1
// `;

let answer = run(input);

console.log(`_duration:${performance.now() - start}`);
console.log(answer);
