#include <cstdint>
#include <ctime>
#include <iostream>
#include <sstream>
#include <string>

static constexpr int64_t kBase = 20201227;
static constexpr int64_t kSubjectNumber = 7;

void Iterate(int64_t &value, int64_t subject_number = kSubjectNumber) {
  value = value * subject_number % kBase;
}

int64_t GetEncryptionKey(int64_t card_public, int64_t door_public) {
  int64_t value = kSubjectNumber;
  int loops = 0;
  while (value != card_public && value != door_public) {
    Iterate(value);
    ++loops;
  }
  int64_t subject_number;
  if (value == card_public) {
    subject_number = door_public;
  } else {
    subject_number = card_public;
  }
  int64_t encryption_key = subject_number;
  for (int loop = 0; loop < loops; ++loop) {
    Iterate(encryption_key, subject_number);
  }
  return encryption_key;
}

std::string run(const std::string &input) {
  // Your code goes here
  std::istringstream iss(input);
  std::string line;
  std::getline(iss, line);
  int64_t card_public = atoll(line.c_str());
  std::getline(iss, line);
  int64_t door_public = atoll(line.c_str());
  return std::to_string(GetEncryptionKey(card_public, door_public));
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
