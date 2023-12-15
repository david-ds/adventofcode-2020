#include <ctime>
#include <iostream>
#include <sstream>
#include <stdexcept>
#include <string>
#include <vector>

static constexpr int kNChars = 10;
static constexpr int kNCombinations = 1 << 10;
static std::vector<bool> kMap(kNCombinations);

int ToId(const std::string& line) {
  int res = 0;
  for (char c : line) {
    res <<= 1;
    if (c == 'B' || c == 'R') res += 1;
  }
  return res;
}

std::string run(const std::string& input) {
  // Your code goes here
  std::istringstream iss(input);
  for (std::string line; std::getline(iss, line);) {
    int id = ToId(line);
    kMap.at(id) = true;
  }
  for (int id = 1; id < kNCombinations - 1; ++id) {
    if (!kMap.at(id) && kMap.at(id - 1) && kMap.at(id + 1))
      return std::to_string(id);
  }
  throw std::invalid_argument("No valid id");
}

int main(int argc, char** argv) {
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
