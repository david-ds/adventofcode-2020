#include <array>
#include <ctime>
#include <iostream>
#include <optional>
#include <ostream>
#include <stdexcept>
#include <string>
#include <string_view>
#include <unordered_map>
#include <unordered_set>
#include <utility>

static constexpr int kEdge = 10;
static constexpr int kTileEdge = 12;
static constexpr int kDrawingEdge = kTileEdge * (kEdge - 2);
static constexpr int kTileCharSize = (kEdge + 1) * (kEdge + 1) + 1;
static constexpr std::array<std::pair<int, int>, 15> kMonster = {{{0, 18},
                                                                  {1, 0},
                                                                  {1, 5},
                                                                  {1, 6},
                                                                  {1, 11},
                                                                  {1, 12},
                                                                  {1, 17},
                                                                  {1, 18},
                                                                  {1, 19},
                                                                  {2, 1},
                                                                  {2, 4},
                                                                  {2, 7},
                                                                  {2, 10},
                                                                  {2, 13},
                                                                  {2, 16}}};
static constexpr int kMonsterCols = 20;
static constexpr int kMonsterRows = 3;
static std::unordered_map<int, std::unordered_set<int>> kEdgeBitsToTiles;
static std::unordered_map<int, std::array<int, 4>> kTileToEdgeBits;
static std::array<int, kTileEdge * kTileEdge> kTilesInOrder;
static std::unordered_map<int, int> kTileIdToPos;
static std::array<std::array<bool, kDrawingEdge>, kDrawingEdge> kDrawing;

enum Edge { kUp, kRight, kDown, kLeft };

static constexpr std::array<Edge, 4> kEdges = {kUp, kRight, kDown, kLeft};

struct Orientation {
  Edge start;
  bool backward;
};

struct EdgePos {
  int start;
  int offset;
  std::string_view s;

  friend std::ostream &operator<<(std::ostream &os, const EdgePos &edge_pos) {
    for (int idx = 0; idx < kEdge; ++idx) {
      os << edge_pos.s[edge_pos.start + idx * edge_pos.offset];
    }
    return os;
  }
};

static constexpr std::array<std::array<Edge, 4>, 8> kOrientationToEdges = {{
    {kUp, kRight, kDown, kLeft},
    {kLeft, kUp, kRight, kDown},
    {kDown, kLeft, kUp, kRight},
    {kRight, kDown, kLeft, kUp},
    {kLeft, kDown, kRight, kUp},
    {kUp, kLeft, kDown, kRight},
    {kRight, kUp, kLeft, kDown},
    {kDown, kRight, kUp, kLeft},
}};

EdgePos ToEdgePos(const std::string &s, int tile_id, Edge edge,
                  Orientation orientation = {kUp, false}) {
  int pos = kTileCharSize * kTileIdToPos[tile_id];
  Edge actual_edge =
      kOrientationToEdges[orientation.start + 4 * orientation.backward][edge];
  if (orientation.backward) {
    switch (actual_edge) {
    case kUp:
      return {pos + 2 * kEdge, -1, s};
    case kRight:
      return {pos + (kEdge + 1) * (kEdge + 1) - 2, -kEdge - 1, s};
    case kDown:
      return {pos + kEdge * (kEdge + 1), 1, s};
    case kLeft:
      return {pos + kEdge + 1, kEdge + 1, s};
    }
  } else {
    switch (actual_edge) {
    case kUp:
      return {pos + kEdge + 1, 1, s};
    case kRight:
      return {pos + 2 * kEdge, kEdge + 1, s};
    case kDown:
      return {pos + (kEdge + 1) * (kEdge + 1) - 2, -1, s};
    case kLeft:
      return {pos + kEdge * (kEdge + 1), -kEdge - 1, s};
    }
  }
  throw std::invalid_argument("Failed");
}

EdgePos ToRow(const std::string &s, int tile_id, int row,
              Orientation orientation = {kUp, false}) {
  int pos = kTileCharSize * kTileIdToPos[tile_id];
  Edge actual_edge =
      kOrientationToEdges[orientation.start + 4 * orientation.backward][kUp];
  if (orientation.backward) {
    switch (actual_edge) {
    case kUp:
      return {pos + 2 * kEdge + row * (kEdge + 1), -1, s};
    case kRight:
      return {pos + (kEdge + 1) * (kEdge + 1) - 2 - row, -kEdge - 1, s};
    case kDown:
      return {pos + (kEdge - row) * (kEdge + 1), 1, s};
    case kLeft:
      return {pos + kEdge + 1 + row, kEdge + 1, s};
    }
  } else {
    switch (actual_edge) {
    case kUp:
      return {pos + (1 + row) * (kEdge + 1), 1, s};
    case kRight:
      return {pos + 2 * kEdge - row, kEdge + 1, s};
    case kDown:
      return {pos + (kEdge + 1 - row) * (kEdge + 1) - 2, -1, s};
    case kLeft:
      return {pos + kEdge * (kEdge + 1) + row, -kEdge - 1, s};
    }
  }
  throw std::invalid_argument("Failed");
}

