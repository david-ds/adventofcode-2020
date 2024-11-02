#include <ctime>
#include <iostream>
#include <ostream>
#include <string>
#include <unordered_map>
#include <unordered_set>

static constexpr int kCycles = 100;
static constexpr int kSize = 9;
static constexpr int kExtract = 3;

struct Node {
  int data;
  Node *next;
};

static std::unordered_map<int, Node> kMap;

Node *Extract(Node *head, int n) {
  Node *list = head->next;
  Node *tail = list;
  for (int idx = 1; idx < n; ++idx) {
    tail = tail->next;
  }
  head->next = tail->next;
  tail->next = nullptr;
  return list;
}

void Insert(Node *head, Node *list) {
  Node *next = head->next;
  head->next = list;
  Node *tail = list;
  while (tail->next != nullptr) {
    tail = tail->next;
  }
  tail->next = next;
}

int ToInt(char c) { return c - '0'; }

int Decrement(int current, const std::unordered_set<int> &extracted) {
  int destination = current - 1;
  if (destination <= 0) {
    destination += kSize;
  }
  while (extracted.find(destination) != extracted.end()) {
    --destination;
    if (destination <= 0) {
      destination += kSize;
    }
  }
  return destination;
}

std::string run(const std::string &input) {
  // Your code goes here
  int value = ToInt(input[0]);
  kMap[value] = {value, nullptr};
  Node *head = &kMap[value];
  Node *node = head;
  for (int idx = 1; idx < input.size(); ++idx) {
    value = ToInt(input[idx]);
    kMap[value] = {value, nullptr};
    node->next = &kMap[value];
    node = node->next;
  }
  node->next = head;
  std::unordered_set<int> extracted;
  for (int cycle = 0; cycle < kCycles; ++cycle) {
    Node *list = Extract(head, kExtract);
    extracted.clear();
    Node *node = list;
    for (int idx = 0; idx < kExtract; ++idx) {
      extracted.insert(node->data);
      node = node->next;
    }
    int destination = Decrement(head->data, extracted);
    Insert(&kMap[destination], list);
    head = head->next;
  }
  std::string res;
  head = &kMap[1];
  while (head->next != &kMap[1]) {
    head = head->next;
    res.push_back(head->data + '0');
  }
  return res;
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
