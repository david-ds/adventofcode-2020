#include <cstdint>
#include <ctime>
#include <iostream>
#include <sstream>
#include <string>

std::int64_t CountTrees(const std::string& input, int row_size, int col_slope,
                        int row_slope) {
  int count = 0;
  int col = col_slope;
  for (int row_index = row_slope; row_index * (row_size + 1) < input.size();
       row_index += row_slope) {
    count += input[row_index * (row_size + 1) + col] == '#';
    col = (col + col_slope) % row_size;
  }
  return count;
}

std::string run(const std::string& input) {
  // Your code goes here
  std::istringstream iss(input);
  int row_size = input.find('\n');
  return std::to_string(
      CountTrees(input, row_size, 1, 1) * CountTrees(input, row_size, 3, 1) *
      CountTrees(input, row_size, 5, 1) * CountTrees(input, row_size, 7, 1) *
      CountTrees(input, row_size, 1, 2));
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
