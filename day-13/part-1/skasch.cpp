#include <ctime>
#include <iostream>
#include <limits>
#include <string>

int GetTimeToWait(int bus_id, int timestamp) {
  return bus_id - (timestamp % bus_id);
}

std::string run(const std::string& input) {
  // Your code goes here
  int right = 0;
  for (; right < input.size(); ++right) {
    if (input[right] == '\n') break;
  }
  int timestamp = std::atoi(input.substr(0, right).c_str());
  int left = right + 1;
  int best_time_to_wait = std::numeric_limits<int>::max();
  int result = 0;
  for (int right = left + 1; right < input.size(); ++right) {
    if (input[right] == ',') {
      if (input[left] != 'x') {
        int bus_id = std::atoi(input.substr(left, right - left).c_str());
        int time_to_wait = GetTimeToWait(bus_id, timestamp);
        if (time_to_wait < best_time_to_wait) {
          best_time_to_wait = time_to_wait;
          result = time_to_wait * bus_id;
        }
      }
      left = right + 1;
    }
  }
  if (input[left] != 'x') {
    int bus_id = std::atoi(input.substr(left, input.size() - left).c_str());
    int time_to_wait = GetTimeToWait(bus_id, timestamp);
    if (time_to_wait < best_time_to_wait) {
      best_time_to_wait = time_to_wait;
      result = time_to_wait * bus_id;
    }
  }
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
