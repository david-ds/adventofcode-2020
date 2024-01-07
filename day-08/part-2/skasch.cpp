#include <array>
#include <bitset>
#include <ctime>
#include <iostream>
#include <optional>
#include <sstream>
#include <stdexcept>
#include <string>

static constexpr int kNInstructions = 1000;
static std::array<int, kNInstructions> kInstructions;

std::optional<int> Test(const std::string& input, int corrupted, int n_lines) {
  if (input[kInstructions[corrupted]] == 'a') return std::nullopt;
  int acc = 0;
  int pos = 0;
  std::bitset<kNInstructions> visited;
  while (!visited.test(pos) && pos != n_lines) {
    visited.set(pos);
    char c = input[kInstructions[pos]];
    if (pos == corrupted) {
      c = (c == 'n') ? 'j' : 'n';
    }
    switch (c) {
      case 'n': {
        ++pos;
        break;
      }
      case 'a': {
        acc += atoi(input
                        .substr(kInstructions[pos] + 4,
                                kInstructions[pos + 1] - 5 - kInstructions[pos])
                        .data());
        ++pos;
        break;
      }
      case 'j': {
        pos += atoi(input
                        .substr(kInstructions[pos] + 4,
                                kInstructions[pos + 1] - 5 - kInstructions[pos])
                        .data());
        break;
      }
      default: {
        std::cerr << kInstructions[pos] << "\n";
        throw std::invalid_argument("Invalid character found.");
      }
    }
  }
  return (pos == n_lines) ? std::make_optional(acc) : std::nullopt;
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
  for (int corrupted = 0; corrupted < line_idx; ++corrupted) {
    if (auto result = Test(input, corrupted, line_idx); result.has_value()) {
      return std::to_string(*result);
    }
  }
  throw std::invalid_argument("No corruption found");
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
