#include <ctime>
#include <iostream>
#include <sstream>
#include <string>

int ToId(const std::string& line) {
  int res = 0;
  for (char c : line) {
    res <<= 1;
    if (c == 'B' || c == 'R') res += 1;
  }
  return res;
}

std::string run(const std::string& input) {
  // Your code goes here
  std::istringstream iss(input);
  int res = 0;
  for (std::string line; std::getline(iss, line);) {
    int id = ToId(line);
    res = std::max(res, id);
  }
  return std::to_string(res);
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
