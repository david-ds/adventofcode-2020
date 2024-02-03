#include <cstdint>
#include <ctime>
#include <iostream>
#include <string>

std::pair<__int128_t, __int128_t> Bezout(__int128_t a, __int128_t b) {
  if (a < b) {
    auto [v, u] = Bezout(b, a);
    return (u >= 0) ? std::make_pair(u, v) : std::make_pair(u + b, v - a);
  }
  __int128_t av = a;
  __int128_t bv = b;
  __int128_t u = 1;
  __int128_t v = 0;
  __int128_t next_u = 0;
  __int128_t next_v = 1;
  while (bv > 0) {
    __int128_t d = av / bv;
    av -= d * bv;
    u -= d * next_u;
    v -= d * next_v;
    std::swap(av, bv);
    std::swap(u, next_u);
    std::swap(v, next_v);
  }
  return (u >= 0) ? std::make_pair(u, v) : std::make_pair(u + b, v - a);
}

std::string run(const std::string& input) {
  // Your code goes here
  int right = 0;
  for (; right < input.size(); ++right) {
    if (input[right] == '\n') break;
  }
  int left = right + 1;
  while (input[right] != ',') {
    ++right;
  }
  // Assume first ID is a number
  __int128_t factor = std::atoi(input.substr(left, right).c_str());
  __int128_t base_timestamp = 0;
  left = right + 1;
  __int128_t index = 1;
  for (int right = left + 1; right < input.size(); ++right) {
    if (input[right] == ',') {
      if (input[left] != 'x') {
        __int128_t bus_id = std::atoi(input.substr(left, right - left).c_str());
        auto [u, v] = Bezout(bus_id, factor);
        factor *= bus_id;
        base_timestamp = (((u % factor) * (bus_id % factor) % factor) *
                              ((base_timestamp + index) % factor) -
                          index) %
                         factor;
        if (base_timestamp < 0) base_timestamp += factor;
      }
      left = right + 1;
      ++index;
    }
  }
  if (input[left] != 'x') {
    __int128_t bus_id = std::atoi(input.substr(left, right - left).c_str());
    auto [u, v] = Bezout(bus_id, factor);
    factor *= bus_id;
    base_timestamp = (((u % factor) * (bus_id % factor) % factor) *
                          ((base_timestamp + index) % factor) -
                      index) %
                     factor;
    if (base_timestamp < 0) base_timestamp += factor;
  }
  return std::to_string((std::int64_t)base_timestamp);
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
