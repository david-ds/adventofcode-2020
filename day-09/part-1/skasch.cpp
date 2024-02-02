#include <array>
#include <ctime>
#include <iostream>
#include <sstream>
#include <stdexcept>
#include <string>
#include <unordered_map>

static constexpr int kBufferSize = 25;

static std::array<int, kBufferSize> kBuffer;
static int kIndex = 0;
static std::unordered_map<int, int> kValues;

void Initialize(std::istringstream& iss) {
  std::string line;
  for (int idx = 0; idx < kBufferSize; ++idx) {
    std::getline(iss, line);
    kBuffer.at(idx) = std::atoi(line.c_str());
    ++kValues[kBuffer.at(idx)];
  }
}

bool IsValid(int value) {
  for (int other : kBuffer) {
    if (kValues.contains(value - other)) return true;
  }
  return false;
}

void Update(int value) {
  int prev = kBuffer.at(kIndex);
  kBuffer.at(kIndex) = value;
  kIndex = (kIndex + 1) % kBufferSize;
  --kValues[prev];
  if (kValues[prev] == 0) kValues.erase(prev);
  ++kValues[value];
}

std::string run(const std::string& input) {
  // Your code goes here
  std::istringstream iss(input);
  Initialize(iss);
  for (std::string line; std::getline(iss, line);) {
    int value = std::atoi(line.c_str());
    if (!IsValid(value)) return line;
    Update(value);
  }
  throw std::invalid_argument("Failed to find an invalid value.");
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
