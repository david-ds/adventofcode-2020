#include <iostream>
#include <algorithm>
#include <unordered_map>
#include <unordered_set>
#include <vector>
#include <string>
#include <ctime>


using namespace std;

bool all_one(const unordered_map<string, unordered_set<string>>& ingredents_by_allergen) {
    for (const pair<string, unordered_set<string>>& entry: ingredents_by_allergen) {
        if (entry.second.size() != 1) return false;
    }
    return true;
}

string run(char* s) {
    int i = 0;
    unordered_map<string, unordered_set<string>> ingredents_by_allergen;
    unordered_set<string> all_allergens, all_ingredients;

    while (s[i]) {
        if (s[i] == '\n') {
            i++;
            continue;
        }
        unordered_set<string> ingredients;
        while (s[i] != '(') {
            int start = i;
            while (s[i] != ' ') i++;
            string ingredient(s+start, s+i);
            all_ingredients.insert(ingredient);
            ingredients.insert(ingredient);
            i++;
        }
        i += 10;
        while (s[i] != ')') {
            int start = i;
            while (s[i] != ',' && s[i] != ')') i++;
            string allergen(s+start, s+i);
            all_allergens.insert(allergen);
            if (s[i] == ',') i += 2;
            if (ingredents_by_allergen.find(allergen) == ingredents_by_allergen.end()) {
                ingredents_by_allergen[allergen] = ingredients;
            } else {
                unordered_set<string> to_remove;
                for (const string& x: ingredents_by_allergen[allergen]) {
                    if (ingredients.find(x) == ingredients.end()) to_remove.insert(x);
                }
                for (const string& x: to_remove) {
                    ingredents_by_allergen[allergen].erase(x);
                }
            }
        }
        i++;
    }
    
    while (!all_one(ingredents_by_allergen)) {
        for (const pair<string, unordered_set<string>>& entry: ingredents_by_allergen) {
            if (entry.second.size() > 1) continue;
            for (const string& ingredient: entry.second) {
                for (const string& allergen: all_allergens) {
                    if (entry.first == allergen) continue;
                    ingredents_by_allergen[allergen].erase(ingredient);
                }
            }
        }
    }

    vector<string> allergens_array(all_allergens.begin(), all_allergens.end());
    sort(allergens_array.begin(), allergens_array.end());

    string res;
    for (const string& allergen: allergens_array) {
        for (const string& ingredient: ingredents_by_allergen[allergen]) {
            res += ingredient + ",";
        }
    }

    return res.substr(0, res.size()-1);
}

int main(int argc, char** argv) {
    if (argc < 2) {
        cout << "Missing one argument" << endl;
        exit(1);
    }

    clock_t start = clock();
    string answer = run(argv[1]);
    
    cout << "_duration:" << float( clock () - start ) * 1000.0 /  CLOCKS_PER_SEC << "\n";
    cout << answer << "\n";
    return 0;
}
