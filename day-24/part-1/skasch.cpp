#include <ctime>
#include <iostream>
#include <sstream>
#include <string>
#include <unordered_map>
#include <unordered_set>

static std::unordered_map<int, std::unordered_set<int>> kFlipped;
static int kFlippedCount = 0;

void Flip(const std::string &line) {
  int pos = 0;
  int row = 0;
  int col = 0;
  while (pos < line.size()) {
    switch (line[pos]) {
    case 'w':
      col -= 2;
      break;
    case 'e':
      col += 2;
      break;
    case 'n': {
      --row;
      ++pos;
      switch (line[pos]) {
      case 'w':
        --col;
        break;
      case 'e':
        ++col;
        break;
      }
      break;
    }
    case 's': {
      ++row;
      ++pos;
      switch (line[pos]) {
      case 'w':
        --col;
        break;
      case 'e':
        ++col;
        break;
      }
      break;
    }
    }
    ++pos;
  }
  auto it = kFlipped.find(row);
  if (it != kFlipped.end()) {
    auto it2 = it->second.find(col);
    if (it2 != it->second.end()) {
      it->second.erase(it2);
      --kFlippedCount;
      return;
    }
  }
  kFlipped[row].insert(col);
  ++kFlippedCount;
}

std::string run(const std::string &input) {
  // Your code goes here
  std::istringstream iss(input);
  for (std::string line; std::getline(iss, line);) {
    Flip(line);
  }
  return std::to_string(kFlippedCount);
}

int main(int argc, char **argv) {
  if (argc < 2) {
    std::cout << "Missing one argument" << std::endl;
    exit(1);
  }

  clock_t start = clock();
  auto answer = run(argv[1]);

  std::cout << "_duration:" << float(clock() - start) * 1000.0 / CLOCKS_PER_SEC
            << "\n";
  std::cout << answer << "\n";
  return 0;
}
