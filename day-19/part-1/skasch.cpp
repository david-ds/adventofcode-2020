#include <array>
#include <ctime>
#include <iostream>
#include <optional>
#include <sstream>
#include <string>
#include <variant>
#include <vector>

using Rule = std::variant<char, std::vector<std::vector<int>>>;

std::array<Rule, 200> kRules;

void ParseRule(const std::string &line) {
  int pos = 0;
  int index = 0;
  while (line[pos] != ':') {
    index = 10 * index + line[pos] - '0';
    ++pos;
  }
  ++pos;
  ++pos;
  if (line[pos] == '"') {
    kRules[index] = line[pos + 1];
    return;
  }
  int left = pos;
  std::vector<std::vector<int>> rule = {{}};
  while (pos < line.size()) {
    left = pos;
    if (line[pos] == '|') {
      rule.push_back({});
      ++pos;
      ++pos;
      continue;
    }
    while (!(line[pos] == ' ' || pos >= line.size())) {
      ++pos;
    }
    int value = atoi(line.substr(left, pos - left).c_str());
    rule.back().push_back(value);
    ++pos;
  }
  kRules[index] = rule;
}

std::optional<int> Check(const std::string &s, int pos = 0, int index = 0) {
  if (auto *v = std::get_if<char>(&kRules[index])) {
    if (s[pos] == *v) {
      return pos + 1;
    }
    return std::nullopt;
  }
  auto *v = std::get_if<std::vector<std::vector<int>>>(&kRules[index]);
  for (const auto &rule_indexes : *v) {
    std::optional<int> next_pos = pos;
    for (const auto &rule_index : rule_indexes) {
      next_pos = Check(s, *next_pos, rule_index);
      if (!next_pos.has_value()) {
        break;
      }
    }
    if (next_pos.has_value()) {
      return next_pos;
    }
  }
  return std::nullopt;
}

std::string run(const std::string &input) {
  // Your code goes here
  std::istringstream iss(input);
  for (std::string line; std::getline(iss, line);) {
    if (line == "") {
      break;
    }
    ParseRule(line);
  }
  int result = 0;
  for (std::string line; std::getline(iss, line);) {
    if (std::optional<int> v = Check(line);
        v.has_value() && *v == line.size()) {
      ++result;
    }
  }
  return std::to_string(result);
}

int main(int argc, char **argv) {
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
