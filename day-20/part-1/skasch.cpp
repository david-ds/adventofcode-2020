#include <array>
#include <cstdint>
#include <ctime>
#include <iostream>
#include <string>
#include <string_view>
#include <unordered_map>
#include <unordered_set>

static constexpr int kEdge = 10;
static constexpr int kTileCharSize = (kEdge + 1) * (kEdge + 1) + 1;
static std::unordered_map<int, std::unordered_set<int>> kEdgeBitsToTiles;
static std::unordered_map<int, std::array<int, 4>> kTileToEdgeBits;

int ToIndex(std::string_view s, int start, int offset) {
  int index1 = 0;
  int index2 = 0;
  for (int idx = 0; idx < kEdge; ++idx) {
    if (s[start + idx * offset] == '#') {
      index1 += 1 << idx;
      index2 += 1 << (kEdge - 1 - idx);
    }
  }
  return std::min(index1, index2);
}

int ProcessTile(const std::string &s, int offset) {
  int tile_id = atoi(s.substr(offset + 5, 4).c_str());
  int up_index = ToIndex(s, offset + kEdge + 1, 1);
  kEdgeBitsToTiles[up_index].insert(tile_id);
  kTileToEdgeBits[tile_id].at(0) = up_index;
  int left_index = ToIndex(s, offset + kEdge + 1, kEdge + 1);
  kEdgeBitsToTiles[left_index].insert(tile_id);
  kTileToEdgeBits[tile_id].at(1) = left_index;
  int right_index = ToIndex(s, offset + 2 * kEdge, kEdge + 1);
  kEdgeBitsToTiles[right_index].insert(tile_id);
  kTileToEdgeBits[tile_id].at(2) = right_index;
  int down_index = ToIndex(s, offset + kEdge * (kEdge + 1), 1);
  kEdgeBitsToTiles[down_index].insert(tile_id);
  kTileToEdgeBits[tile_id].at(3) = down_index;
  return tile_id;
}

std::string run(const std::string &input) {
  // Your code goes here
  int pos = 0;
  while (pos < input.size()) {
    ProcessTile(input, pos);
    pos += kTileCharSize;
  }
  int64_t result = 1;
  for (auto &[edge_bits, tiles] : kEdgeBitsToTiles) {
    std::cerr << "kEdgeBitsToTiles[" << edge_bits << "]: ";
    for (int tile : tiles) {
      std::cerr << tile << ",";
    }
    std::cerr << "\n";
  }
  for (auto &[tile_id, edge_bits] : kTileToEdgeBits) {
    std::cerr << "kTileToEdgeBits[" << tile_id << "]: ";
    for (int edge_bit : edge_bits) {
      std::cerr << edge_bit << ",";
    }
    std::cerr << "\n";
  }
  for (auto &[tile_id, edge_bits] : kTileToEdgeBits) {
    int count_edges = 0;
    for (int edge_bit : edge_bits) {
      if (kEdgeBitsToTiles[edge_bit].size() >= 2) {
        ++count_edges;
      }
    }
    if (count_edges == 2) {
      std::cerr << "Found " << count_edges << " edges for: " << tile_id << "\n";
      result *= tile_id;
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