int ToEdgeBit(std::string_view s, EdgePos edge_pos) {
  int edge_bit1 = 0;
  int edge_bit2 = 0;
  for (int idx = 0; idx < kEdge; ++idx) {
    if (s[edge_pos.start + idx * edge_pos.offset] == '#') {
      edge_bit1 += 1 << idx;
      edge_bit2 += 1 << (kEdge - 1 - idx);
    }
  }
  return std::min(edge_bit1, edge_bit2);
}

int ProcessTile(const std::string &s, int tile_num) {
  int pos = tile_num * kTileCharSize;
  int tile_id = atoi(s.substr(pos + 5, 4).c_str());
  kTilesInOrder[tile_num] = tile_id;
  kTileIdToPos[tile_id] = tile_num;
  int up_edge_bit = ToEdgeBit(s, ToEdgePos(s, tile_id, kUp));
  kEdgeBitsToTiles[up_edge_bit].insert(tile_id);
  kTileToEdgeBits[tile_id].at(0) = up_edge_bit;
  int left_edge_bit = ToEdgeBit(s, ToEdgePos(s, tile_id, kLeft));
  kEdgeBitsToTiles[left_edge_bit].insert(tile_id);
  kTileToEdgeBits[tile_id].at(3) = left_edge_bit;
  int right_edge_bit = ToEdgeBit(s, ToEdgePos(s, tile_id, kRight));
  kEdgeBitsToTiles[right_edge_bit].insert(tile_id);
  kTileToEdgeBits[tile_id].at(1) = right_edge_bit;
  int down_edge_bit = ToEdgeBit(s, ToEdgePos(s, tile_id, kDown));
  kEdgeBitsToTiles[down_edge_bit].insert(tile_id);
  kTileToEdgeBits[tile_id].at(2) = down_edge_bit;
  return tile_id;
}

Orientation FindOrientation(const std::string &s, int top_left_tile) {
  std::optional<Edge> first_edge;
  for (Edge edge : kEdges) {
    int edge_bit = ToEdgeBit(s, ToEdgePos(s, top_left_tile, edge));
    if (kEdgeBitsToTiles[edge_bit].size() >= 2) {
      first_edge = edge;
      break;
    }
  }
  if (!first_edge.has_value()) {
    throw std::invalid_argument("Could not find a first edge.");
  }
  if (first_edge == kUp) {
    int edge_bit = ToEdgeBit(s, ToEdgePos(s, top_left_tile, kLeft));
    if (kEdgeBitsToTiles[edge_bit].size() >= 2) {
      return Orientation{kDown};
    }
  }
  return Orientation{static_cast<Edge>((1 - *first_edge + 4) % 4)};
}

bool CompareEdges(const std::string &s, EdgePos edge_pos1, EdgePos edge_pos2) {
  for (int idx = 0; idx < kEdge; ++idx) {
    if (s[edge_pos1.start + idx * edge_pos1.offset] !=
        s[edge_pos2.start + (kEdge - 1 - idx) * edge_pos2.offset]) {
      return false;
    }
  }
  return true;
}

std::pair<int, Orientation> FindNext(const std::string &s, int tile_id,
                                     Orientation orientation) {
  EdgePos right_edge_pos = ToEdgePos(s, tile_id, kRight, orientation);
  int right_edge_bit = ToEdgeBit(s, right_edge_pos);
  int other_tile_id = 0;
  for (int id : kEdgeBitsToTiles[right_edge_bit]) {
    if (id == tile_id) {
      continue;
    }
    other_tile_id = id;
    break;
  }
  if (other_tile_id == 0) {
    throw std::invalid_argument("No other tile to the right.");
  }
  for (Edge edge : kEdges) {
    if (CompareEdges(s, right_edge_pos,
                     ToEdgePos(s, other_tile_id, kLeft, {edge}))) {
      return {other_tile_id, {edge}};
    }
    if (CompareEdges(s, right_edge_pos,
                     ToEdgePos(s, other_tile_id, kLeft, {edge, true}))) {
      return {other_tile_id, {edge, true}};
    }
  }
  throw std::invalid_argument("Failed to find a match between tiles.");
}

std::pair<int, Orientation> FindBelow(const std::string &s, int tile_id,
                                      Orientation orientation) {
  EdgePos down_edge_pos = ToEdgePos(s, tile_id, kDown, orientation);
  int down_edge_bit = ToEdgeBit(s, down_edge_pos);
  int other_tile_id = 0;
  for (int id : kEdgeBitsToTiles[down_edge_bit]) {
    if (id == tile_id) {
      continue;
    }
    other_tile_id = id;
    break;
  }
  if (other_tile_id == 0) {
    throw std::invalid_argument("No other tile below.");
  }
  for (Edge edge : kEdges) {
    if (CompareEdges(s, down_edge_pos,
                     ToEdgePos(s, other_tile_id, kUp, {edge}))) {
      return {other_tile_id, {edge}};
    }
    if (CompareEdges(s, down_edge_pos,
                     ToEdgePos(s, other_tile_id, kUp, {edge, true}))) {
      return {other_tile_id, {edge, true}};
    }
  }
  throw std::invalid_argument("Failed to find a match between tiles.");
}

