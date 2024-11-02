#include <ctime>
#include <deque>
#include <iostream>
#include <iterator>
#include <sstream>
#include <string>
#include <unordered_set>

std::string ToString(const std::deque<int> &player1,
                     const std::deque<int> &player2) {
  std::string s;
  for (int card1 : player1) {
    s.push_back(card1);
  }
  s.push_back('_');
  for (int card2 : player2) {
    s.push_back(card2);
  }
  return s;
}

std::deque<int> *Play(std::deque<int> &player1, std::deque<int> &player2,
                      std::unordered_set<std::string> &visited);

std::deque<int> *Game(std::deque<int> &player1, std::deque<int> &player2) {
  std::unordered_set<std::string> visited;
  std::deque<int> *winner = nullptr;
  while (winner == nullptr) {
    winner = Play(player1, player2, visited);
  }
  return winner;
}

std::deque<int> *Play(std::deque<int> &player1, std::deque<int> &player2,
                      std::unordered_set<std::string> &visited) {
  std::string s = ToString(player1, player2);
  if (auto it = visited.find(s); it != visited.end()) {
    return &player1;
  }
  visited.insert(s);
  int card1 = player1.front();
  player1.pop_front();
  int card2 = player2.front();
  player2.pop_front();
  bool player1_wins = card1 > card2;
  if (card1 <= player1.size() && card2 <= player2.size()) {
    std::deque<int> sub_player1;
    auto sub_card1 = player1.begin();
    for (int idx = 0; idx < card1; ++idx) {
      sub_player1.push_back(*sub_card1);
      std::advance(sub_card1, 1);
    }
    std::deque<int> sub_player2;
    auto sub_card2 = player2.begin();
    for (int idx = 0; idx < card2; ++idx) {
      sub_player2.push_back(*sub_card2);
      std::advance(sub_card2, 1);
    }
    std::deque<int> *winner = Game(sub_player1, sub_player2);
    player1_wins = winner == &sub_player1;
  }
  if (player1_wins) {
    player1.push_back(card1);
    player1.push_back(card2);
    return player2.empty() ? &player1 : nullptr;
  } else {
    player2.push_back(card2);
    player2.push_back(card1);
    return player1.empty() ? &player2 : nullptr;
  }
}

std::string run(const std::string &input) {
  // Your code goes here
  std::istringstream iss(input);
  std::string line;
  std::getline(iss, line);
  std::deque<int> player1;
  std::deque<int> player2;
  for (; std::getline(iss, line);) {
    if (line.empty()) {
      break;
    }
    player1.push_back(atoi(line.c_str()));
  }
  std::getline(iss, line);
  for (; std::getline(iss, line);) {
    player2.push_back(atoi(line.c_str()));
  }
  std::deque<int> *winner = Game(player1, player2);
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
