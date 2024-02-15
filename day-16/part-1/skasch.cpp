#include <array>
#include <ctime>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>

static constexpr int kNFields = 20;
static constexpr std::array<int, kNFields> kInputOffsets = {
    20, 19, 20, 17, 16, 16, 18, 17, 18, 15, 7, 10, 7, 7, 5, 6, 7, 6, 7, 6};

struct Range {
  int left;
  int right;

  bool Contains(int value) const { return left <= value && value <= right; }
};

struct FieldCondition {
  Range low;
  Range high;

  bool IsValid(int value) const {
    return low.Contains(value) || high.Contains(value);
  }
};

FieldCondition ParseFieldCondition(const std::string& line, int row) {
  const int& offset = kInputOffsets.at(row);
  int dash1 = line.find('-', offset);
  int orPos = line.find('o', dash1);
  int dash2 = line.find('-', orPos + 3);
  return FieldCondition{
      Range{std::atoi(line.substr(offset, dash1 - offset).c_str()),
            std::atoi(line.substr(dash1 + 1, orPos - dash1 - 2).c_str())},
      Range{std::atoi(line.substr(orPos + 3, dash2 - orPos - 3).c_str()),
            std::atoi(line.substr(dash2 + 1).c_str())}};
}

bool IsValueValid(int value,
                  const std::vector<FieldCondition>& fieldConditions) {
  for (const FieldCondition& fieldCondition : fieldConditions) {
    if (fieldCondition.IsValid(value)) return true;
  }
  return false;
}

int FindInvalidValues(const std::string& line,
                      const std::vector<FieldCondition>& fieldConditions) {
  int invalidValues = 0;
  int left = 0;
  for (int right = 1; right < line.size(); ++right) {
    if (line.at(right) != ',') continue;
    int value = std::atoi(line.substr(left, right - left).c_str());
    if (!IsValueValid(value, fieldConditions)) invalidValues += value;
    ++right;
    left = right;
  }
  int value = std::atoi(line.substr(left).c_str());
  if (!IsValueValid(value, fieldConditions)) invalidValues += value;
  return invalidValues;
}

std::string run(const std::string& input) {
  // Your code goes here
  std::istringstream iss(input);
  std::vector<FieldCondition> fieldConditions;
  fieldConditions.reserve(kNFields);
  std::string line;
  for (int row = 0; row < kNFields; ++row) {
    std::getline(iss, line);
    fieldConditions.push_back(ParseFieldCondition(line, row));
  }
  for (; std::getline(iss, line);) {
    if (line.starts_with('n')) break;
  }
  int errorRate = 0;
  for (; std::getline(iss, line);) {
    errorRate += FindInvalidValues(line, fieldConditions);
  }
  return std::to_string(errorRate);
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
