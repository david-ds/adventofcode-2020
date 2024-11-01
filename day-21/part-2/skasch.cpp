#include <ctime>
#include <iostream>
#include <map>
#include <sstream>
#include <string>
#include <unordered_map>
#include <unordered_set>
#include <vector>

static std::unordered_map<std::string, std::unordered_set<std::string>>
    kAllergensToIngredients;
static std::map<std::string, std::string> kResolvedAllergenToIngredient;
static std::unordered_map<std::string, std::string>
    kResolvedIngredientToAllergen;

std::pair<std::unordered_set<std::string>, std::unordered_set<std::string>>
ParseLine(const std::string &line) {
  std::unordered_set<std::string> ingredients;
  int pos = 0;
  while (line[pos] != '(') {
    int left = pos;
    while (line[pos] != ' ') {
      ++pos;
    }
    std::string ingredient = line.substr(left, pos - left);
    ingredients.insert(ingredient);
    ++pos;
  }
  pos += 10;
  std::unordered_set<std::string> allergens;
  while (pos < line.size()) {
    int left = pos;
    while (line[pos] != ',' && line[pos] != ')') {
      ++pos;
    }
    allergens.insert(line.substr(left, pos - left));
    pos += 2;
  }
  return std::make_pair(ingredients, allergens);
}

void UpdateAllergensMap(const std::unordered_set<std::string> &ingredients,
                        const std::unordered_set<std::string> &allergens) {
  for (const std::string &allergen : allergens) {
    if (auto it = kAllergensToIngredients.find(allergen);
        it == kAllergensToIngredients.end()) {
      kAllergensToIngredients[allergen] = {ingredients.begin(),
                                           ingredients.end()};
    } else {
      std::unordered_set<std::string> ingredients_to_remove;
      for (const std::string &ingredient : it->second) {
        if (auto it2 = ingredients.find(ingredient); it2 == ingredients.end()) {
          ingredients_to_remove.insert(ingredient);
        }
      }
      for (const std::string &ingredient : ingredients_to_remove) {
        it->second.erase(it->second.find(ingredient));
      }
    }
    std::vector<std::string> resolved_allergens = {allergen};
    while (!resolved_allergens.empty()) {
      std::string resolved_allergen = resolved_allergens.back();
      resolved_allergens.pop_back();
      if (kAllergensToIngredients[resolved_allergen].size() != 1) {
        continue;
      }
      std::string resolved_ingredient =
          *kAllergensToIngredients[resolved_allergen].begin();
      kResolvedAllergenToIngredient[resolved_allergen] = resolved_ingredient;
      kResolvedIngredientToAllergen[resolved_ingredient] = resolved_allergen;
      for (auto &[allergen, ingredients] : kAllergensToIngredients) {
        if (auto it = ingredients.find(resolved_ingredient);
            it != ingredients.end()) {
          ingredients.erase(it);
          resolved_allergens.push_back(allergen);
        }
      }
    }
  }
}

std::string run(const std::string &input) {
  // Your code goes here
  std::istringstream iss(input);
  for (std::string line; std::getline(iss, line);) {
    auto [ingredients, allergens] = ParseLine(line);
    UpdateAllergensMap(ingredients, allergens);
  }
  std::string res = "";
  for (const auto &[_, ingredient] : kResolvedAllergenToIngredient) {
    if (!res.empty()) {
      res.push_back(',');
    }
    res.append(ingredient);
  }
  return res;
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
