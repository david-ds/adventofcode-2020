#include <ctime>
#include <deque>
#include <iostream>
#include <sstream>
#include <string>

static std::deque<int> kPlayer1;
static std::deque<int> kPlayer2;

std::deque<int> *Play() {
  int card1 = kPlayer1.front();
  kPlayer1.pop_front();
  int card2 = kPlayer2.front();
  kPlayer2.pop_front();
  if (card1 > card2) {
    kPlayer1.push_back(card1);
    kPlayer1.push_back(card2);
    return kPlayer2.empty() ? &kPlayer1 : nullptr;
  } else {
    kPlayer2.push_back(card2);
    kPlayer2.push_back(card1);
    return kPlayer1.empty() ? &kPlayer2 : nullptr;
  }
}

std::string run(const std::string &input) {
  // Your code goes here
  std::istringstream iss(input);
  std::string line;
  std::getline(iss, line);
  for (; std::getline(iss, line);) {
    if (line.empty()) {
      break;
    }
    kPlayer1.push_back(atoi(line.c_str()));
  }
  std::getline(iss, line);
  for (; std::getline(iss, line);) {
    kPlayer2.push_back(atoi(line.c_str()));
  }
  std::deque<int> *winner = nullptr;
  while (winner == nullptr) {
    winner = Play();
  }
  int result = 0;
  for (int index = 0; index < winner->size(); ++index) {
    result += (winner->size() - index) * winner->at(index);
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
