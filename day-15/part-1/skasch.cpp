#include <ctime>
#include <iostream>
#include <string>
#include <unordered_map>

static constexpr int kTargetIndex = 2020;

using State = std::unordered_map<int, int>;

int Initialize(int& index, State& state, const std::string& input) {
  int left = 0;
  for (int right = 1; right < input.size(); ++right) {
    if (input[right] != ',') continue;
    state[std::atoi(input.substr(left, right - left).c_str())] = index;
    ++index;
    ++right;
    left = right;
  }
  return std::atoi(input.substr(left).c_str());
}

std::string run(const std::string& input) {
  // Your code goes here
  State state;
  int index = 1;
  int value = Initialize(index, state, input);
  int next_value;
  for (; index < kTargetIndex; ++index) {
    auto it = state.find(value);
    if (it == state.end()) {
      next_value = 0;
      state[value] = index;
    } else {
      next_value = index - it->second;
      it->second = index;
    }
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
