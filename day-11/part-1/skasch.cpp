#include <ctime>
#include <iostream>
#include <string>
#include <vector>

static int kLineSize;

bool HasNoAdjacent(const std::string& input, int idx) {
  if (idx - kLineSize - 2 >= 0 && input[idx - kLineSize - 2] == '#')
    return false;
  if (idx - kLineSize - 1 >= 0 && input[idx - kLineSize - 1] == '#')
    return false;
  if (idx - kLineSize >= 0 && input[idx - kLineSize] == '#') return false;
  if (idx - 1 >= 0 && input[idx - 1] == '#') return false;
  if (idx + 1 < input.size() && input[idx + 1] == '#') return false;
  if (idx + kLineSize < input.size() && input[idx + kLineSize] == '#')
    return false;
  if (idx + kLineSize + 1 < input.size() && input[idx + kLineSize + 1] == '#')
    return false;
  if (idx + kLineSize + 2 < input.size() && input[idx + kLineSize + 2] == '#')
    return false;
  return true;
}

bool Has4PlusAdjacent(const std::string& input, int idx) {
  int count_adjacent = 0;
  if (idx - kLineSize - 2 >= 0 && input[idx - kLineSize - 2] == '#')
    ++count_adjacent;
  if (idx - kLineSize - 1 >= 0 && input[idx - kLineSize - 1] == '#')
    ++count_adjacent;
  if (idx - kLineSize >= 0 && input[idx - kLineSize] == '#') ++count_adjacent;
  if (idx - 1 >= 0 && input[idx - 1] == '#') ++count_adjacent;
  if (count_adjacent >= 4) return true;
  if (idx + 1 < input.size() && input[idx + 1] == '#') ++count_adjacent;
  if (count_adjacent >= 4) return true;
  if (idx + kLineSize < input.size() && input[idx + kLineSize] == '#')
    ++count_adjacent;
  if (count_adjacent >= 4) return true;
  if (idx + kLineSize + 1 < input.size() && input[idx + kLineSize + 1] == '#')
    ++count_adjacent;
  if (count_adjacent >= 4) return true;
  if (idx + kLineSize + 2 < input.size() && input[idx + kLineSize + 2] == '#')
    ++count_adjacent;
  return count_adjacent >= 4;
}

std::string run(std::string input) {
  // Your code goes here
  std::vector<int> seats;
  for (int idx = 0; idx < input.size(); ++idx) {
    if (input[idx] == 'L') {
      seats.push_back(idx);
    } else if (kLineSize == 0 && input[idx] == '\n') {
      kLineSize = idx;
    }
  }
  std::string next_input = input;
  while (true) {
    bool is_updated = false;
    int occupied = 0;
    for (int seat : seats) {
      if (input[seat] == 'L') {
        if (HasNoAdjacent(input, seat)) {
          next_input[seat] = '#';
          is_updated = true;
        } else {
          next_input[seat] = 'L';
        }
      } else {
        ++occupied;
        if (Has4PlusAdjacent(input, seat)) {
          next_input[seat] = 'L';
          is_updated = true;
        } else {
          next_input[seat] = '#';
        }
      }
    }
    if (!is_updated) return std::to_string(occupied);
    std::swap(input, next_input);
  }
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
