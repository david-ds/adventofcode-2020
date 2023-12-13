#include <ctime>
#include <iostream>
#include <sstream>
#include <stdexcept>
#include <string>
#include <unordered_set>

static constexpr int kTargetSum = 2020;

std::string run(const std::string& input) {
  // Your code goes here
  std::istringstream iss(input);
  std::unordered_set<int> values;
  for (std::string line; std::getline(iss, line);) {
    int value = atoi(line.c_str());
    if (values.contains(kTargetSum - value))
      return std::to_string(value * (kTargetSum - value));
    values.insert(value);
  }
  throw std::invalid_argument("No pair sums to the target sum.");
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
