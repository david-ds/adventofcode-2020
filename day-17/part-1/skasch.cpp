#include <array>
#include <ctime>
#include <iostream>
#include <string>
#include <unordered_set>
#include <utility>

static constexpr int kSize = 8;
static constexpr int kCycles = 6;
static constexpr int kEdge = 2 * kCycles + kSize;
static constexpr int kHeight = 2 * kCycles + 1;
static constexpr int kCubeSize = kEdge * kEdge * kHeight;

struct P {
  int x;
  int y;
  int z;

  P operator+(const P &o) { return {x + o.x, y + o.y, z + o.z}; }
};

constexpr int to_index(const P &p) {
  return p.x + kEdge * p.y + kEdge * kEdge * p.z;
}

bool contains(const std::unordered_set<int> &s, int v) {
  return s.find(v) != s.end();
}

static std::array<P, 26> kNeighbors = {
    P{-1, -1, -1}, P{-1, -1, 0}, P{-1, -1, 1}, P{-1, 0, -1}, P{-1, 0, 0},
    P{-1, 0, 1},   P{-1, 1, -1}, P{-1, 1, 0},  P{-1, 1, 1},  P{0, -1, -1},
    P{0, -1, 0},   P{0, -1, 1},  P{0, 0, -1},  P{0, 0, 1},   P{0, 1, -1},
    P{0, 1, 0},    P{0, 1, 1},   P{1, -1, -1}, P{1, -1, 0},  P{1, -1, 1},
    P{1, 0, -1},   P{1, 0, 0},   P{1, 0, 1},   P{1, 1, -1},  P{1, 1, 0},
    P{1, 1, 1},
};

void Iterate(std::unordered_set<int> &active, int cycle) {
  std::unordered_set<int> new_active;
  for (int x = -cycle; x < kSize + cycle; ++x) {
    for (int y = -cycle; y < kSize + cycle; ++y) {
      for (int z = -cycle; z < 1 + cycle; ++z) {
        P pos = {x, y, z};
        int cnt = 0;
        for (const P &neighbor : kNeighbors) {
          if (contains(active, to_index(pos + neighbor))) {
            ++cnt;
          }
        }
        int index = to_index(pos);
        if (contains(active, index)) {
          if (cnt == 2 || cnt == 3) {
            new_active.insert(index);
          }
        } else {
          if (cnt == 3) {
            new_active.insert(index);
          }
        }
      }
    }
  }
  std::swap(active, new_active);
}

std::string run(const std::string &input) {
  int x = 0;
  int y = 0;
  std::unordered_set<int> active = {};
  for (auto c : input) {
    if (c == '\n') {
      ++x;
      y = 0;
      continue;
    }
    if (c == '#') {
      active.insert(to_index({x, y, 0}));
    }
    ++y;
  }
  for (int cycle = 1; cycle <= kCycles; ++cycle) {
    Iterate(active, cycle);
  }
  return std::to_string(active.size());
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
