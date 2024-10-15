#include <array>
#include <ctime>
#include <iostream>
#include <sstream>
#include <string>
#include <unordered_set>
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

std::unordered_set<int> Check(const std::string &s, int pos = 0,
                              int index = 0) {
  if (auto *v = std::get_if<char>(&kRules[index])) {
    if (s[pos] == *v) {
      return {pos + 1};
    }
    return {};
  }
  auto *v = std::get_if<std::vector<std::vector<int>>>(&kRules[index]);
  std::unordered_set<int> result;
  for (const auto &rule_indexes : *v) {
    std::unordered_set<int> next_poss = {pos};
    for (const auto &rule_index : rule_indexes) {
      std::unordered_set<int> next_next_poss = {};
      for (int next_pos : next_poss) {
        for (int next_next_pos : Check(s, next_pos, rule_index)) {
          if (next_next_pos <= s.size()) {
            next_next_poss.insert(next_next_pos);
          }
        }
      }
      std::swap(next_next_poss, next_poss);
    }
    for (auto v : next_poss) {
      result.insert(v);
    }
  }
  return result;
}

std::string run(const std::string &input) {
  // Your code goes here
  std::istringstream iss(input);
  for (std::string line; std::getline(iss, line);) {
    if (line == "") {
      break;
    }
    if (line == "8: 42") {
      line = "8: 42 | 42 8";
    }
    if (line == "11: 42 31") {
      line = "11: 42 31 | 42 11 31";
    }
    ParseRule(line);
  }
  int result = 0;
  for (std::string line; std::getline(iss, line);) {
    if (std::unordered_set<int> v = Check(line);
        v.find(line.size()) != v.end()) {
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
