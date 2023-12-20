#include <array>
#include <ctime>
#include <iostream>
#include <sstream>
#include <string>
#include <unordered_map>
#include <vector>

static constexpr int kNBags = 1024;

struct Bags {
  std::array<std::vector<int>, kNBags> content;
  std::unordered_map<std::string, int> names;
};

int GetColorEnd(const std::string& line, int pos) {
  return line.find(' ', line.find(' ', pos) + 1);
}

void ParseLine(const std::string& line, Bags& bags) {
  int right = GetColorEnd(line, 0);
  int index = bags.names[line.substr(0, right)];
  int pos = right + 16;  // " bags contain X "
  if (line[pos] == ' ') return;
  while (pos < line.size()) {
    right = GetColorEnd(line, pos);
    int value = kNBags * (line[pos - 2] - '0') +
                bags.names[line.substr(pos, right - pos)];
    bags.content[index].push_back(value);
    pos = right + (line[pos - 2] == '1' ? 8 : 9);
  }
}

int CountBags(const Bags& bags, int bag) {
  int result = 1;
  for (int value : bags.content[bag]) {
    int sub_bag = value % kNBags;
    int count = value / kNBags;
    result += count * CountBags(bags, sub_bag);
  }
  return result;
}

std::string run(const std::string& input) {
  // Your code goes here
  Bags bags;
  int index = 0;
  int shiny = -1;
  std::istringstream iss(input);
  for (std::string line; std::getline(iss, line);) {
    const std::string& name = line.substr(0, GetColorEnd(line, 0));
    bags.names[name] = index;
    if (name == "shiny gold") shiny = index;
    ++index;
  }
  iss.clear();
  iss.str(input);
  for (std::string line; std::getline(iss, line);) {
    ParseLine(line, bags);
  }
  return std::to_string(CountBags(bags, shiny) - 1);
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
