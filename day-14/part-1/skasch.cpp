#include <cstdint>
#include <ctime>
#include <iostream>
#include <sstream>
#include <string>
#include <unordered_map>
#include <utility>
#include <vector>

struct Mask {
  std::vector<int> indexes;
  std::vector<bool> bits;
};

void UpdateMask(Mask& mask, const std::string& line) {
  mask.indexes.clear();
  mask.bits.clear();
  for (int pos = 7; pos < line.size(); ++pos) {
    if (line[pos] == 'X') continue;
    mask.indexes.push_back(42 - pos);
    mask.bits.push_back(line[pos] == '1');
  }
}

std::pair<int, std::int64_t> ParseMem(const std::string& line) {
  int left = 4;
  int right = left + 1;
  while (line[right] != ']') ++right;
  int address = std::atoi(line.substr(left, right - left).c_str());
  left = right + 4;
  std::int64_t value = std::atoll(line.substr(left).c_str());
  return std::make_pair(address, value);
}

void ApplyMask(std::int64_t& value, const Mask& mask) {
  for (int idx = 0; idx < mask.indexes.size(); ++idx) {
    if (mask.bits[idx]) {
      value |= (std::int64_t)1 << mask.indexes[idx];
    } else {
      value &=
          (~((std::int64_t)1 << mask.indexes[idx])) % ((std::int64_t)1 << 36);
    }
  }
}

using Mem = std::unordered_map<int, std::int64_t>;

void UpdateMem(Mem& mem, const Mask& mask, const std::string& line) {
  auto [address, value] = ParseMem(line);
  mem[address] = value;
  ApplyMask(mem[address], mask);
}

void ProcessLine(Mem& mem, Mask& mask, const std::string& line) {
  if (line[1] == 'a') {
    UpdateMask(mask, line);
  } else {
    UpdateMem(mem, mask, line);
  }
}

std::string run(const std::string& input) {
  // Your code goes here
  Mem mem;
  Mask mask;
  std::istringstream iss(input);
  for (std::string line; std::getline(iss, line);) {
    ProcessLine(mem, mask, line);
  }
  std::int64_t result = 0;
  for (auto [_, v] : mem) {
    result += v;
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
