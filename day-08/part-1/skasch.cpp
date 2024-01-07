#include <array>
#include <bitset>
#include <ctime>
#include <iostream>
#include <sstream>
#include <stdexcept>
#include <string>

static constexpr int kNInstructions = 1000;
static std::array<int, kNInstructions> kInstructions;
static std::bitset<kNInstructions> kVisited;

int Run(const std::string& input) {
  int acc = 0;
  int pos = 0;
  while (!kVisited.test(pos)) {
    kVisited.set(pos);
    switch (input[kInstructions[pos]]) {
      case 'n': {
        ++pos;
        break;
      }
      case 'a': {
        acc += atoi(input
                        .substr(kInstructions[pos] + 4,
                                kInstructions[pos + 1] - 5 - kInstructions[pos])
                        .c_str());
        ++pos;
        break;
      }
      case 'j': {
        pos += atoi(input
                        .substr(kInstructions[pos] + 4,
                                kInstructions[pos + 1] - 5 - kInstructions[pos])
                        .c_str());
        break;
      }
      default: {
        std::cerr << kInstructions[pos] << "\n";
        throw std::invalid_argument("Invalid character found.");
      }
    }
  }
  return acc;
}

std::string run(const std::string& input) {
  // Your code goes here
  std::istringstream iss(input);
  int line_idx = 1;
  kInstructions[0] = 0;
  for (int pos = 5; pos < input.size(); ++pos) {
    if (input[pos] == '\n') {
      kInstructions[line_idx] = pos + 1;
      pos += 5;
      ++line_idx;
    }
  }
  kInstructions[line_idx] = input.size() + 1;
  return std::to_string(Run(input));
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
