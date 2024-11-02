#include <array>
#include <ctime>
#include <iostream>
#include <sstream>
#include <string>
#include <unordered_map>
#include <unordered_set>

static std::unordered_map<int, std::unordered_set<int>> kFlipped;
static int kFlippedCount = 0;
static constexpr std::array<std::pair<int, int>, 6> kNeighbors = {
    {{0, -2}, {-1, -1}, {-1, 1}, {0, 2}, {1, 1}, {1, -1}}};
static constexpr int kCycles = 100;

bool Contains(int row, int col) {
  auto it = kFlipped.find(row);
  if (it != kFlipped.end()) {
    return it->second.find(col) != it->second.end();
  }
  return false;
}

std::pair<int, int> FindPos(const std::string &line) {
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
  return {row, col};
}

void Flip(int row, int col) {
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

int CountBlackNeighbors(int row, int col) {
  int cnt = 0;
  for (const auto &[dr, dc] : kNeighbors) {
    if (Contains(row + dr, col + dc)) {
      ++cnt;
    }
  }
  return cnt;
}

void Animate() {
  std::unordered_map<int, std::unordered_set<int>> to_flip;
  for (const auto &[row, cols] : kFlipped) {
    for (const int col : cols) {
      int cnt = CountBlackNeighbors(row, col);
      if (cnt == 0 || cnt > 2) {
        to_flip[row].insert(col);
      }
      for (const auto &[dr, dc] : kNeighbors) {
        if (Contains(row + dr, col + dc)) {
          continue;
        }
        if (CountBlackNeighbors(row + dr, col + dc) == 2) {
          to_flip[row + dr].insert(col + dc);
        }
      }
    }
  }
  for (const auto &[row, cols] : to_flip) {
    for (const int col : cols) {
      Flip(row, col);
    }
  }
}

std::string run(const std::string &input) {
  // Your code goes here
  std::istringstream iss(input);
  for (std::string line; std::getline(iss, line);) {
    auto [row, col] = FindPos(line);
    Flip(row, col);
  }
  for (int cycle = 0; cycle < kCycles; ++cycle) {
    Animate();
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
