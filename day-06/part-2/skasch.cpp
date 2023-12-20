#include <array>
#include <ctime>
#include <iostream>
#include <sstream>
#include <string>

static std::array<int32_t, 26> kMasks = {
    1 << 0,  1 << 1,  1 << 2,  1 << 3,  1 << 4,  1 << 5,  1 << 6,
    1 << 7,  1 << 8,  1 << 9,  1 << 10, 1 << 11, 1 << 12, 1 << 13,
    1 << 14, 1 << 15, 1 << 16, 1 << 17, 1 << 18, 1 << 19, 1 << 20,
    1 << 21, 1 << 22, 1 << 23, 1 << 24, 1 << 25};

static int32_t kBase = (1 << 26) - 1;

int32_t ParseLine(const std::string& line) {
  int bitmap = 0;
  for (char c : line) {
    bitmap |= kMasks[c - 'a'];
  }
  return bitmap;
}

int CountOnes(int32_t bitmap) {
  int result = 0;
  while (bitmap > 0) {
    result += bitmap & 1;
    bitmap >>= 1;
  }
  return result;
}

std::string run(const std::string& input) {
  // Your code goes here
  std::istringstream iss(input);
  int32_t answers = kBase;
  int result = 0;
  for (std::string line; std::getline(iss, line);) {
    if (line.size() == 0) {
      result += CountOnes(answers);
      answers = kBase;

      continue;
    }
    answers &= ParseLine(line);
  }
  result += CountOnes(answers);
  return std::to_string(result);
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
