#include <cstdint>
#include <ctime>
#include <iostream>
#include <sstream>
#include <string>
#include <unordered_map>
#include <utility>
#include <vector>

struct Mask {
  std::vector<int> floating;
  std::vector<int> ones;
};

void UpdateMask(Mask& mask, const std::string& line) {
  mask.floating.clear();
  mask.ones.clear();
  for (int pos = 7; pos < line.size(); ++pos) {
    switch (line[pos]) {
      case 'X': {
        mask.floating.push_back(42 - pos);
        break;
      }
      case '1': {
        mask.ones.push_back(42 - pos);
        break;
      }
      default: {
        break;
      }
    }
  }
}

std::pair<std::int64_t, std::int64_t> ParseMem(const std::string& line) {
  int left = 4;
  int right = left + 1;
  while (line[right] != ']') ++right;
  std::int64_t address = std::atoll(line.substr(left, right - left).c_str());
  left = right + 4;
  std::int64_t value = std::atoll(line.substr(left).c_str());
  return std::make_pair(address, value);
}

using Mem = std::unordered_map<std::int64_t, std::int64_t>;

void ApplyMask(Mem& mem, std::int64_t address, std::int64_t value,
               const Mask& mask) {
  for (int one : mask.ones) {
    address |= (std::int64_t)1 << one;
  }
  std::vector<std::int64_t> addresses = {address};
  mem[address] = value;
  addresses.reserve(1 << mask.floating.size());
  for (int floating : mask.floating) {
    int size = addresses.size();
    for (int idx = 0; idx < size; ++idx) {
      addresses.push_back(addresses[idx] ^ ((std::int64_t)1 << floating));
      mem[addresses.back()] = value;
    }
  }
}

void UpdateMem(Mem& mem, const Mask& mask, const std::string& line) {
  auto [address, value] = ParseMem(line);
  ApplyMask(mem, address, value, mask);
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
