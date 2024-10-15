#include <cstdint>
#include <ctime>
#include <iostream>
#include <optional>
#include <string>
#include <vector>

struct State {
  std::vector<std::optional<int64_t>> vals;
  std::vector<char> ops;
};

void Parse(char t, State &state) {
  switch (t) {
  case ' ':
    break;
  case '+':
  case '*': {
    state.ops.push_back(t);
    break;
  }
  case '(': {
    state.vals.push_back(std::nullopt);
    break;
  }
  case ')': {
    int64_t r = *state.vals.back();
    state.vals.pop_back();
    if (!state.vals.back().has_value()) {
      state.vals.back() = r;
    } else {
      char op = state.ops.back();
      state.ops.pop_back();
      if (op == '+') {
        state.vals.back() = *state.vals.back() + r;
      } else {
        state.vals.back() = *state.vals.back() * r;
      }
    }
    break;
  }
  default: {
    int64_t v = std::atoi(&t);
    if (!state.vals.back().has_value()) {
      state.vals.back() = v;
    } else {
      char op = state.ops.back();
      state.ops.pop_back();
      if (op == '+') {
        state.vals.back() = *state.vals.back() + v;
      } else {
        state.vals.back() = *state.vals.back() * v;
      }
    }
    break;
  }
  }
}

std::string run(const std::string &input) {
  State state = {.vals = {std::nullopt}};
  int64_t result = 0;
  for (char c : input) {
    if (c == '\n') {
      result += *state.vals.back();
      state = {.vals = {std::nullopt}};
      continue;
    }
    Parse(c, state);
  }
  result += *state.vals.back();
  return std::to_string(result);
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
