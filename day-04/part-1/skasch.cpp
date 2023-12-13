#include <ctime>
#include <iostream>
#include <sstream>
#include <string>
#include <string_view>

static constexpr std::string_view kIgnore = "cid";
static constexpr int kKeysToFind = 7;

bool ParseLine(const std::string& line, int& remaining_keys) {
  if (line.size() == 0) return true;
  for (int pos = 0; pos < line.size();) {
    int sep = line.find(':', pos);
    if (line.substr(pos, sep - pos) != kIgnore) --remaining_keys;
    pos = line.find(' ', sep) + 1;
    if (pos == 0) break;
  }
  return false;
}

std::string run(const std::string& input) {
  // Your code goes here
  std::istringstream iss(input);
  int remaining_keys = kKeysToFind;
  int result = 0;
  for (std::string line; std::getline(iss, line);) {
    if (ParseLine(line, remaining_keys)) {
      if (remaining_keys == 0) ++result;
      remaining_keys = kKeysToFind;
    }
  }
  if (remaining_keys == 0) ++result;
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
