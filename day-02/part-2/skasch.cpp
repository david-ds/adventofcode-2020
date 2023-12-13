#include <ctime>
#include <iostream>
#include <sstream>
#include <string>

bool IsValid(const std::string& line) {
  int dash = line.find('-');
  int first = atoi(line.substr(0, dash).c_str());
  int space = line.find(' ', dash);
  int second = atoi(line.substr(dash + 1, space - dash - 1).c_str());
  char c = line[space + 1];
  return (line[space + 3 + first] == c) != (line[space + 3 + second] == c);
}

std::string run(const std::string& input) {
  // Your code goes here
  std::istringstream iss(input);
  int result = 0;
  for (std::string line; std::getline(iss, line);) {
    if (IsValid(line)) ++result;
  }
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
