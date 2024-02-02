#include <algorithm>
#include <ctime>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>

static constexpr int kMaxAdapters = 128;

std::string run(const std::string& input) {
  // Your code goes here
  std::vector<int> adapters;
  adapters.reserve(kMaxAdapters);
  std::istringstream iss(input);
  for (std::string line; std::getline(iss, line);) {
    adapters.push_back(std::atoi(line.c_str()));
  }
  std::sort(adapters.begin(), adapters.end());
  int count_1s = 0;
  int count_3s = 1;
  switch (adapters[0]) {
    case 1:
      ++count_1s;
      break;
    case 3:
      ++count_3s;
      break;
    default:
      break;
  }
  for (int idx = 1; idx < adapters.size(); ++idx) {
    switch (adapters[idx] - adapters[idx - 1]) {
      case 1:
        ++count_1s;
        break;
      case 3:
        ++count_3s;
        break;
      default:
        break;
    }
  }
  return std::to_string(count_1s * count_3s);
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
