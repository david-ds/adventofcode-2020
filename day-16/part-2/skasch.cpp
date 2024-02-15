#include <algorithm>
#include <array>
#include <bitset>
#include <cstdint>
#include <ctime>
#include <iostream>
#include <sstream>
#include <stdexcept>
#include <string>
#include <vector>

static constexpr int kNFields = 20;
static const std::bitset<kNFields> kDepartureFields{"00000000000000111111"};
static constexpr std::array<int, kNFields> kInputOffsets = {
    20, 19, 20, 17, 16, 16, 18, 17, 18, 15, 7, 10, 7, 7, 5, 6, 7, 6, 7, 6};

using IndexedBitset = std::pair<int, std::bitset<kNFields>>;

static std::array<IndexedBitset, kNFields> kValidFields;

struct Range {
  int left;
  int right;

  bool Contains(int value) const { return left <= value && value <= right; }
};

struct FieldCondition {
  Range low;
  Range high;

  bool IsValid(int value) const {
    return low.Contains(value) || high.Contains(value);
  }
};

FieldCondition ParseFieldCondition(const std::string& line, int row) {
  const int& offset = kInputOffsets.at(row);
  int dash1 = line.find('-', offset);
  int orPos = line.find('o', dash1);
  int dash2 = line.find('-', orPos + 3);
  return FieldCondition{
      Range{std::atoi(line.substr(offset, dash1 - offset).c_str()),
            std::atoi(line.substr(dash1 + 1, orPos - dash1 - 2).c_str())},
      Range{std::atoi(line.substr(orPos + 3, dash2 - orPos - 3).c_str()),
            std::atoi(line.substr(dash2 + 1).c_str())}};
}

using Ticket = std::array<int, kNFields>;

Ticket ParseTicket(const std::string& line) {
  Ticket ticket;
  int left = 0;
  int index = 0;
  for (int right = 1; right < line.size(); ++right) {
    if (line.at(right) != ',') continue;
    ticket.at(index) = std::atoi(line.substr(left, right - left).c_str());
    ++index;
    ++right;
    left = right;
  }
  ticket.at(index) = std::atoi(line.substr(left).c_str());
  return ticket;
}

bool IsValueValid(int value,
                  const std::vector<FieldCondition>& fieldConditions) {
  for (const FieldCondition& fieldCondition : fieldConditions) {
    if (fieldCondition.IsValid(value)) return true;
  }
  return false;
}

bool IsTicketValid(const Ticket& ticket,
                   const std::vector<FieldCondition>& fieldConditions) {
  for (int value : ticket) {
    if (!IsValueValid(value, fieldConditions)) return false;
  }
  return true;
}

void InitializeValidFields() {
  int fieldIndex = 0;
  for (auto& [index, validFields] : kValidFields) {
    for (int idx = 0; idx < kNFields; ++idx) {
      validFields.set(idx);
    }
    index = fieldIndex;
    ++fieldIndex;
  }
}

void UpdateValidFields(const Ticket& ticket,
                       const std::vector<FieldCondition>& fieldConditions) {
  for (int ticketIndex = 0; ticketIndex < kNFields; ++ticketIndex) {
    int value = ticket.at(ticketIndex);
    for (int fieldIndex = 0; fieldIndex < kNFields; ++fieldIndex) {
      const FieldCondition& fieldCondition = fieldConditions.at(fieldIndex);
      if (!fieldCondition.IsValid(value))
        kValidFields.at(ticketIndex).second.reset(fieldIndex);
    }
  }
}

bool Compare(const IndexedBitset& lhs, const IndexedBitset& rhs) {
  return lhs.second.count() < rhs.second.count();
}

std::string run(const std::string& input) {
  // Your code goes here
  std::istringstream iss(input);
  std::vector<FieldCondition> fieldConditions;
  fieldConditions.reserve(kNFields);
  std::string line;
  for (int row = 0; row < kNFields; ++row) {
    std::getline(iss, line);
    fieldConditions.push_back(ParseFieldCondition(line, row));
  }
  for (; std::getline(iss, line);) {
    if (line.starts_with('y')) break;
  }
  std::getline(iss, line);
  Ticket myTicket = ParseTicket(line);
  for (; std::getline(iss, line);) {
    if (line.starts_with('n')) break;
  }
  InitializeValidFields();
  for (; std::getline(iss, line);) {
    Ticket ticket = ParseTicket(line);
    if (!IsTicketValid(ticket, fieldConditions)) continue;
    UpdateValidFields(ticket, fieldConditions);
  }
  std::sort(kValidFields.begin(), kValidFields.end(), Compare);
  std::int64_t result = 1;
  for (int fieldIdx = 0; fieldIdx < kNFields; ++fieldIdx) {
    const std::bitset<kNFields>& bitset = kValidFields.at(fieldIdx).second;
    if (bitset.count() != 1)
      throw std::invalid_argument("Could not find valid sequence.");
    for (int nextIdx = fieldIdx + 1; nextIdx < kNFields; ++nextIdx) {
      kValidFields.at(nextIdx).second &= ~bitset;
    }
    if ((bitset & kDepartureFields).any()) {
      result *= myTicket.at(kValidFields.at(fieldIdx).first);
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
