#include <ctime>
#include <iostream>
#include <sstream>
#include <string>
#include <string_view>

static constexpr std::string_view kIgnore = "cid";

static constexpr int kKeysToFind = 7;

static constexpr int kMinByr = 1920;
static constexpr int kMaxByr = 2002;

static constexpr int kMinIyr = 2010;
static constexpr int kMaxIyr = 2020;

static constexpr int kMinEyr = 2020;
static constexpr int kMaxEyr = 2030;

static constexpr int kMinHgtCm = 150;
static constexpr int kMaxHgtCm = 193;

static constexpr int kMinHgtIn = 59;
static constexpr int kMaxHgtIn = 76;

bool IsInRange(const std::string& line, int left, int right, int min_value,
               int max_value) {
  int value = atoi(line.substr(left, right - left).c_str());
  return min_value <= value && value <= max_value;
}

bool IsByrValid(const std::string& line, int left, int right) {
  return IsInRange(line, left, right, kMinByr, kMaxByr);
}

bool IsIyrValid(const std::string& line, int left, int right) {
  return IsInRange(line, left, right, kMinIyr, kMaxIyr);
}

bool IsEyrValid(const std::string& line, int left, int right) {
  return IsInRange(line, left, right, kMinEyr, kMaxEyr);
}

bool IsHgtCmValid(const std::string& line, int left, int right) {
  return IsInRange(line, left, right, kMinHgtCm, kMaxHgtCm);
}

bool IsHgtInValid(const std::string& line, int left, int right) {
  return IsInRange(line, left, right, kMinHgtIn, kMaxHgtIn);
}

bool IsHgtValid(const std::string& line, int left, int right) {
  if (right - left < 2) return false;
  if (line[right - 2] == 'c' && line[right - 1] == 'm')
    return IsHgtCmValid(line, left, right - 2);
  if (line[right - 2] == 'i' && line[right - 1] == 'n')
    return IsHgtInValid(line, left, right - 2);
  return false;
}

bool IsDecimal(char c) { return '0' <= c && c <= '9'; }

bool IsHexadecimal(char c) { return IsDecimal(c) || ('a' <= c && c <= 'f'); }

bool IsHclValid(const std::string& line, int left, int right) {
  if (right - left != 7) return false;
  if (line[left] != '#') return false;
  for (int pos = left + 1; pos < right; ++pos) {
    if (!IsHexadecimal(line[pos])) return false;
  }
  return true;
}

bool IsEclValid(const std::string& line, int left, int right) {
  if (right - left != 3) return false;
  std::string ecl = line.substr(left, right - left);
  return ((ecl == "amb") || (ecl == "blu") || (ecl == "brn") ||
          (ecl == "gry") || (ecl == "grn") || (ecl == "hzl") || (ecl == "oth"));
}

bool IsPidValid(const std::string& line, int left, int right) {
  if (right - left != 9) return false;
  for (int pos = left; pos < right; ++pos) {
    if (!IsDecimal(line[pos])) return false;
  }
  return true;
}

bool IsValueValid(const std::string& line, int left, int sep, int right) {
  bool result;
  switch (line[left]) {
    case 'b': {
      if (line[left + 1] != 'y' || line[left + 2] != 'r') {
        result = false;
      } else {
        result = IsByrValid(line, sep + 1, right);
      }
      break;
    }
    case 'c': {
      if (line[left + 1] != 'i' || line[left + 2] != 'd') {
        result = false;
      } else {
        result = true;
      }
      break;
    }
    case 'e': {
      switch (line[left + 1]) {
        case 'c': {
          if (line[left + 2] != 'l') {
            result = false;
          } else {
            result = IsEclValid(line, sep + 1, right);
          }
          break;
        }
        case 'y': {
          if (line[left + 2] != 'r') {
            result = false;
          } else {
            result = IsEyrValid(line, sep + 1, right);
          }
          break;
        }
        default: {
          result = false;
          break;
        }
      }
      break;
    }
    case 'h': {
      switch (line[left + 1]) {
        case 'c': {
          if (line[left + 2] != 'l') {
            result = false;
          } else {
            result = IsHclValid(line, sep + 1, right);
          }
          break;
        }
        case 'g': {
          if (line[left + 2] != 't') {
            result = false;
          } else {
            result = IsHgtValid(line, sep + 1, right);
          }
          break;
        }
        default: {
          result = false;
          break;
        }
      }
      break;
    }
    case 'i': {
      if (line[left + 1] != 'y' || line[left + 2] != 'r') {
        result = false;
      } else {
        result = IsIyrValid(line, sep + 1, right);
      }
      break;
    }
    case 'p': {
      if (line[left + 1] != 'i' || line[left + 2] != 'd') {
        result = false;
      } else {
        result = IsPidValid(line, sep + 1, right);
      }
      break;
    }
    default: {
      result = false;
      break;
    }
  }
  return result;
}

bool ParseLine(const std::string& line, int& remaining_keys, bool& all_valid) {
  if (line.size() == 0) return true;
  for (int pos = 0; pos < line.size();) {
    int sep = line.find(':', pos);
    int right = line.find(' ', sep);
    if (right == -1) right = line.size();
    if (line.substr(pos, sep - pos) != kIgnore) {
      --remaining_keys;
      all_valid = all_valid && IsValueValid(line, pos, sep, right);
    }
    pos = right + 1;
  }
  return false;
}

std::string run(const std::string& input) {
  // Your code goes here
  std::istringstream iss(input);
  int remaining_keys = kKeysToFind;
  bool all_valid = true;
  int result = 0;
  for (std::string line; std::getline(iss, line);) {
    if (ParseLine(line, remaining_keys, all_valid)) {
      if (remaining_keys == 0 && all_valid) ++result;
      remaining_keys = kKeysToFind;
      all_valid = true;
    }
  }
  if (remaining_keys == 0 && all_valid) ++result;
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