std::pair<int, int> ToDrawingIndex(int tile_row, int tile_col, int row,
                                   int col) {
  return {tile_row * (kEdge - 2) + row, tile_col * (kEdge - 2) + col};
}

void UpdateDrawing(const std::string &s, int tile_id, Orientation orientation,
                   int tile_row, int tile_col) {
  for (int row = 0; row < kEdge - 2; ++row) {
    EdgePos edge_pos = ToRow(s, tile_id, row + 1, orientation);
    for (int col = 0; col < kEdge - 2; ++col) {
      auto [drawing_row, drawing_col] =
          ToDrawingIndex(tile_row, tile_col, row, col);
      kDrawing[drawing_row][drawing_col] =
          s[edge_pos.start + edge_pos.offset * (col + 1)] == '#';
    }
  }
}

bool RemoveMonster(int row, int col) {
  for (auto [monster_row, monster_col] : kMonster) {
    if (!kDrawing[row + monster_row][col + monster_col]) {
      return false;
    }
  }
  for (auto [monster_row, monster_col] : kMonster) {
    kDrawing[row + monster_row][col + monster_col] = false;
  }
  return true;
}

bool RemoveMonsters() {
  bool result = false;
  for (int row = 0; row <= kDrawingEdge - kMonsterRows; ++row) {
    for (int col = 0; col <= kDrawingEdge - kMonsterCols; ++col) {
      result |= RemoveMonster(row, col);
    }
  }
  return result;
}

void Rotate() {
  for (int row = 0; row < (kDrawingEdge) / 2; ++row) {
    for (int col = 0; col < (kDrawingEdge + 1) / 2; ++col) {
      std::swap(kDrawing[row][col], kDrawing[col][kDrawingEdge - row - 1]);
      std::swap(kDrawing[col][kDrawingEdge - row - 1],
                kDrawing[kDrawingEdge - row - 1][kDrawingEdge - col - 1]);
      std::swap(kDrawing[kDrawingEdge - row - 1][kDrawingEdge - col - 1],
                kDrawing[kDrawingEdge - col - 1][row]);
    }
  }
}

void Flip() {
  for (int row = 0; row < kDrawingEdge - 1; ++row) {
    for (int col = row + 1; col < kDrawingEdge; ++col) {
      std::swap(kDrawing[row][col], kDrawing[col][row]);
    }
  }
}

int Roughness() {
  int res = 0;
  for (int row = 0; row < kDrawingEdge; ++row) {
    for (int col = 0; col < kDrawingEdge; ++col) {
      if (kDrawing[row][col]) {
        ++res;
      }
    }
  }
  return res;
}

std::string run(const std::string &input) {
  // Your code goes here
  int tile_num = 0;
  while (kTileCharSize * tile_num < input.size()) {
    ProcessTile(input, tile_num);
    ++tile_num;
  }
  int top_left_tile = 0;
  for (auto &[tile_id, edge_bits] : kTileToEdgeBits) {
    int count_edges = 0;
    for (int edge_bit : edge_bits) {
      if (kEdgeBitsToTiles[edge_bit].size() >= 2) {
        ++count_edges;
      }
    }
    if (count_edges == 2) {
      top_left_tile = tile_id;
      break;
    }
  }
  Orientation left_orientation = FindOrientation(input, top_left_tile);
  int left_tile_id = 0;
  for (int tile_row = 0; tile_row < kTileEdge; ++tile_row) {
    if (left_tile_id == 0) {
      left_tile_id = top_left_tile;
    } else {
      auto res = FindBelow(input, left_tile_id, left_orientation);
      left_tile_id = res.first;
      left_orientation = res.second;
    }
    UpdateDrawing(input, left_tile_id, left_orientation, tile_row, 0);
    int tile_id = left_tile_id;
    Orientation orientation = left_orientation;
    for (int tile_col = 1; tile_col < kTileEdge; ++tile_col) {
      auto res = FindNext(input, tile_id, orientation);
      tile_id = res.first;
      orientation = res.second;
      UpdateDrawing(input, tile_id, orientation, tile_row, tile_col);
    }
  }
  if (RemoveMonsters()) {
    return std::to_string(Roughness());
  }
  Rotate();
  if (RemoveMonsters()) {
    return std::to_string(Roughness());
  }
  Rotate();
  if (RemoveMonsters()) {
    return std::to_string(Roughness());
  }
  Rotate();
  if (RemoveMonsters()) {
    return std::to_string(Roughness());
  }
  Flip();
  if (RemoveMonsters()) {
    return std::to_string(Roughness());
  }
  Rotate();
  if (RemoveMonsters()) {
    return std::to_string(Roughness());
  }
  Rotate();
  if (RemoveMonsters()) {
    return std::to_string(Roughness());
  }
  Rotate();
  if (RemoveMonsters()) {
    return std::to_string(Roughness());
  }
  throw std::invalid_argument("No monster found");
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
