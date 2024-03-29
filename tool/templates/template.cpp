#include <ctime>
#include <iostream>
#include <sstream>
#include <string>

std::string run(const std::string& input) {
  // Your code goes here
  std::istringstream iss(input);
  for (std::string line; std::getline(iss, line);) {
  }
  return std::to_string(0);
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
