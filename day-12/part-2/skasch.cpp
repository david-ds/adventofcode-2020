#include <ctime>
#include <iostream>
#include <sstream>
#include <stdexcept>
#include <string>

struct State {
  int x = 0;
  int y = 0;
  int dx = 10;
  int dy = 1;
};

void Update(State& state, const std::string& line) {
  int value = std::atoi(line.substr(1).c_str());
  switch (line[0]) {
    case 'N': {
      state.dy += value;
      break;
    }
    case 'S': {
      state.dy -= value;
      break;
    }
    case 'E': {
      state.dx += value;
      break;
    }
    case 'W': {
      state.dx -= value;
      break;
    }
    case 'L': {
      value = 360 - value;
    }
    case 'R': {
      switch (value) {
        case 90: {
          int dx = state.dx;
          state.dx = state.dy;
          state.dy = -dx;
          break;
        }
        case 180: {
          state.dx = -state.dx;
          state.dy = -state.dy;
          break;
        }
        case 270: {
          int dx = state.dx;
          state.dx = -state.dy;
          state.dy = dx;
          break;
        }
        default: {
          throw std::invalid_argument("Invalid angle.");
        }
      }
      break;
    }
    case 'F': {
      state.x += state.dx * value;
      state.y += state.dy * value;
      break;
    }
    default: {
      throw std::invalid_argument("Invalid first letter.");
    }
  }
}

std::string run(const std::string& input) {
  // Your code goes here
  std::istringstream iss(input);
  State state;
  for (std::string line; std::getline(iss, line);) {
    Update(state, line);
  }
  return std::to_string(std::abs(state.x) + std::abs(state.y));
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
