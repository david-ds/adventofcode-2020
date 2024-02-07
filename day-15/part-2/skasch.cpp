#include <array>
#include <ctime>
#include <iostream>
#include <string>

static constexpr int kTargetIndex = 30'000'000;

static std::array<int, kTargetIndex> kState;

int Initialize(int& index, const std::string& input) {
  int left = 0;
  for (int right = 1; right < input.size(); ++right) {
    if (input[right] != ',') continue;
    kState[std::atoi(input.substr(left, right - left).c_str())] = index;
    ++index;
    ++right;
    left = right;
  }
  return std::atoi(input.substr(left).c_str());
}

std::string run(const std::string& input) {
  // Your code goes here
  int index = 1;
  int value = Initialize(index, input);
  int next_value;
  for (; index < kTargetIndex; ++index) {
    if (kState[value] == 0) {
      next_value = 0;
    } else {
      next_value = index - kState[value];
    }
    kState[value] = index;
    std::swap(value, next_value);
  }
  return std::to_string(value);
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
