const { performance } = require("perf_hooks");

const bags = new Map();

const getContent = (color) => {
  let bag = bags.get(color);
  if (bag) {
    return bag;
  }
  bag = [];
  bags.set(color, bag);
  return bag;
};

const parseLine = (line) => {
  // shiny gold bags contain 2 dark red bags
  const [, colorName, contentChunks] = line.match(
    /([a-z ]*) bags contain (.*)\./
  );
  const bag = getContent(colorName);
  if (contentChunks === "no other bags") {
    return;
  }
  for (const contentChunk of contentChunks.split(", ")) {
    const [, number, color] = contentChunk.match(/([0-9]+) ([a-z ]*) bag.*?/);
    const subContent = getContent(color);
    bag.push({
      quantity: parseInt(number, 10),
      content: subContent,
    });
  }
};

const getNb = (content) => {
  let count = 1;
  for (const child of content) {
    count += child.quantity * getNb(child.content);
  }
  return count;
};

const run = (s) => {
  for (const line of s.trim().split("\n")) {
    parseLine(line);
  }
  return getNb(bags.get("shiny gold")) - 1;
};

let start = performance.now();
let answer = run(process.argv[2]);

console.log(`_duration:${performance.now() - start}`);
console.log(answer);
