#include <ctime>
#include <iostream>
#include <string>
#include <vector>

static int kLineSize;

int FindSeat(const std::string& input, int index, int direction) {
  index += direction;
  while (0 <= index && index < input.size() && input[index] != '\n') {
    if (input[index] == '.') {
      index += direction;
      continue;
    }
    return index;
  }
  return -1;
}

bool HasNoAdjacent(const std::string& input, int index) {
  if (int seat = FindSeat(input, index, -kLineSize - 2);
      seat != -1 && input[seat] == '#')
    return false;
  if (int seat = FindSeat(input, index, -kLineSize - 1);
      seat != -1 && input[seat] == '#')
    return false;
  if (int seat = FindSeat(input, index, -kLineSize);
      seat != -1 && input[seat] == '#')
    return false;
  if (int seat = FindSeat(input, index, -1); seat != -1 && input[seat] == '#')
    return false;
  if (int seat = FindSeat(input, index, 1); seat != -1 && input[seat] == '#')
    return false;
  if (int seat = FindSeat(input, index, kLineSize);
      seat != -1 && input[seat] == '#')
    return false;
  if (int seat = FindSeat(input, index, kLineSize + 1);
      seat != -1 && input[seat] == '#')
    return false;

  if (int seat = FindSeat(input, index, kLineSize + 2);
      seat != -1 && input[seat] == '#')
    return false;
  return true;
}

int Has5PlusAdjacent(const std::string& input, int index) {
  int count_adjacent = 0;
  if (int seat = FindSeat(input, index, -kLineSize - 2);
      seat != -1 && input[seat] == '#')
    ++count_adjacent;
  if (int seat = FindSeat(input, index, -kLineSize - 1);
      seat != -1 && input[seat] == '#')
    ++count_adjacent;
  if (int seat = FindSeat(input, index, -kLineSize);
      seat != -1 && input[seat] == '#')
    ++count_adjacent;
  if (int seat = FindSeat(input, index, -1); seat != -1 && input[seat] == '#')
    ++count_adjacent;
  if (int seat = FindSeat(input, index, 1); seat != -1 && input[seat] == '#')
    ++count_adjacent;
  if (count_adjacent >= 5) return true;
  if (int seat = FindSeat(input, index, kLineSize);
      seat != -1 && input[seat] == '#')
    ++count_adjacent;
  if (count_adjacent >= 5) return true;
  if (int seat = FindSeat(input, index, kLineSize + 1);
      seat != -1 && input[seat] == '#')
    ++count_adjacent;
  if (count_adjacent >= 5) return true;
  if (int seat = FindSeat(input, index, kLineSize + 2);
      seat != -1 && input[seat] == '#')
    ++count_adjacent;
  return count_adjacent >= 5;
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
        if (Has5PlusAdjacent(input, seat)) {
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
