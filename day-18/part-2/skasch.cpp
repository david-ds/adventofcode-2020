#include <cstdint>
#include <ctime>
#include <iostream>
#include <iterator>
#include <list>
#include <ostream>
#include <string>
#include <variant>

struct Expression {
  std::list<std::variant<Expression, int64_t>> expressions;
  std::list<char> operations;
  Expression *parent;

  int64_t value() {
    for (int i = 0; i < expressions.size(); ++i) {
      auto it = expressions.begin();
      std::advance(it, i);
      if (auto *v = std::get_if<Expression>(&*it)) {
        expressions.insert(it, v->value());
        expressions.erase(it);
      }
    }
    int i = 0;
    while (i < operations.size()) {
      auto op = operations.begin();
      std::advance(op, i);
      if (*op == '*') {
        ++i;
        continue;
      }
      auto lhs = expressions.begin();
      std::advance(lhs, i);
      auto rhs = expressions.begin();
      std::advance(rhs, i + 1);
      expressions.insert(lhs,
                         std::get<int64_t>(*lhs) + std::get<int64_t>(*rhs));
      expressions.erase(lhs);
      expressions.erase(rhs);
      operations.erase(op);
    }
    i = 0;
    while (i < operations.size()) {
      auto op = operations.begin();
      std::advance(op, i);
      auto lhs = expressions.begin();
      std::advance(lhs, i);
      auto rhs = expressions.begin();
      std::advance(rhs, i + 1);
      expressions.insert(lhs,
                         std::get<int64_t>(*lhs) * std::get<int64_t>(*rhs));
      expressions.erase(lhs);
      expressions.erase(rhs);
      operations.erase(op);
    }
    return std::get<int64_t>(*expressions.begin());
  }
};

Expression *Parse(char t, Expression *expression) {
  switch (t) {
  case ' ':
    break;
  case '+':
  case '*': {
    expression->operations.push_back(t);
    return expression;
  }
  case '(': {
    expression->expressions.push_back(
        Expression{.expressions = {}, .operations = {}, .parent = expression});
    return std::get_if<Expression>(&expression->expressions.back());
  }
  case ')': {
    return expression->parent;
  }
  default: {
    int64_t v = std::atoi(&t);
    expression->expressions.push_back(v);
    return expression;
  }
  }
  return expression;
}

std::string run(const std::string &input) {
  Expression expression = {
      .expressions = {}, .operations = {}, .parent = nullptr};
  Expression *p = &expression;
  int64_t result = 0;
  for (char c : input) {
    if (c == '\n') {
      int64_t v = expression.value();
      result += v;
      expression.expressions.clear();
      expression.operations.clear();
      p = &expression;
      continue;
    }
    p = Parse(c, p);
  }
  int64_t v = expression.value();
  result += v;
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
