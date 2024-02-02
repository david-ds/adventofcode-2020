#include <algorithm>
#include <array>
#include <cstdint>
#include <ctime>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>

static constexpr int kMaxAdapters = 128;
static std::array<std::int64_t, kMaxAdapters> kMem;

std::int64_t CountArrangements(const std::vector<int>& adapters, int index) {
  if (kMem[index] != 0) {
    return kMem[index];
  }
  int next_index = index + 1;
  std::int64_t result = 0;
  while (next_index < adapters.size() &&
         adapters[next_index] <= adapters[index] + 3) {
    result += CountArrangements(adapters, next_index);
    ++next_index;
  }
  kMem[index] = result;
  return result;
}

std::string run(const std::string& input) {
  // Your code goes here
  std::vector<int> adapters = {0};
  adapters.reserve(kMaxAdapters);
  std::istringstream iss(input);
  for (std::string line; std::getline(iss, line);) {
    adapters.push_back(std::atoi(line.c_str()));
  }
  std::sort(adapters.begin(), adapters.end());
  kMem[adapters.size() - 1] = 1;
  return std::to_string(CountArrangements(adapters, 0));
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
